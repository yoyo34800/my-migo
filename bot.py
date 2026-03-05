import os
import anthropic
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("8114725670:AAHB9yyplVuRkuNVJoHBNepf0dMjZ-6qR_4")
print(f"TOKEN EXISTS: {BOT_TOKEN is not None}")
CLAUDE_KEY = os.getenv("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")

AGENT_PERSONALITY = """
أنت وكيل ذكاء اصطناعي متخصص في التسويق الرقمي والتصميم.
صاحبك مصمم شعارات على ملابس يبيع في تونس وأوروبا.
مهمتك:
- تكتب كابشن وهاشتاقات احترافية للمنشورات
- ترد على العملاء بلغتهم (عربي، فرنسي، إنجليزي...)
- تبيع بأسلوب مقنع وودي
- لا عنصرية، لا إساءة للأديان
- تكون مرح وإنساني في تعاملك
"""

client = anthropic.Anthropic(api_key=CLAUDE_KEY)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text or ""
    user_name = update.effective_user.first_name or "صديقي"
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action="typing"
    )
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system=AGENT_PERSONALITY,
        messages=[{"role": "user", "content": f"{user_name} يقول: {user_msg}"}]
    )
    reply = response.content[0].text
    await update.message.reply_text(reply)

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    caption = update.message.caption or "صورة بدون وصف"
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system=AGENT_PERSONALITY,
        messages=[{
            "role": "user",
            "content": f"أرسلت لك صورة تصميم مع الوصف: {caption}. اكتب كابشن احترافي وهاشتاقات للنشر على إنستغرام."
        }]
    )
    reply = response.content[0].text
    await update.message.reply_text(f"✅ جاهز للنشر:\n\n{reply}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    print("🤖 الوكيل يعمل الآن...")
    app.run_polling()

if __name__ == "__main__":
    main()


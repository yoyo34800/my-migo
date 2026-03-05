import os
import anthropic
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = "
8114725670:AAHB9yyplVuRkuNVJoHBNepf0dMjZ-6qR_4"
CLAUDE_KEY = "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
"

PERSONALITY = """أنت وكيل ذكاء اصطناعي مساعد لمصمم شعارات على ملابس.
ترد بلغة المستخدم. تكتب كابشن وهاشتاقات احترافية.
تبيع بأسلوب ودي ومقنع. لا عنصرية ولا إساءة."""

client = anthropic.Anthropic(api_key=CLAUDE_KEY)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text or ""
    name = update.effective_user.first_name or "صديقي"
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system=PERSONALITY,
        messages=[{"role": "user", "content": f"{name}: {msg}"}]
    )
    await update.message.reply_text(response.content[0].text)

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    caption = update.message.caption or "تصميم جديد"
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system=PERSONALITY,
        messages=[{"role": "user", "content": f"اكتب كابشن وهاشتاقات لهذا التصميم: {caption}"}]
    )
    await update.message.reply_text(f"✅ جاهز:\n\n{response.content[0].text}")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
print("🤖 البوت يعمل!")
app.run_polling()

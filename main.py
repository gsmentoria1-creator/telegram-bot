import os
import anthropic
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
      await update.message.reply_text("Ola! Sou um bot com IA. Mande uma mensagem para conversar!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
      user_message = update.message.text
      message = client.messages.create(
          model="claude-opus-4-5",
          max_tokens=1024,
          messages=[{"role": "user", "content": user_message}]
      )
      response = message.content[0].text
      await update.message.reply_text(response)

if __name__ == "__main__":
      app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
      app.add_handler(CommandHandler("start", start))
      app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
      print("Bot iniciado!")
      app.run_polling()

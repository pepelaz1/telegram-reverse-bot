import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

def reverse_text(text: str) -> str:
    return text[::-1]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Отправь слово или фразу — я разверну её задом наперёд."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    if len(user_text) > 1000:
        await update.message.reply_text("Слишком длинный текст (максимум 1000 символов)!")
        return
    reversed_text = reverse_text(user_text)
    await update.message.reply_text(reversed_text)

def check_and_set_webhook():
    TOKEN = "8555598494:AAHOzva7mHXOZFfN0Lf6azoIzOND_I75fn0"
    WEBHOOK_URL = "https://reasonable-spirit-production.up.railway.app/bot"
    
    # Проверяем текущий webhook
    response = requests.get(f"https://api.telegram.org/bot{TOKEN}/getWebhookInfo")
    webhook_info = response.json()
    
    # Если webhook не установлен или URL не совпадает
    if not webhook_info["result"]["url"] == WEBHOOK_URL:
        # Устанавливаем webhook
        payload = {
            "url": WEBHOOK_URL,
            "drop_pending_updates": True
        }
        response = requests.post(
            f"https://api.telegram.org/bot{TOKEN}/setWebhook",
            json=payload
        )
        print("Webhook обновлён:", response.json())
    else:
        print("Webhook уже настроен корректно.")

def main():
    TOKEN = "8555598494:AAHOzva7mHXOZFfN0Lf6azoIzOND_I75fn0"
    PORT = int(os.environ.get("PORT", 8080))
    WEBHOOK_URL = "https://reasonable-spirit-production.up.railway.app/bot"


    # Сначала проверяем/устанавливаем webhook
    check_and_set_webhook()

    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запускаем webhook
    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL
    )

if __name__ == "__main__":
    main()

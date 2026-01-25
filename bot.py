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

def main():
    TOKEN = "7993497213:AAFX-iDorDOF7tcJRWLi2z54PtM6jp-Ou9Q"  
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    application.run_polling()

if __name__ == "__main__":
    main()

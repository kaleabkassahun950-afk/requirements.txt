import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN", "8959470710:AAGX7zMKq0XbP3pwJEDo9y0JfStumYJU2zE")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [
        ['🏠 ቤት (House)', '🚗 መኪና (Car)'],
        ['🚜 ማሽነሪ (Machinery)', '📱 ኤሌክትሮኒክስ (Electronics)']
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "እንኳን ወደ ደላላ ቦት በደህና መጡ! 👋\nእባክዎን የሚፈልጉትን ዘርፍ ይምረጡ፡",
        reply_markup=markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if 'ቤት' in text or 'House' in text or text.lower() == 'house':
        await update.message.reply_text("🏠 **የቤት ደላላ ክፍል**\n\n1. የሚሸጥ ቤት ለማስመዝገብ\n2. የሚከራይ ቤት ለማግኘት\n\nእባክዎን ዝርዝር መረጃ ይጻፉልን።")
    elif 'መኪና' in text or 'Car' in text or text.lower() == 'car':
        await update.message.reply_text("🚗 **የመኪና ደላላ ክፍል**\n\n1. የሚሸጥ መኪና ለማስመዝገብ\n2. የሚከራይ መኪና ለመግዛት/ለመከራየት\n\nየመኪናውን ሞዴል እና ዋጋ ይፃፉልን።")
    elif 'ማሽነሪ' in text or 'Machinery' in text or text.lower() == 'machinery':
        await update.message.reply_text("🚜 **የማሽነሪ ደላላ ክፍል**\n\nከባድ ማሽነሪዎችን ለመሸጥ ወይም ለመከራየት ዝርዝሩን ያስገቡ።")
    elif 'ኤሌክትሮኒክስ' in text or 'Electronics' in text or text.lower() == 'electronics':
        await update.message.reply_text("📱 **የኤሌክትሮኒክስ ደላላ ክፍል**\n\nስልኮች፣ ላፕቶፖች እና ሌሎች እቃዎችን ለመግዛት/ለመሸጥ ዝርዝር ይፃፉ።")
    else:
        await update.message.reply_text("እባክዎን ከታች ካሉት ቁልፎች አንዱን ይምረጡ ወይም /start ብለው እንደገና ይጀምሩ።")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is running...")
    app.run_polling()

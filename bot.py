import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# ከ BotFather ያገኙትን ቶከን እዚህ ይተኩ
TOKEN = "8959470710:AAGX7zMKq0XbP3pwJEDo9y0JfStumYJU2zE"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🟢 Buy Asset", callback_data='buy'),
            InlineKeyboardButton("🔴 Sell Asset", callback_data='sell')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("እንኳን ወደ Broker Bot በደህና መጡ! ይምረጡ:", reply_markup=reply_markup)

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'buy':
        await query.edit_message_text("🟢 የመግዢ ትዕዛዝ በመሰራት ላይ ነው...")
    elif query.data == 'sell':
        await query.edit_message_text("🔴 የመሸጫ ትዕዛዝ በመሰራት ላይ ነው...")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))
    
    print("ቦቱ እየሰራ ነው...")
    app.run_polling()

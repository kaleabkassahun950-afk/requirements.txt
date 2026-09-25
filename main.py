import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes, 
    MessageHandler, filters, ConversationHandler
)

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# ቴሌግራም ላይ ከ @userinfobot ያገኘኸውን ID እዚህ አስገባ
ADMIN_CHAT_ID = "8531978555" 

# ደረጃዎች (States)
CHOOSING_CATEGORY, WAITING_FOR_DETAILS = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [['🚗 መኪና (Car)', '🏠 ቤት (House)']]
    await update.message.reply_text(
        "እንኳን ወደ ደላላ ቦት በደህና መጡ! 👋\nእባክዎን የሚፈልጉትን ዘርፍ ይምረጡ፡",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    return CHOOSING_CATEGORY

async def category_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    category = update.message.text
    context.user_data['category'] = category
    
    await update.message.reply_text(
        f"ለ{category} የሚሆን ዝርዝር መረጃ እና የስልክ ቁጥርዎን ያስገቡ፡",
        reply_markup=ReplyKeyboardRemove()
    )
    return WAITING_FOR_DETAILS

async def save_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    category = context.user_data.get('category', 'ያልታወቀ')
    user = update.effective_user

    # ለተጠቃሚው ማረጋገጫ መስጠት
    await update.message.reply_text("መረጃዎ በተሳካ ሁኔታ ተመዝግቧል! እናመሰግናለን።\nእንዳዲስ ለመጀመር /start ይበሉ።")

    # ወደ አንተ (Admin) መረጃውን መላክ
    admin_message = (
        f"📥 **አዲስ ምዝገባ ደርሷል!**\n\n"
        f"👤 **ላኪ:** {user.full_name} (@{user.username})\n"
        f"📌 **ዘርፍ:** {category}\n"
        f"📝 **መረጃ:** {user_text}"
    )
    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_message)

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ሂደቱ ተቋርጧል።", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

if __name__ == '__main__':
    # የቦትህ TOKEN
    TOKEN = "8870538032:AAHlAUc49WqTlYPTSWka2X73pI_IKfZdT6I" 
    
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING_CATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, category_chosen)],
            WAITING_FOR_DETAILS: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_details)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    app.add_handler(conv_handler)
    app.run_polling()

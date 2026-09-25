import logging
import os
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes, 
    MessageHandler, filters, ConversationHandler
)

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Environment variables ወይም በቀጥታ ማስገባት
TOKEN = os.getenv("TOKEN", "8870538032:AAHlAUc49WqTlYPTSWka2X73pI_IKfZdT6I")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID", "8531978555")

# ደረጃዎች (States)
CHOOSING_ROLE, CHOOSING_CATEGORY, WAITING_FOR_DETAILS, BUYER_VIEW_CATEGORY = range(4)

# የተመዘገቡ እቃዎችን በደረጃ ለመያዝ (Memory storage)
LISTINGS = {
    '🚗 መኪና (Car)': [],
    '🏠 ቤት (House)': [],
    '⚙️ ማሽነሪ (Machinery)': [],
    '📱 ኤሌክትሮኒክስ (Electronics)': []
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    role_keyboard = [['🛒 ሻጭ (Seller)', '🛍️ ገዢ (Buyer)']]
    await update.message.reply_text(
        "እንኳን ወደ ደላላ ቦት በደህና መጡ! 👋\nእባክዎን የሚፈልጉትን ሚና (Role) ይምረጡ፡",
        reply_markup=ReplyKeyboardMarkup(role_keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    return CHOOSING_ROLE

async def role_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    role = update.message.text
    context.user_data['role'] = role

    category_keyboard = [
        ['🚗 መኪና (Car)', '🏠 ቤት (House)'],
        ['⚙️ ማሽነሪ (Machinery)', '📱 ኤሌክትሮኒክስ (Electronics)']
    ]
    markup = ReplyKeyboardMarkup(category_keyboard, one_time_keyboard=True, resize_keyboard=True)

    if role == '🛒 ሻጭ (Seller)':
        await update.message.reply_text("እቃዎን ለማስገባት የሚፈልጉትን ዘርፍ ይምረጡ፡", reply_markup=markup)
        return CHOOSING_CATEGORY
    elif role == '🛍️ ገዢ (Buyer)':
        await update.message.reply_text("ሊያዩት የሚፈልጉትን ዘርፍ ይምረጡ፡", reply_markup=markup)
        return BUYER_VIEW_CATEGORY
    else:
        await update.message.reply_text("እባክዎ ትክክለኛውን ቁልፍ ይጠቀሙ። /start በመጫን እንደገና ይሞክሩ።", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

async def category_chosen_seller(update: Update, context: ContextTypes.DEFAULT_TYPE):
    category = update.message.text
    if category not in LISTINGS:
        await update.message.reply_text("እባክዎ ከቁልፍ ሰሌዳው ትክክለኛ ዘርፍ ይምረጡ።")
        return CHOOSING_CATEGORY
        
    context.user_data['category'] = category
    
    await update.message.reply_text(
        f"ለ{category} የሚሆን ዝርዝር መረጃ (ዋጋ፣ ሁኔታ፣ መገኛ) እና የስልክ ቁጥርዎን ያስገቡ፡",
        reply_markup=ReplyKeyboardRemove()
    )
    return WAITING_FOR_DETAILS

async def save_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    category = context.user_data.get('category', '🚗 መኪና (Car)')
    user = update.effective_user

    # እቃውን በዝርዝር መዝገብ ውስጥ ማስቀመጥ
    listing_info = {
        'seller_name': user.full_name,
        'seller_username': user.username,

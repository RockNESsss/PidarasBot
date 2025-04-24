import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import TOKEN, ADMIN_ID
from database import *
import sqlite3

bot = telebot.TeleBot(TOKEN)
init_db()
user_states = {}

def send_main_menu(chat_id):
    user_id = chat_id
    circle_id = get_user_circle(user_id)
    keyboard = InlineKeyboardMarkup()
    if not circle_id:
        keyboard.add(InlineKeyboardButton("🌟 Створити коло", callback_data="create_circle"))
        keyboard.add(InlineKeyboardButton("🔗 Приєднатись до кола", callback_data="join_circle"))
        keyboard.add(InlineKeyboardButton("🔥 Підарас дня", callback_data="pidaras_of_day"))
        keyboard.add(InlineKeyboardButton("📢 Оголошення", callback_data="admin_broadcast"))
    else:
        role = get_user_role(get_user_id(user_id), circle_id)
        keyboard.add(InlineKeyboardButton("🧑‍🤝‍🧑 Змінити рейтинг", callback_data="start_rating"))
        keyboard.add(InlineKeyboardButton("📋 Моє коло", callback_data="view_circle"))
        if role in ("admin", "moderator"):
            keyboard.add(InlineKeyboardButton("📝 Створити пропозицію", callback_data="create_proposal"))
            keyboard.add(InlineKeyboardButton("🏆 Титули тижня", callback_data="weekly_titles"))
        if role == "admin":
            keyboard.add(InlineKeyboardButton("➕ Додати учасника", callback_data="add_person"))
            keyboard.add(InlineKeyboardButton("👑 Призначити редактора", callback_data="assign_moderator"))
            keyboard.add(InlineKeyboardButton("❌ Видалити учасника", callback_data="remove_person"))
        keyboard.add(InlineKeyboardButton("🚪 Покинути коло", callback_data="leave_circle"))
        if user_id == ADMIN_ID:
            keyboard.add(InlineKeyboardButton("🔥 Підарас дня", callback_data="pidaras_of_day"))
            keyboard.add(InlineKeyboardButton("📢 Оголошення", callback_data="admin_broadcast"))
    bot.send_message(chat_id, "Меню доступних дій:", reply_markup=keyboard)

@bot.message_handler(commands=["start"])
def handle_start(message):
    add_user(message.from_user.id, message.from_user.username)
    send_main_menu(message.chat.id)

import scheduler
bot.polling(non_stop=True)

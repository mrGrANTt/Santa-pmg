from aiogram.utils.keyboard import InlineKeyboardBuilder
import secret_santa_bot





def get_player_settings_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="❌ - выгнать", callback_data="kick")
    keyboard.button(text="✏️ - изменить", callback_data="edit")
    keyboard.button(text="🛑 - заблокировать", callback_data="ban")
    keyboard.adjust(2)
    return keyboard.as_markup()

def get_player_edit_keyboard(mode = 0):
    keyboard = InlineKeyboardBuilder()
    if mode == 1:
        keyboard.button(text="✏️ имя", callback_data="edit_plr_name")
        keyboard.button(text="✏️ предпочтения", callback_data="edit_plr_wishes")
        keyboard.button(text="⬅️ назад", callback_data="edit_plr_back")
    else:
        keyboard.button(text="✏️ имя", callback_data="edit_name")
        keyboard.button(text="✏️ предпочтения", callback_data="edit_wishes")
        keyboard.button(text="⬅️ назад", callback_data="edit_back")
    keyboard.adjust(2)
    return keyboard.as_markup()

def get_main_menu_keyboard(is_admin):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="✏️ изменить профиль", callback_data="edit_plr")
    if secret_santa_bot.game_started != 0:
        keyboard.button(text="💬 написать другу", callback_data="send_friend")
    if not is_admin:
        keyboard.button(text="⚠️ написать админу", callback_data="send_admin")
    keyboard.button(text="❗информация", callback_data="info")
    if is_admin:
        keyboard.button(text="💻 админ понель", callback_data="admin_menu")
    keyboard.adjust(1)
    return keyboard.as_markup()

def get_cancel_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="⛔ отмена", callback_data="cancel")
    return keyboard.as_markup()
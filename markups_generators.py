from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import secret_santa_bot





def get_player_settings_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="❌ выгнать", callback_data="kick")
    keyboard.button(text="✏️ изменить", callback_data="edit")
    keyboard.button(text="🛑 заблокировать", callback_data="ban")
    keyboard.button(text="💬 написать", callback_data="send_player_adm")
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

def get_main_menu_keyboard(is_admin, user_id):
    keyboard = InlineKeyboardBuilder()
    reg = secret_santa_bot.registered(user_id)
    if not secret_santa_bot.check_ban(user_id) and secret_santa_bot.game_started is None:
        if reg:
            keyboard.button(text="✏️ изменить профиль", callback_data="edit_plr")
        else:
            keyboard.button(text="🎁 участвовать", callback_data="register")

    if secret_santa_bot.game_started is not None: #TODO: EDIT
        keyboard.button(text="💬 написать другу", callback_data="send_friend")
        keyboard.button(text="💬 написать санте", callback_data="send_santa")
    if not is_admin:
        keyboard.button(text="⚠️ написать админу", callback_data="send_admin")
    keyboard.button(text="❗информация", callback_data="game_information")
    if is_admin:
        keyboard.button(text="💻 админ понель", callback_data="admin_menu")
    if reg and secret_santa_bot.game_started is None:
        keyboard.button(text="💔 покинуть игру", callback_data="leave_game")
    keyboard.adjust(1)
    return keyboard.as_markup()

def get_cancel_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="⛔ отмена", callback_data="cancel")
    return keyboard.as_markup()

def get_unban_keyboard(link, name):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="🪪 профиль", url=f"tg://user?id={link}"))
    keyboard.button(text="❌ разблокировать", callback_data=f"unban:{link}:{name}")
    keyboard.adjust(1)
    return keyboard.as_markup()

def get_admin_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="📃 игроки", callback_data="players_list")
    keyboard.button(text="🛑 заблокированные", callback_data="bunned_list")
    keyboard.button(text="📬 отправить всем", callback_data="broadcast")
    if secret_santa_bot.game_started is not None:
        keyboard.button(text="💔 прервать игру", callback_data="stop_game")
    else:
        keyboard.button(text="🎁 начать игру", callback_data="start_game")
    keyboard.button(text="⬅️ назад", callback_data="edit_plr_back")
    keyboard.adjust(1)
    return keyboard.as_markup()

def get_getter_keyboard(link):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="🪪 профиль", url=f"tg://user?id={link}"))
    return keyboard.as_markup()
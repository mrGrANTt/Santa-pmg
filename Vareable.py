BOT_TOKEN = "7272189082:AAHsqAypl-ozlp5VXLpZqgrCiJkwm3pyiAM"
ADMIN_ID = None
DB_FILE = "secret_santa.db"
WELCOME_MSG = "пиривет!"
PRINT_NAME_MSG = "Введи имя!"
PRINT_WISHES_MSG = "Введи предпочтения!"
SUCCESS_REGISTRY_MSG = "Вы зырегестрированы!"
YOU_BANED_MSG = "Вы заблокированы!"
YOU_KICKED_MSG = "Вы были выброшены из игры, но всё ещё можете повторно зарегестрироваться введя /start"
MENU_MSG = "Меню"
MSG_SEND = "Сообщение отправлено"
HAVE_NOT_PERMISSION = "Недостаточно доступа"

open("admin.txt", "a+", encoding="utf-8")
with open("admin.txt", "r", encoding="utf-8") as f:
    value = f.read()
    print(value)
    if value and value != "":
        ADMIN_ID = int(value)
    print(ADMIN_ID)
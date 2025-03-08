import os
from dotenv import load_dotenv

config_file = "files/config.env"
ADMIN_ID = None

open("files/admin.txt", "a+", encoding="utf-8")
with open("files/admin.txt", "r", encoding="utf-8") as f:
    value = f.read()
    if value and value != "":
        ADMIN_ID = int(value)

if not os.path.exists(config_file):
    with open(config_file, "w", encoding="utf-8") as f:
        f.write("BOT_TOKEN='your_bot_token'\n")
        f.write("ADMIN_ID='your_tg_id'\n")
        f.write("DB_FILE='files/secret_santa.db'\n")
        f.write("WELCOME_MSG='пиривет!'\n")
        f.write("PRINT_NAME_MSG='Введи имя!'\n")
        f.write("PRINT_WISHES_MSG='Введи предпочтения!'\n")
        f.write("SUCCESS_REGISTRY_MSG='Вы зырегестрированы!'\n")
        f.write("YOU_BANED_MSG='Вы заблокированы!'\n")
        f.write("YOU_KICKED_MSG='Вы были выброшены из игры, но всё ещё можете повторно зарегестрироваться введя /start'\n")
        f.write("MENU_MSG='Меню'\n")
        f.write("MSG_SEND='Сообщение отправлено'\n")
        f.write("HAVE_NOT_PERMISSION='Не достаточно доступа'\n")
        f.write("GAME_INFO='Игра тайный друг, создана @mrgrantt'\n")
    print(f"{config_file} создан.")
else:
    print(f"{config_file} уже существует, загрузка значений...")

load_dotenv(config_file)


BOT_TOKEN = os.getenv("BOT_TOKEN", "")
DB_FILE = os.getenv("DB_FILE", "files/secret_santa.db")
WELCOME_MSG = os.getenv("WELCOME_MSG", "пиривет!")
PRINT_NAME_MSG = os.getenv("PRINT_NAME_MSG", "Введи имя!")
PRINT_WISHES_MSG = os.getenv("PRINT_WISHES_MSG", "Введи предпочтения!")
SUCCESS_REGISTRY_MSG = os.getenv("SUCCESS_REGISTRY_MSG", "Вы зырегестрированы!")
YOU_BANED_MSG = os.getenv("YOU_BANED_MSG", "Вы заблокированы!")
YOU_KICKED_MSG = os.getenv("YOU_KICKED_MSG", "Вы были выброшены из игры, но всё ещё можете повторно зарегестрироваться введя /start'")
MENU_MSG = os.getenv("MENU_MSG", "Меню")
MSG_SEND = os.getenv("MSG_SEND", "Сообщение отправлено")
HAVE_NOT_PERMISSION = os.getenv("HAVE_NOT_PERMISSION", "Не достаточно доступа")
GAME_INFO = os.getenv("GAME_INFO", "Игра тайный друг, создана @mrgrantt")

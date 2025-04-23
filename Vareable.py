import os
from dotenv import load_dotenv

if not os.path.exists('files'):
    os.makedirs('files')

open("files/token.txt", "a+", encoding="utf-8").close()
open("files/baned.txt", "a+", encoding="utf-8").close()

config_file = "files/config.env"

if not os.path.exists(config_file):
    with open(config_file, "w", encoding="utf-8") as f:
        f.write("ADMIN_ID=''\n")
        f.write("DB_FILE='files/secret_santa.db'\n")
        f.write("\n\n")
        f.write("WELCOME_MSG='Привет!'\n")
        f.write("PRINT_NAME_MSG='Введи имя!'\n")
        f.write("PRINT_WISHES_MSG='Введи предпочтения!'\n")
        f.write("SUCCESS_REGISTRY_MSG='Вы зарегистрированы!'\n")
        f.write("YOU_BANED_MSG='Вы заблокированы!'\n")
        f.write("YOU_KICKED_MSG='Вы были выброшены из игры, но всё ещё можете повторно зарегистрироваться нажав кнопку в меню'\n")
        f.write("MENU_MSG='Меню\nВы: {name}\nПредпочтения: {wishes}'\n")
        f.write("MSG_SEND='Сообщение отправлено'\n")
        f.write("HAVE_NOT_PERMISSION='Не достаточно доступа'\n")
        f.write("GAME_INFO='Игра тайный друг, создана @mrgrantt\n\nДокументация: https://mrgteam.gitbook.io/mrgteam/'\n")
        f.write("COMMAND_NOT_EXIST='Такой команды не существует...'\n")
        f.write("NOT_VALID_INPUT='Если вы пытаетесь ввести какую-то информацию, то начните с начала, предыдущая сессия была сброшена!'\n")
        f.write("EMPTY_LIST='Тут пока-что пусто('\n")
        f.write("USER_LIST_FORMATE='{username} ({name})\n\n{wishes}'\n")
        f.write("GAME_IS_STARTED='Игра уже началась. Вы поздно опомнились'\n")
        f.write("INPUT_CANCELLED='Ввод отменён'\n")
        f.write("ADMIN_NOT_STATED='Администратор не назначен, невозможно отправить ему сообщение...'\n")
        f.write("INPUT_MESSAGE='Введите сообщение для администратора:'\n")
        f.write("CHECK_ACTUALITY_INFO='Проверьте актуальность данных!\nВведите /users_list ещё раз'\n")
        f.write("USER_REMOVED='Пользователь {name} удалён и уведомлен об этом!'\n")
        f.write("INPUT_SOMETHING='Введите {edit_type}!'\n")
        f.write("USER_BANED_MSG='Пользователь {name} заблокирован и уведомлен об этом!'\n")
        f.write("PLAYER_LIVED='Игрок {name} покидает игру('\n")
        f.write("GAME_NOT_STARTED='Игра ещё не начата...'\n")
        f.write("INPUT_FOR_USER_MSG='Введите сообщение для получателя'\n")
        f.write("INPUT_FOR_SANTA_MSG='Введите сообщение для отправителя'\n")
        f.write("INPUT_MSG='Введите сообщение для {name}:'\n")
        f.write("BANED_USER_INFO='Имя: {name}'\n")
        f.write("THERE_ARE_NO_BANED_USER='В этом городе пока спокойно👮 \n(нет заблокированных игроков)'\n")
        f.write("USER_UNBAN_INFO='Пользователь {name} разблокирован'\n")
        f.write("YOU_ARE_UNBANNED='Вы разблокированы и снова можете пользоваться ботом.\n Обновите меню введя /menu'\n")
        f.write("GAME_ABORTED='Игра прервана по решению администрации'\n")
        f.write("GAME_SUCCESS_ABORTED='Игра успешно прервана'\n")
        f.write("YOU_NEED_MORE_PLAYER='Недостаточно участников для формирования цепочки'\n")
        f.write("GAME_SUCCESS_STARTED='Игра успешно запущена'\n")
        f.write("YOU_GIVE_TO='Вы дарите: {name}\nЕго пожелания: {wishes}'\n")
        f.write("YOUR_INFO_UPDATED='Данные вашего аккаунта обновлены обновлены! Новые данные:\n\nИмя: {name}\nПредпочтения: {wishes}'\n")
    print(f"{config_file} создан.")
else:
    print(f"{config_file} уже существует, загрузка значений...")

load_dotenv(config_file)


ADMIN_ID = os.getenv("ADMIN_ID", None)
if ADMIN_ID == "" or not ADMIN_ID:
    ADMIN_ID = None
else:
    ADMIN_ID = int(ADMIN_ID)

DB_FILE = os.getenv("DB_FILE", "files/secret_santa.db")
WELCOME_MSG =             os.getenv("WELCOME_MSG", "Привет!")
PRINT_NAME_MSG =          os.getenv("PRINT_NAME_MSG", "Введи имя!")
PRINT_WISHES_MSG =        os.getenv("PRINT_WISHES_MSG", "Введи предпочтения!")
SUCCESS_REGISTRY_MSG =    os.getenv("SUCCESS_REGISTRY_MSG", "Вы зарегистрированы!")
YOU_BANED_MSG =           os.getenv("YOU_BANED_MSG", "Вы заблокированы!")
YOU_KICKED_MSG =          os.getenv("YOU_KICKED_MSG", "Вы были выброшены из игры, но всё ещё можете повторно зарегистрироваться нажав кнопку в меню'")
MENU_MSG =                os.getenv("MENU_MSG", "Меню\nВы: {name}\nПредпочтения: {wishes}")
MSG_SEND =                os.getenv("MSG_SEND", "Сообщение отправлено")
HAVE_NOT_PERMISSION =     os.getenv("HAVE_NOT_PERMISSION", "Не достаточно доступа")
GAME_INFO =               os.getenv("GAME_INFO", "Игра тайный друг, создана @mrgrantt\n\nДокументация: https://mrgteam.gitbook.io/mrgteam/")
COMMAND_NOT_EXIST =       os.getenv("COMMAND_NOT_EXIST", "Такой команды не существует...")
NOT_VALID_INPUT =         os.getenv("NOT_VALID_INPUT", "Если вы пытаетесь ввести какую-то информацию, то начните с начала, предыдущая сессия была сброшена!")
EMPTY_LIST =              os.getenv("EMPTY_LIST", "Тут пока-что пусто(")
USER_LIST_FORMATE =       os.getenv("USER_LIST_FORMATE", "{username} ({name})\n\n{wishes}")
GAME_IS_STARTED =         os.getenv("GAME_IS_STARTED", "Игра уже началась. Вы поздно опомнились")
INPUT_CANCELLED =         os.getenv("INPUT_CANCELLED", "Ввод отменён")
ADMIN_NOT_STATED =        os.getenv("ADMIN_NOT_STATED", "Администратор не назначен, невозможно отправить ему сообщение...")
INPUT_MESSAGE =           os.getenv("INPUT_MESSAGE", "Введите сообщение для администратора:")
CHECK_ACTUALITY_INFO =    os.getenv("CHECK_ACTUALITY_INFO", "Проверьте актуальность данных!\nВведите /users_list ещё раз")
USER_REMOVED =            os.getenv("USER_REMOVED", "Пользователь {name} удалён и уведомлен об этом!")
INPUT_SOMETHING =         os.getenv("INPUT_SOMETHING", "Введите {edit_type}!")
USER_BANED_MSG =          os.getenv("USER_BANED_MSG", "Пользователь {name} заблокирован и уведомлен об этом!")
PLAYER_LIVED =            os.getenv("PLAYER_LIVED", "Игрок {name} покидает игру(")
GAME_NOT_STARTED =        os.getenv("GAME_NOT_STARTED", "Игра ещё не начата...")
INPUT_FOR_USER_MSG =      os.getenv("INPUT_FOR_USER_MSG", "Введите сообщение для получателя")
INPUT_FOR_SANTA_MSG =     os.getenv("INPUT_FOR_SANTA_MSG", "Введите сообщение для отправителя")
INPUT_MSG =               os.getenv("INPUT_MSG", "Введите сообщение для {name}:")
BANED_USER_INFO =         os.getenv("BANED_USER_INFO", "Имя: {name}")
THERE_ARE_NO_BANED_USER = os.getenv("THERE_ARE_NO_BANED_USER", "В этом городе пока спокойно👮 \n(нет заблокированных игроков)")
USER_UNBAN_INFO =         os.getenv("USER_UNBAN_INFO", "Пользователь {name} разблокирован")
YOU_ARE_UNBANNED =        os.getenv("YOU_ARE_UNBANNED", "Вы разблокированы и снова можете пользоваться ботом.\n Обновите меню введя /menu")
GAME_ABORTED =            os.getenv("GAME_ABORTED", "Игра прервана по решению администрации")
GAME_SUCCESS_ABORTED =    os.getenv("GAME_SUCCESS_ABORTED", "Игра успешно прервана")
YOU_NEED_MORE_PLAYER =    os.getenv("YOU_NEED_MORE_PLAYER", "Недостаточно участников для формирования цепочки")
GAME_SUCCESS_STARTED =    os.getenv("GAME_SUCCESS_STARTED", "Игра успешно запущена")
YOU_GIVE_TO =             os.getenv("YOU_GIVE_TO", "Вы дарите: {name}\nЕго пожелания: {wishes}")
YOUR_INFO_UPDATED =       os.getenv("YOUR_INFO_UPDATED", "Данные вашего аккаунта обновлены обновлены! Новые данные:\n\nИмя: {name}\nПредпочтения: {wishes}")

BOT_TOKEN = None
with open("files/token.txt", "r", encoding="utf-8") as f:
    value = f.read()
    if value and value != "":
        BOT_TOKEN = value



import array
import sqlite3

from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
import asyncio

from aiogram.utils.token import TokenValidationError

import Vareable
import button_click_handler
import console_command
import msg_cmd
import secret_santa_bot

#TODO:                                                                                                                  starting process
#TODO:                                                                                                                  starting process
#TODO:                                                                                                                  starting process

# Initializing the bot and dispatcher with async functionality
try:
    secret_santa_bot.bot = Bot(token=Vareable.BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
except TokenValidationError:
    print("Неверный токен бота. Пожалуйста проверте коректность указанных данных и перезапустите программу...")
    exit()

secret_santa_bot.dp = Dispatcher()

secret_santa_bot.dp.include_router(router=button_click_handler.router)
secret_santa_bot.dp.include_router(router=msg_cmd.router)

# Database setup
secret_santa_bot.conn = sqlite3.connect(Vareable.DB_FILE)
secret_santa_bot.cursor = secret_santa_bot.conn.cursor()

# Creating tables
secret_santa_bot.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
 	id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    username TEXT NOT NULL,
    name TEXT,
    wishes TEXT
)''')
secret_santa_bot.cursor.execute('''CREATE TABLE IF NOT EXISTS pairs (
 	id INTEGER PRIMARY KEY AUTOINCREMENT,
    giver_id INTEGER,
    receiver_id INTEGER,
    FOREIGN KEY (giver_id) REFERENCES users (id),
    FOREIGN KEY (receiver_id) REFERENCES users (id)
)''')
secret_santa_bot.cursor.execute("PRAGMA journal_mode=WAL;")
secret_santa_bot.conn.commit()


secret_santa_bot.cursor.execute("SELECT id FROM pairs LIMIT 1")
game_started = secret_santa_bot.cursor.fetchone()

if game_started:
    secret_santa_bot.game_started = 1
else:
    secret_santa_bot.game_started = None


commands = {
    'help': console_command.help_cmd,
    'stop': console_command.stop_cmd
}





#TODO:                                                                                                                  start
#TODO:                                                                                                                  start
#TODO:                                                                                                                  start

async def run_bot():
    print("Бот запущен!")
    asyncio.create_task(cmd())
    await secret_santa_bot.dp.start_polling(secret_santa_bot.bot)

async def cmd():
    print('staring console!')
    while True:
        cmd_name = await asyncio.to_thread(input, "Введите команду: ")

        arr = cmd_name.split(' ')
        cmd_name = arr[0]
        del arr[0]

        await run_command(cmd_name, clean_array(arr))
        if cmd_name == "stop":
            break


def clean_array(arr):
    new_arr = list()
    for a in arr:
        if a:
            new_arr.append(a)
    return new_arr


async def run_command(command: str, args: array):
    if not command:
        return
    print()
    if command in commands:
        func = commands[command]
        await func(args)
    else:
        print("Unregistered command")



def main():
    asyncio.run(run_bot())

if __name__ == "__main__":
    main()  # Запуск программы

# отвечать на любое сообщение
# переписать лист пользователей чтобы тот не нуждался в перезагрузке
# log в консоли
# кнопка "инфа о паре" в меню
# инфа о паре в листе(Если админ не в игре)
# вместо ошибки доступа - проcьбу обновить токен
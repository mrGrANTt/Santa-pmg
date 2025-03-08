import sqlite3

from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
import asyncio

from aiogram.utils.token import TokenValidationError

import Vareable
import button_click_handler
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
secret_santa_bot.conn.commit()

game_started = secret_santa_bot.cursor.fetchone()
if secret_santa_bot.game_started:
    secret_santa_bot.game_started = 1
else:
    secret_santa_bot.game_started = 0










#TODO:                                                                                                                  start
#TODO:                                                                                                                  start
#TODO:                                                                                                                  start

async def run_bot():
    print("Бот запущен!")
    await secret_santa_bot.dp.start_polling(secret_santa_bot.bot)


async def main():
    await run_bot()

if __name__ == "__main__":
    asyncio.run(main())



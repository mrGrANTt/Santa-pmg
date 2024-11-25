import signal
import sqlite3
import sys
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.client.bot import DefaultBotProperties
import random
import asyncio
import os
import shutil
import Vareable
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Initializing the bot and dispatcher with async functionality
bot = Bot(token=Vareable.BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

secret_santa_db = "secret_santa.db"

# Database setup
conn = sqlite3.connect(secret_santa_db)
cursor = conn.cursor()

# Creating tables
cursor.execute('''CREATE TABLE IF NOT EXISTS players (
    user_id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    name TEXT NOT NULL,
    preferences TEXT
)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS pairs (
    giver_id INTEGER,
    receiver_id INTEGER,
    FOREIGN KEY (giver_id) REFERENCES players (user_id),
    FOREIGN KEY (receiver_id) REFERENCES players (user_id)
)''')
cursor.execute("PRAGMA journal_mode=WAL;")
conn.commit()

welcomeMsg = '''🎅 Добро пожаловать на Тайного Санту! 🎅

📜 Условия участия:

   🔸 На протяжении месяца дарим мини-подарки выпавшим людям, а за неделю-две до Нового Года отдаём финальный подарок 🎁

   🔸 Минимальная стоимость финального подарка: 500 руб. (меньше нельзя, больше можно) 💸

   🔸 Мини-подарки не имеют ограничения по стоимости. Они не обязательны, но будут приятны! 🧸

   🔸 Создана [группа для участников](https://t.me/+jcwpkICx4D0zNmUy). Пожалуйста, присоединяйтесь 📢

   🔸 По вопросам пишите в группу или админу через команду /admin 🗿

   🔸 Чтобы записаться в игру введите /join и действуйте по инструкции  🧰
'''

importentMag = '''        ‼️‼️ ВАЖНО ‼️‼️

🔒 Никто не должен знать, кто кому дарит. Подарки можно передавать анонимно, закидывая в портфель или прятать как закладки и указывать место место через команду /send или передавать их другим способом. Главное — анонимность! Так будет веселее 🙃
'''


# State machine for the join command
class JoinGameState(StatesGroup):
    waiting_for_name = State()
    waiting_for_preferences = State()


# Register a new player
@dp.message(Command("start"))
async def start(message: Message):
    await bot.send_message(message.chat.id, welcomeMsg, disable_web_page_preview=True, parse_mode="Markdown")
    await bot.send_message(message.chat.id, importentMag)


@dp.message(Command("join"))
async def start_join(message: Message, state: FSMContext):
    if Vareable.GAME_STARTED != 0:
        await message.answer("Слишком поздно, игра уже началась (.")
        return
    await message.answer("Введите ваше имя.", reply_markup=getKeyboard())
    await state.set_state(JoinGameState.waiting_for_name)


@dp.message(JoinGameState.waiting_for_name)
async def enter_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Теперь введите ваши предпочтения.", reply_markup=getKeyboard())
    await state.set_state(JoinGameState.waiting_for_preferences)


@dp.message(JoinGameState.waiting_for_preferences)
async def enter_preferences(message: Message, state: FSMContext):
    preferences = message.text
    user_data = await state.get_data()
    name = user_data['name']
    user_id = message.from_user.id
    username = message.from_user.username

    if not username:
        username = message.from_user.first_name

    # Saving user data to the database
    cursor.execute(
        "INSERT OR REPLACE INTO players (user_id, username, name, preferences) VALUES (?, ?, ?, ?)",
        (user_id, username, name, preferences)
    )
    conn.commit()

    await message.answer(f"Вы записаны на тайного Санту!\nИмя: {name}\nПредпочтения: {preferences}")
    await bot.send_message(Vareable.ADMIN_ID,
                           f"Игрок записан на тайного Санту!\nИмя: {name}\nПредпочтения: {preferences}")
    await state.clear()


# Leave the game
@dp.message(Command("leave"))
async def leave_game(message: Message):
    if Vareable.GAME_STARTED != 0:
        await message.answer("Слишком поздно, игра уже началась (.")
        return
    user_id = message.from_user.id
    cursor.execute("DELETE FROM players WHERE user_id = ?", (user_id,))
    conn.commit()
    await message.answer("Вы покинули тайного Санту (")
    await bot.send_message(Vareable.ADMIN_ID, f"{user_id} покинул игру (")


class MsgState(StatesGroup):
    message = State()


# Send anonymous message to assigned person
@dp.message(Command("send"))
async def send_anonymous_message(message: Message, state: FSMContext):
    await message.answer("Введите сообщение.", reply_markup=getKeyboard())
    await state.set_state(MsgState.message)


@dp.message(MsgState.message)
async def enter_name(message: Message, state: FSMContext):
    user_id = message.from_user.id
    cursor.execute("SELECT receiver_id FROM pairs WHERE giver_id = ?", (user_id,))
    result = cursor.fetchone()
    if not result:
        await message.answer("У вас еще нет назначенного получателя или игра еще не началась.")
        await state.clear()
        return
    receiver_id = result[0]
    await bot.send_message(receiver_id, f"Вам пишет Санта: {message.text}")
    await state.clear()


class AdmMsgState(StatesGroup):
    message = State()


def getKeyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="[❌]-отменить", callback_data="cansel")
    keyboard.adjust(1)
    return keyboard.as_markup()


# Message admin
@dp.message(Command("admin"))
async def message_admin(message: Message, state: FSMContext):
    await message.answer("Введите сообщение.", reply_markup=getKeyboard())
    await state.set_state(AdmMsgState.message)


@dp.message(AdmMsgState.message)
async def message_admin(message: Message, state: FSMContext):
    username = message.from_user.username
    if not username:
        username = message.from_user.first_name

    await bot.send_message(Vareable.ADMIN_ID, f"Сообщение от {username}: {message.text}")
    await message.answer("Сообщение отправлено админу.")
    await state.clear()


# Admin: View list of players
@dp.message(Command("list"))
async def list_players(message: Message):
    if message.from_user.id != Vareable.ADMIN_ID:
        await message.answer("Нет доступа к команде!")
        return

    cursor.execute("SELECT name, preferences, user_id FROM players")
    players = cursor.fetchall()
    if not players:
        await message.answer("Нет игроков в игре.")
    else:
        response = "Игроки:\n\n" + "\n".join([f"`{p[2]}` ({p[0]}) - {p[1]}\n\n" for p in players])
        await message.answer(response, parse_mode="Markdown")


# Admin: Remove a player
@dp.message(Command("remove"))
async def remove_player(message: Message):
    if message.from_user.id != Vareable.ADMIN_ID:
        await message.answer("Нет доступа к команде!")
        return

    username = message.text.split(' ', 1)[1].strip() if ' ' in message.text else ''
    cursor.execute("DELETE FROM players WHERE user_id = ?", (username,))
    conn.commit()
    await message.answer(f"Игрок c id '{username}' удалён из игры.")


class PlrSendMsg(StatesGroup):
    msg = State()
    plrId = State()


@dp.message(Command("send_plr"))
async def start_join(message: Message, state: FSMContext):
    if message.from_user.id != Vareable.ADMIN_ID:
        await message.answer("Нет доступа к команде!")
        return
    await message.answer("Введите id получателя.", reply_markup=getKeyboard())
    await state.set_state(PlrSendMsg.plrId)


@dp.message(PlrSendMsg.plrId)
async def enter_plrId(message: Message, state: FSMContext):
    await state.update_data(plrId=message.text)
    await message.answer("Теперь введите cообщение.", reply_markup=getKeyboard())
    await state.set_state(PlrSendMsg.msg)


@dp.message(PlrSendMsg.msg)
async def enter_preferences(message: Message, state: FSMContext):
    msg = message.text
    user_data = await state.get_data()
    plrId = user_data['plrId']

    await bot.send_message(plrId, "Сообщение от админа: " + msg)
    await message.answer(f"Сообщение отправлено!")
    await state.clear()


# Admin: Start distribution
@dp.message(Command("distribute"))
async def distribute_pairs(message: Message):
    if message.from_user.id != Vareable.ADMIN_ID:
        await message.answer("Нет доступа к команде!")
        return
    cursor.execute("SELECT user_id FROM players")
    user_ids = [row[0] for row in cursor.fetchall()]
    if len(user_ids) < 2:
        await message.answer("Недостаточно людей для начала игры!")
        return

    # Shuffle and assign pairs
    random.shuffle(user_ids)
    pairs = list(zip(user_ids, user_ids[1:] + [user_ids[0]]))  # Circular pairing

    # Store pairs in the database
    cursor.execute("DELETE FROM pairs")
    cursor.executemany("INSERT INTO pairs (giver_id, receiver_id) VALUES (?, ?)", pairs)
    conn.commit()

    # Notify each player of their assigned person
    for giver_id, receiver_id in pairs:
        cursor.execute("SELECT name, preferences FROM players WHERE user_id = ?", (receiver_id,))
        receiver_info = cursor.fetchone()
        await bot.send_message(giver_id,
                               f"Вы дарите подарки для: {receiver_info[0]},\n\n Его предпочтения: {receiver_info[1]}")

    Vareable.GAME_STARTED = 1
    await message.answer("Игроки распределены!")


# Admin: Send global message
@dp.message(Command("broadcast"))
async def broadcast_message(message: Message):
    if message.from_user.id != Vareable.ADMIN_ID:
        await message.answer("Нет доступа к команде!")
        return

    await bot.send_message(Vareable.ADMIN_ID, "Stopping proces!")
    text = message.text.split(' ', 1)[1] if ' ' in message.text else ''
    if not text:
        await message.answer("Укажите сообщение для отправки после команды.")
        return
    cursor.execute("SELECT user_id FROM players")
    for (user_id,) in cursor.fetchall():
        await bot.send_message(user_id, f"Глобальное сообщение: {text}")


# Admin: Send global message
@dp.message(Command("stop"))
async def broadcast_message(message: Message):
    if message.from_user.id != Vareable.ADMIN_ID:
        await message.answer("Нет доступа к команде!")
        return
    await stopping()



@dp.callback_query(lambda callback: callback.data == "cansel")
async def handle_button_click(callback_query: CallbackQuery, state: FSMContext):
    # Здесь можно вызвать любую функцию или выполнить код
    await state.clear()
    await bot.send_message(callback_query.from_user.id, "Ввод отменён!")


async def runBot():
    print("runBot")
    cursor.execute("SELECT receiver_id FROM pairs LIMIT 1")
    result = cursor.fetchone()
    if result:
        Vareable.GAME_STARTED = 1
    await dp.start_polling(bot)


enabled = 1


async def copy_db_periodically(src):
    next_run = datetime.now() + timedelta(hours=Vareable.INTERVAL)
    while enabled != 0:
        now = datetime.now()
        if now >= next_run:
            try:
                dst_dir = f"backup/{datetime.now().date()}"
                dst = os.path.join(dst_dir, f"secret_santa-{datetime.now().hour}") + ".db"
                # Проверка доступности файла
                if not os.path.exists(dst_dir):
                    os.makedirs(dst_dir)
                if os.path.exists(src) and os.access(src, os.R_OK):

                    shutil.copy2(src, dst)  # Копируем файл с сохранением метаданных
                    await bot.send_message(Vareable.ADMIN_ID, f"Файл {src} скопирован в {dst}.")
                else:
                    await bot.send_message(Vareable.ADMIN_ID, f"Файл {src} недоступен для чтения.")
            except Exception as e:
                await bot.send_message(Vareable.ADMIN_ID, f"Ошибка при копировании файла: {e}")
            finally:
                next_run = datetime.now() + timedelta(hours=Vareable.INTERVAL)

        # Ждем заданный интервал
        await asyncio.sleep(60)


# Пример запуска
async def backUp():
    print("beckUp")
    await copy_db_periodically(secret_santa_db)


async def stopping():
    print("Stopping proces, wait for a minute...")
    await bot.send_message(Vareable.ADMIN_ID, "Stopping proces, wait for a minute...")

    await dp.stop_polling()
    global enabled
    enabled = 0

async def main():
    bot_task = asyncio.create_task(runBot())
    backup_task = asyncio.create_task(backUp())

    try:
        await asyncio.gather(bot_task, backup_task)
    except KeyboardInterrupt:
        await stopping()

if __name__ == "__main__":
    asyncio.run(main())

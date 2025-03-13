#TODO:                                                                                                                  Vareables
#TODO:                                                                                                                  Vareables
#TODO:                                                                                                                  Vareables
import shutil

from aiogram.types import Message

bot = None
dp = None


# Database setup
conn = None
cursor = None

game_started = None




import sqlite3
import Vareable
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

conn = sqlite3.connect(Vareable.DB_FILE)
cursor = conn.cursor()
bot = Bot(token=Vareable.BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()


#TODO:                                                                                                                  help func
#TODO:                                                                                                                  help func
#TODO:                                                                                                                  help func

def get_plr_id_from_list(message: Message):
    us_id = message.text.split(')')[0]
    cursor.execute("SELECT user_id FROM users WHERE id = ?", (us_id,))
    conn.commit()
    result = cursor.fetchone()
    if not result:
        return None
    return result[0]

def check_ban(plr_id):
    with open("files/baned.txt", "r", encoding="utf-8") as f:
        baned = f.read()
        return baned.find(f"{plr_id}") != -1

def ban(plr_id):
    cursor.execute("DELETE FROM users WHERE user_id = ?", (plr_id,))
    conn.commit()
    with open("files/baned.txt", "w", encoding="utf-8") as f:
        f.write(f"{plr_id}\n")

def unban(plr_id):
    with open("files/baned.txt", "r", encoding="utf-8") as f:
        with open("files/temp.txt", "w", encoding="utf-8") as t:
            lien = f.readline()
            while lien != "":
                if lien.find(str(plr_id)) == -1:
                    t.write(f"{lien}\n")
                lien = f.readline()
    shutil.move("files/temp.txt", "files/baned.txt")

def registered(plr_id):
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (plr_id,))
    return cursor.fetchone()
#TODO:                                                                                                                  Vareables
#TODO:                                                                                                                  Vareables
#TODO:                                                                                                                  Vareables
from aiofiles.os import rename
from aiogram.types import Message

bot = None
dp = None


# Database setup
conn = None
cursor = None

game_started = None






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
    with open("baned.txt", "r", encoding="utf-8") as f:
        baned = f.read()
        return baned.find(f"{plr_id}") != -1

def ban(plr_id):
    cursor.execute("DELETE FROM users WHERE user_id = ?", (plr_id,))
    with open("baned.txt", "w", encoding="utf-8") as f:
        f.write(f"{plr_id}\n")

def unban(plr_id):
    with open("baned.txt", "r", encoding="utf-8") as f:
        with open("temp.txt", "w", encoding="utf-8") as t:
            lien = f.readline()
            while lien != "":
                if lien != plr_id:
                    t.write(f"{lien}\n")
                lien = f.readline()
    rename("temp.txt", "baned.txt")
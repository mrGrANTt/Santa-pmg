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

def placeholder(string: str, uuid):
    cursor.execute("SELECT * FROM users WHERE user_id = ?",(uuid,))
    res = cursor.fetchone()
    if res:
        name = str(res[3])
        username = str(res[2])
        wishes = str(res[4])
        user_id = str(res[1])
    else:
        user_id = "-"
        name = "-"
        username = "-"
        wishes = "-"
    return (string
            .replace("{name}", name)
            .replace("{name\\}", "{name}")
            .replace("{username}", username)
            .replace("{username\\}", "{username}")
            .replace("{wishes}", wishes)
            .replace("{user_id\\}", "{user_id}")
            .replace("{user_id}", user_id)
            .replace("{wishes\\}", "{wishes}")
            )
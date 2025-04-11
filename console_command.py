import array

import Vareable
import secret_santa_bot


async def help_cmd(args: array):
    print("help - print this list",
          "\nstop - protected stopping program")


async def stop_cmd(args: array):
    await secret_santa_bot.dp.stop_polling()
    await secret_santa_bot.bot.session.close()
    secret_santa_bot.cursor.close()
    secret_santa_bot.conn.commit()
    secret_santa_bot.conn.close()

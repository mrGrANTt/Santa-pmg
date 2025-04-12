from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

router = Router()

import Vareable
import markups_generators
import secret_santa_bot
import States









#TODO:                                                                                                                  State
#TODO:                                                                                                                  State
#TODO:                                                                                                                  State

@router.message(States.JoinGameState.waiting_for_name)
async def get_name(message: Message, state: FSMContext):
    if secret_santa_bot.game_started is not None:
        await message.answer(Vareable.GAME_IS_STARTED)
        return
    await state.update_data(name=message.text)
    await secret_santa_bot.bot.send_message(message.from_user.id, Vareable.PRINT_WISHES_MSG, reply_markup=markups_generators.get_cancel_keyboard())
    await state.set_state(States.JoinGameState.waiting_for_wishes)

@router.message(States.JoinGameState.waiting_for_wishes)
async def get_wishes(message: Message, state: FSMContext):
    if secret_santa_bot.game_started is not None:
        await message.answer(Vareable.GAME_IS_STARTED)
        return
    user_id = message.from_user.id
    us = message.chat.username
    name = (await state.get_data())["name"]
    wishes = message.text

    if us is None:
        us = message.chat.first_name
        if message.chat.last_name is not None:
            us = us + " " + message.chat.last_name

    secret_santa_bot.cursor.execute("INSERT OR REPLACE INTO users(user_id, username, name, wishes) VALUES (?, ?, ?, ?)", (user_id, us, name, wishes))
    secret_santa_bot.conn.commit()
    await message.answer(Vareable.SUCCESS_REGISTRY_MSG)
    if Vareable.ADMIN_ID:
        await secret_santa_bot.bot.send_message(Vareable.ADMIN_ID, f"Пользователь \"{name}\" записан")
    await state.clear()
    await secret_santa_bot.bot.send_message(message.from_user.id, secret_santa_bot.placeholder(Vareable.MENU_MSG, message.from_user.id), reply_markup=markups_generators.get_main_menu_keyboard(message.from_user.id == Vareable.ADMIN_ID, message.from_user.id))


@router.message(States.MsgState.message)
async def egit_values_message(message: Message, state: FSMContext):
    if secret_santa_bot.game_started is not None:
        await message.answer(Vareable.GAME_IS_STARTED)
        return
    eType : str = await state.get_value("edit_type")
    if eType == "edit_name" or eType == "edit_plr_name":
        column = "name"
    else:
        column = "wishes"
    uuid = await state.get_value("edit_name_plr")
    secret_santa_bot.cursor.execute(f"UPDATE users SET {column}=? WHERE user_id=?;", (message.text, uuid))
    secret_santa_bot.conn.commit()
    if uuid != message.from_user.id:
        await secret_santa_bot.bot.send_message(uuid, secret_santa_bot.placeholder(Vareable.YOUR_INFO_UPDATED, uuid))
    await message.answer("Данные обновлены!")
    await state.clear()
    if eType.find("plr") != -1:
        await secret_santa_bot.bot.send_message(message.from_user.id, secret_santa_bot.placeholder(Vareable.MENU_MSG, message.from_user.id), reply_markup=markups_generators.get_main_menu_keyboard(message.from_user.id == Vareable.ADMIN_ID, message.from_user.id))


@router.message(States.GlobalMsgState.message)
async def global_message(message: Message, state : FSMContext):
    if message.from_user.id != Vareable.ADMIN_ID:
        await secret_santa_bot.bot.send_message(message.from_user.id, Vareable.HAVE_NOT_PERMISSION)
        return
    secret_santa_bot.cursor.execute("SELECT user_id FROM users;")
    res = secret_santa_bot.cursor.fetchall()
    if res:
        for one in res:
            await secret_santa_bot.bot.send_message(one[0], "Глобальное сообщение:")
            await secret_santa_bot.bot.send_message(one[0], message.text)
    await secret_santa_bot.bot.send_message(message.from_user.id, secret_santa_bot.placeholder(Vareable.MENU_MSG, message.from_user.id), reply_markup=markups_generators.get_main_menu_keyboard(message.from_user.id == Vareable.ADMIN_ID, message.from_user.id))
    await state.clear()

@router.message(States.AdmMsgState.message)
async def admin_message(message: Message, state : FSMContext):
    if Vareable.ADMIN_ID:
        await secret_santa_bot.bot.send_message(Vareable.ADMIN_ID, secret_santa_bot.placeholder("Новое сообщение от {name}!", message.from_user.id))
        await secret_santa_bot.bot.send_message(Vareable.ADMIN_ID, message.text)
        await message.answer(Vareable.MSG_SEND)
    else:
        await message.answer(Vareable.ADMIN_NOT_STATED_MSG)
    await state.clear()
    await secret_santa_bot.bot.send_message(message.from_user.id, secret_santa_bot.placeholder(Vareable.MENU_MSG, message.from_user.id), reply_markup=markups_generators.get_main_menu_keyboard(message.from_user.id == Vareable.ADMIN_ID, message.from_user.id))


@router.message(States.GetterMsgState.message)
async def getter_message(message: Message, state: FSMContext):
    await send_msg(message, "giver_id")
    await message.answer(Vareable.MSG_SEND)
    await state.clear()
    await secret_santa_bot.bot.send_message(message.from_user.id, secret_santa_bot.placeholder(Vareable.MENU_MSG, message.from_user.id), reply_markup=markups_generators.get_main_menu_keyboard(message.from_user.id == Vareable.ADMIN_ID, message.from_user.id))

@router.message(States.SantaMsgState.message)
async def santa_message(message: Message, state: FSMContext):
    await send_msg(message, "receiver_id")
    await message.answer(Vareable.MSG_SEND)
    await state.clear()
    await secret_santa_bot.bot.send_message(message.from_user.id,
                                            secret_santa_bot.placeholder(Vareable.MENU_MSG, message.from_user.id),
                                            reply_markup=markups_generators.get_main_menu_keyboard(
                                                message.from_user.id == Vareable.ADMIN_ID, message.from_user.id))


async def send_msg(message: Message, execute_type):
    secret_santa_bot.cursor.execute(f"SELECT {execute_type} FROM pairs WHERE (giver_id = ? OR receiver_id = ?) AND {execute_type} != ?", (message.from_user.id,message.from_user.id,message.from_user.id))
    res = secret_santa_bot.cursor.fetchone()
    if res:
        uuid = res[0]
        if execute_type == "giver_id":
            await secret_santa_bot.bot.send_message(uuid, "Вам сообщение от получателя:")
        else:
            await secret_santa_bot.bot.send_message(uuid, "Вам сообщение от отправителя:")
        await secret_santa_bot.bot.send_message(uuid, message.text)
#TODO: Check working!!!


@router.message(States.UserMsgState.message)
async def admin_to_user_msg(message: Message, state: FSMContext):
    uuid = int(await state.get_value("uuid"))
    await secret_santa_bot.bot.send_message(uuid, "Новое сообщение от админа!")
    await secret_santa_bot.bot.send_message(uuid, message.text)
    await state.clear()
    await message.answer(Vareable.MSG_SEND)









#TODO:                                                                                                                  Commands
#TODO:                                                                                                                  Commands
#TODO:                                                                                                                  Commands

@router.message(Command("start"))
async def start(message: Message):
    await secret_santa_bot.bot.send_message(message.from_user.id, Vareable.WELCOME_MSG)
    await secret_santa_bot.bot.send_message(message.from_user.id, secret_santa_bot.placeholder(Vareable.MENU_MSG, message.from_user.id), reply_markup=markups_generators.get_main_menu_keyboard(message.from_user.id == Vareable.ADMIN_ID, message.from_user.id))

@router.message(Command("menu"))
async def start(message: Message):
    await secret_santa_bot.bot.send_message(message.from_user.id, secret_santa_bot.placeholder(Vareable.MENU_MSG, message.from_user.id), reply_markup=markups_generators.get_main_menu_keyboard(message.from_user.id == Vareable.ADMIN_ID, message.from_user.id))

# @router.message(Command("im_admin"))
# async def im_admin(message: Message):
#     if not Vareable.ADMIN_ID:
#         Vareable.ADMIN_ID = message.from_user.id
#         set_key(Vareable.config_file, "ADMIN_ID", str(Vareable.ADMIN_ID))
#         await message.answer("Теперь вы администратов!")
#         await secret_santa_bot.bot.send_message(message.from_user.id, secret_santa_bot.placeholder(Vareable.MENU_MSG, message.from_user.id), reply_markup=markups_generators.get_main_menu_keyboard(message.from_user.id == Vareable.ADMIN_ID, message.from_user.id))



@router.message(Command("users_list"))
async def print_list(message: Message, state: FSMContext):
    if message.from_user.id != Vareable.ADMIN_ID:
        await secret_santa_bot.bot.send_message(message.from_user.id, Vareable.HAVE_NOT_PERMISSION)
        return
    secret_santa_bot.cursor.execute("SELECT * FROM users")
    secret_santa_bot.conn.commit()
    result = secret_santa_bot.cursor.fetchall()
    if not result:
        await message.answer(Vareable.EMPTY_LIST)
        return
    for value in result:
        text = f'{value[0]})' + (Vareable.USER_LIST_FORMATE
                                 .replace("{user_id}", value[1])
                                 .replace("{user_id\\}", "{user_id}")
                                 .replace("{username}", value[2])
                                 .replace("{username\\}", "{username}")
                                 .replace("{name}", value[3])
                                 .replace("{name\\}", "{name}")
                                 .replace("{wishes}", value[4])
                                 .replace("{wishes\\}", "{wishes}")
                                 )
        await message.answer(text, reply_markup=markups_generators.get_player_settings_keyboard())











#TODO:                                                                                                                  Other
#TODO:                                                                                                                  Other
#TODO:                                                                                                                  Other

@router.message()
async def start(message: Message):
    if message.text and message.text != "" and message.text[0] == "/":
        await secret_santa_bot.bot.send_message(message.from_user.id, Vareable.COMMAND_NOT_EXIST)
    else:
        await secret_santa_bot.bot.send_message(message.from_user.id, Vareable.NOT_VALID_INPUT)

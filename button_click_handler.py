import random
from tkinter.font import names

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

router = Router()

import Vareable
import secret_santa_bot
import States
import markups_generators



@router.callback_query(lambda callback: callback.data == "register")
async def handle_button_click_register(callback_query: CallbackQuery, state: FSMContext):
    if secret_santa_bot.game_started is not None:
        await secret_santa_bot.bot.send_message(callback_query.from_user.id, Vareable.GAME_IS_STARTED)
        return
    if not secret_santa_bot.check_ban(callback_query.from_user.id):
        await secret_santa_bot.bot.send_message(callback_query.from_user.id, Vareable.PRINT_NAME_MSG, reply_markup=markups_generators.get_cancel_keyboard())
        await callback_query.answer()
        await state.set_state(States.JoinGameState.waiting_for_name)
    else:
        await secret_santa_bot.bot.send_message(callback_query.from_user.id, Vareable.YOU_BANED_MSG)
        await callback_query.answer()

@router.callback_query(lambda callback: callback.data == "players_list")
async def handle_button_click_register(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.from_user.id != Vareable.ADMIN_ID:
        await secret_santa_bot.bot.send_message(callback_query.from_user.id, Vareable.HAVE_NOT_PERMISSION)
        await callback_query.answer()
        return
    secret_santa_bot.cursor.execute("SELECT * FROM users")
    result = secret_santa_bot.cursor.fetchall()
    if not result:
        await secret_santa_bot.bot.send_message(callback_query.from_user.id, Vareable.EMPTY_LIST)
        await callback_query.answer()
        return
    for value in result:
        text = f'{value[0]}) {value[2]} ({value[3]})\n\n{value[4]}'
        await secret_santa_bot.bot.send_message(callback_query.from_user.id, text, reply_markup=markups_generators.get_player_settings_keyboard())
    await callback_query.answer()


@router.callback_query(lambda callback: callback.data == "game_information")
async def handle_button_click_info(callback_query: CallbackQuery):
    await secret_santa_bot.bot.send_message(callback_query.from_user.id, Vareable.GAME_INFO)
    await callback_query.answer()


@router.callback_query(lambda callback: callback.data == "cancel")
async def handle_button_click_cancel(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()
    await secret_santa_bot.bot.send_message(callback_query.from_user.id, Vareable.INPUT_CANCELLED)
    await secret_santa_bot.bot.send_message(callback_query.from_user.id, secret_santa_bot.placeholder(Vareable.MENU_MSG, callback_query.from_user.id), reply_markup=markups_generators.get_main_menu_keyboard(callback_query.from_user.id == Vareable.ADMIN_ID, callback_query.from_user.id))
    await callback_query.answer()


@router.callback_query(lambda callback: callback.data == "send_admin")
async def handle_button_click_send_admin(callback_query: CallbackQuery, state: FSMContext):
    if not Vareable.ADMIN_ID:
        await secret_santa_bot.bot.send_message(callback_query.from_user.id, Vareable.ADMIN_NOT_STATED)
        await callback_query.answer()
        return
    await secret_santa_bot.bot.send_message(callback_query.from_user.id, Vareable.INPUT_MESSAGE, reply_markup=markups_generators.get_cancel_keyboard())
    await callback_query.answer()
    await state.set_state(States.AdmMsgState.message)


@router.callback_query(lambda callback: callback.data == "kick")
async def handle_button_click_kick(callback_query: CallbackQuery):
    if callback_query.from_user.id != Vareable.ADMIN_ID:
        await secret_santa_bot.bot.send_message(callback_query.from_user.id, Vareable.HAVE_NOT_PERMISSION)
        await callback_query.answer()
        return
    us_id = secret_santa_bot.get_plr_id_from_list(callback_query.message)
    if not us_id:
        await secret_santa_bot.bot.send_message(callback_query.from_user.id, Vareable.CHECK_ACTUALITY_INFO)
        await callback_query.answer()
        return

    text = secret_santa_bot.placeholder(Vareable.USER_REMOVED, us_id)

    secret_santa_bot.cursor.execute("DELETE FROM users WHERE user_id = ?", (us_id,))
    secret_santa_bot.conn.commit()

    await secret_santa_bot.bot.send_message(us_id, Vareable.YOU_KICKED_MSG)
    await secret_santa_bot.bot.send_message(callback_query.from_user.id, text)
    await callback_query.answer()


@router.callback_query(lambda callback: callback.data == "edit")
async def handle_button_click_edit(callback_query: CallbackQuery):
    if callback_query.from_user.id != Vareable.ADMIN_ID:
        await secret_santa_bot.bot.send_message(callback_query.from_user.id, Vareable.HAVE_NOT_PERMISSION)
        await callback_query.answer()
        return
    await secret_santa_bot.bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        reply_markup=markups_generators.get_player_edit_keyboard())
    await callback_query.answer()


@router.callback_query(lambda callback: callback.data == "edit_back")
async def handle_button_click_edit_back(callback_query: CallbackQuery):
    if callback_query.from_user.id != Vareable.ADMIN_ID:
        await secret_santa_bot.bot.send_message(callback_query.from_user.id, Vareable.HAVE_NOT_PERMISSION)
        await callback_query.answer()
        return
    await secret_santa_bot.bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        reply_markup=markups_generators.get_player_settings_keyboard())
    await callback_query.answer()


@router.callback_query(lambda callback: callback.data == "edit_name" or callback.data == "edit_wishes")
async def handle_button_click_edit_think(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.from_user.id != Vareable.ADMIN_ID:
        await secret_santa_bot.bot.send_message(callback_query.from_user.id, Vareable.HAVE_NOT_PERMISSION)
        await callback_query.answer()
        return

    us_id = secret_santa_bot.get_plr_id_from_list(callback_query.message)
    if not us_id:
        await secret_santa_bot.bot.send_message(callback_query.from_user.id, Vareable.CHECK_ACTUALITY_INFO)
        await callback_query.answer()
        return

    if callback_query.data == "edit_name":
        edit_type = "новое имя"
    else:
        edit_type = "новые предпочтения"

    await secret_santa_bot.bot.send_message(callback_query.from_user.id, Vareable.INPUT_SOMETHING
                                            .replace("{edit_type}", edit_type)
                                            .replace("{edit_type\\}", "{edit_type}"), reply_markup=markups_generators.get_cancel_keyboard())
    await state.update_data(edit_name_plr=us_id, edit_type=callback_query.data)
    await callback_query.answer()
    await state.set_state(States.MsgState.message)


@router.callback_query(lambda callback: callback.data == "edit_plr")
async def handle_button_click_edit_plr(callback_query: CallbackQuery):
    await secret_santa_bot.bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        reply_markup=markups_generators.get_player_edit_keyboard(1))
    await callback_query.answer()


@router.callback_query(lambda callback: callback.data == "edit_plr_back")
async def handle_button_click_edit_plr_back(callback_query: CallbackQuery):
    await secret_santa_bot.bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        reply_markup=markups_generators.get_main_menu_keyboard(
                                            callback_query.from_user.id == Vareable.ADMIN_ID,
                                            callback_query.from_user.id))
    await callback_query.answer()


@router.callback_query(lambda callback: callback.data == "admin_menu")
async def handle_button_click_admin_menu(callback_query: CallbackQuery):
    if callback_query.from_user.id != Vareable.ADMIN_ID:
        await secret_santa_bot.bot.send_message(callback_query.from_user.id, Vareable.HAVE_NOT_PERMISSION)
        await callback_query.answer()
        return
    await secret_santa_bot.bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        reply_markup=markups_generators.get_admin_keyboard())
    await callback_query.answer()


@router.callback_query(lambda callback: callback.data == "edit_plr_name" or callback.data == "edit_plr_wishes")
async def handle_button_click_edit_plr_think(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data == "edit_plr_name":
        edit_type = "новое имя"
    else:
        edit_type = "новые предпочтения"

    await secret_santa_bot.bot.send_message(callback_query.from_user.id, Vareable.INPUT_SOMETHING
                                            .replace("{edit_type}", edit_type)
                                            .replace("{edit_type\\}", "{edit_type}"), reply_markup=markups_generators.get_cancel_keyboard())
    await state.update_data(edit_name_plr=callback_query.from_user.id, edit_type=callback_query.data)
    await callback_query.answer()
    await state.set_state(States.MsgState.message)


@router.callback_query(lambda callback: callback.data == "ban")
async def handle_button_click_ban(callback_query: CallbackQuery):
    if callback_query.from_user.id != Vareable.ADMIN_ID:
        await secret_santa_bot.bot.send_message(callback_query.from_user.id, Vareable.HAVE_NOT_PERMISSION)
        await callback_query.answer()
        return

    us_id = secret_santa_bot.get_plr_id_from_list(callback_query.message)
    if not us_id:
        await secret_santa_bot.bot.send_message(callback_query.from_user.id,
                               Vareable.CHECK_ACTUALITY_INFO)
        await callback_query.answer()
        return

    text = secret_santa_bot.placeholder(Vareable.USER_BANED_MSG, us_id)

    secret_santa_bot.ban(us_id)

    await secret_santa_bot.bot.send_message(us_id,Vareable.YOU_BANED_MSG)
    await secret_santa_bot.bot.send_message(callback_query.from_user.id, text)
    await callback_query.answer()


@router.callback_query(lambda callback: callback.data == "leave_game")
async def handle_button_leave_game(callback_query: CallbackQuery):
    if secret_santa_bot.game_started is not None:
        await secret_santa_bot.bot.send_message(callback_query.from_user.id, Vareable.GAME_IS_STARTED)
        return

    await secret_santa_bot.bot.send_message(Vareable.ADMIN_ID, secret_santa_bot.placeholder(Vareable.PLAYER_LIVED, callback_query.from_user.id))
    secret_santa_bot.cursor.execute("DELETE FROM users WHERE user_id = ?", (callback_query.from_user.id,))
    secret_santa_bot.conn.commit()

    await secret_santa_bot.bot.send_message(callback_query.from_user.id, "Вы покинули игру!")
    await secret_santa_bot.bot.send_message(callback_query.from_user.id, secret_santa_bot.placeholder(Vareable.MENU_MSG, callback_query.from_user.id), reply_markup=markups_generators.get_main_menu_keyboard(callback_query.from_user.id == Vareable.ADMIN_ID, callback_query.from_user.id))
    await callback_query.answer()


@router.callback_query(lambda callback: callback.data == "send_friend" or callback.data == "send_santa")
async def handle_button_send(callback_query: CallbackQuery, state: FSMContext):
    if secret_santa_bot.game_started is None:
        await secret_santa_bot.bot.send_message(callback_query.from_user.id, Vareable.GAME_NOT_STARTED)
        await callback_query.answer()
        return
    if callback_query.data == "send_friend":
        await secret_santa_bot.bot.send_message(callback_query.from_user.id, Vareable.INPUT_FOR_USER_MSG, reply_markup=markups_generators.get_cancel_keyboard())
        await callback_query.answer()
        await state.set_state(States.GetterMsgState.message)
    else:
        await secret_santa_bot.bot.send_message(callback_query.from_user.id, Vareable.INPUT_FOR_SANTA_MSG, reply_markup=markups_generators.get_cancel_keyboard())
        await callback_query.answer()
        await state.set_state(States.SantaMsgState.message)


@router.callback_query(lambda callback: callback.data == "broadcast")
async def handle_button_global_send(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.from_user.id != Vareable.ADMIN_ID:
        await secret_santa_bot.bot.send_message(callback_query.from_user.id, Vareable.HAVE_NOT_PERMISSION)
        await callback_query.answer()
        return
    await callback_query.answer()
    await secret_santa_bot.bot.send_message(callback_query.from_user.id, Vareable.INPUT_MSG, reply_markup=markups_generators.get_cancel_keyboard())
    await callback_query.answer()
    await state.set_state(States.GlobalMsgState.message)

@router.callback_query(lambda callback: callback.data == "send_player_adm")
async def handle_button_send_player_adm(callback_query: CallbackQuery, state: FSMContext):
    uuid = secret_santa_bot.get_plr_id_from_list(callback_query.message)
    await state.update_data(uuid=uuid)
    await secret_santa_bot.bot.send_message(callback_query.from_user.id, secret_santa_bot.placeholder(Vareable.INPUT_MSG, uuid), reply_markup=markups_generators.get_cancel_keyboard())
    await callback_query.answer()
    await state.set_state(States.UserMsgState.message)

@router.callback_query(lambda callback: callback.data == "bunned_list")
async def handle_button_click_bunned_list(callback_query: CallbackQuery, state: FSMContext):
    with open("files/baned.txt", "r", encoding="utf-8") as fl:
        counter = 0
        line = fl.readline()
        while line and line != "":
            chat = await secret_santa_bot.bot.get_chat(int(line))
            if chat:
                if chat.username:
                    name = chat.username
                else:
                    name = chat.first_name + " " + chat.last_name

                await secret_santa_bot.bot.send_message(Vareable.ADMIN_ID, secret_santa_bot.placeholder(Vareable.BANED_USER_INFO
                                                                                                        .replace("{name}", name)
                                                                                                        .replace("{name\\}", "{name}"),
                                                                                                        int(line)),
                                                        reply_markup=markups_generators.get_unban_keyboard(chat.id, name))
                counter += 1
            line = fl.readline()
        if counter == 0:
            await secret_santa_bot.bot.send_message(Vareable.ADMIN_ID, Vareable.THERE_ARE_NO_BANED_USER)
    await callback_query.answer()

@router.callback_query(F.data.startswith("unban:"))
async def handle_button_click_unban_user(callback_query: CallbackQuery):
    if callback_query.from_user.id != Vareable.ADMIN_ID:
        await secret_santa_bot.bot.send_message(callback_query.from_user.id, Vareable.HAVE_NOT_PERMISSION)
        await callback_query.answer()
    arr = callback_query.data.split(":")
    uuid = int(arr[1])
    secret_santa_bot.unban(uuid)
    await secret_santa_bot.bot.send_message(Vareable.ADMIN_ID, secret_santa_bot.placeholder(Vareable.USER_UNBAN_INFO, uuid))
    await secret_santa_bot.bot.send_message(uuid, Vareable.YOU_ARE_UNBANNED)
    await callback_query.answer()


@router.callback_query(lambda callback: callback.data == "stop_game")
async def handle_button_send_player_adm(callback_query: CallbackQuery):
    if callback_query.from_user.id != Vareable.ADMIN_ID:
        await secret_santa_bot.bot.send_message(callback_query.from_user.id, Vareable.HAVE_NOT_PERMISSION)
        await callback_query.answer()

    secret_santa_bot.cursor.execute("SELECT giver_id FROM pairs")
    res = secret_santa_bot.cursor.fetchall()
    if res:
        for one in res:
            await secret_santa_bot.bot.send_message(int(one[0]), Vareable.GAME_ABORTED)

    secret_santa_bot.cursor.execute("DELETE FROM pairs")
    secret_santa_bot.conn.commit()
    secret_santa_bot.game_started = None

    await secret_santa_bot.bot.send_message(callback_query.from_user.id, Vareable.GAME_SUCCESS_ABORTED)
    await callback_query.answer()


@router.callback_query(lambda callback: callback.data == "start_game")
async def handle_button_send_player_adm(callback_query: CallbackQuery):
    if callback_query.from_user.id != Vareable.ADMIN_ID:
        await secret_santa_bot.bot.send_message(callback_query.from_user.id, Vareable.HAVE_NOT_PERMISSION)
        await callback_query.answer()

    secret_santa_bot.cursor.execute("SELECT user_id FROM users")
    users = secret_santa_bot.cursor.fetchall()

    if len(users) < 3:
        await secret_santa_bot.bot.send_message(callback_query.from_user.id, Vareable.YOU_NEED_MORE_PLAYER)
        await callback_query.answer()
        return

    random.shuffle(users)
    print(users)

    pairs = [(users[i][0], users[(i + 1) % len(users)][0]) for i in range(len(users))]
    print(pairs)

    secret_santa_bot.cursor.execute("DELETE FROM pairs")
    secret_santa_bot.cursor.executemany("INSERT INTO pairs (giver_id, receiver_id) VALUES (?, ?)", pairs)
    secret_santa_bot.conn.commit()

    secret_santa_bot.game_started = 1
    await secret_santa_bot.bot.send_message(callback_query.from_user.id, Vareable.GAME_SUCCESS_STARTED)

    secret_santa_bot.cursor.execute("SELECT pairs.giver_id, users.user_id FROM pairs INNER JOIN users ON pairs.receiver_id = users.user_id")
    res = secret_santa_bot.cursor.fetchall()

    if res:
        for one in res:
            uuid = int(one[0])
            msg = await secret_santa_bot.bot.send_message(uuid, secret_santa_bot.placeholder(Vareable.YOU_GIVE_TO, one[1]), reply_markup=markups_generators.get_getter_keyboard(one[1]))
            await secret_santa_bot.bot.pin_chat_message(uuid, msg.message_id)
            await secret_santa_bot.bot.send_message(uuid,
                                                    secret_santa_bot.placeholder(Vareable.MENU_MSG, uuid),
                                                    reply_markup=markups_generators.get_main_menu_keyboard(uuid == Vareable.ADMIN_ID, uuid))
    await callback_query.answer()
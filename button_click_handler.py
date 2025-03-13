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
        await secret_santa_bot.bot.send_message(callback_query.from_user.id, "Тут пока-что пусто(")
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
    await secret_santa_bot.bot.send_message(callback_query.from_user.id, "Ввод отменён")
    await secret_santa_bot.bot.send_message(callback_query.from_user.id, Vareable.MENU_MSG, reply_markup=markups_generators.get_main_menu_keyboard(callback_query.from_user.id == Vareable.ADMIN_ID, callback_query.from_user.id))
    await callback_query.answer()


@router.callback_query(lambda callback: callback.data == "send_admin")
async def handle_button_click_send_admin(callback_query: CallbackQuery, state: FSMContext):
    if not Vareable.ADMIN_ID:
        await secret_santa_bot.bot.send_message(callback_query.from_user.id, "Администратор не назначен, невозможно отправить ему сообщение...")
        await callback_query.answer()
        return
    await secret_santa_bot.bot.send_message(callback_query.from_user.id, "Введите сообщение", reply_markup=markups_generators.get_cancel_keyboard())
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
        await secret_santa_bot.bot.send_message(callback_query.from_user.id, "Проверьте актуальность данных!\nВведите /users_list ещё раз")
        await callback_query.answer()
        return

    secret_santa_bot.cursor.execute("DELETE FROM users WHERE user_id = ?", (us_id,))
    secret_santa_bot.conn.commit()

    await secret_santa_bot.bot.send_message(us_id, Vareable.YOU_KICKED_MSG)
    await secret_santa_bot.bot.send_message(callback_query.from_user.id, "Пользователь удалён и уведамлён об этом!")
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
        await secret_santa_bot.bot.send_message(callback_query.from_user.id, "Проверьте актуальность данных!\nВведите /users_list ещё раз")
        await callback_query.answer()
        return

    if callback_query.data == "edit_name":
        edit_type = "новое имя"
    else:
        edit_type = "новые предпочтения"

    await secret_santa_bot.bot.send_message(callback_query.from_user.id, f"Введите {edit_type}!", reply_markup=markups_generators.get_cancel_keyboard())
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

    await secret_santa_bot.bot.send_message(callback_query.from_user.id, f"Введите {edit_type}!", reply_markup=markups_generators.get_cancel_keyboard())
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
                               "Проверьте актуальность данных!\nВведите /users_list ещё раз")
        await callback_query.answer()
        return

    secret_santa_bot.ban(us_id)

    await secret_santa_bot.bot.send_message(us_id,"Вы были заблокированы в игре, вы не можете повторно зарегестрироваться")
    await secret_santa_bot.bot.send_message(callback_query.from_user.id, "Пользователь заблокирован и уведамлён об этом!")
    await callback_query.answer()


@router.callback_query(lambda callback: callback.data == "leave_game")
async def handle_button_leave_game(callback_query: CallbackQuery):
    secret_santa_bot.cursor.execute("DELETE FROM users WHERE user_id = ?", (callback_query.from_user.id,))
    secret_santa_bot.conn.commit()
    await secret_santa_bot.bot.send_message(callback_query.from_user.id, "Вы покинули игру!")
    await secret_santa_bot.bot.send_message(callback_query.from_user.id, Vareable.MENU_MSG, reply_markup=markups_generators.get_main_menu_keyboard(callback_query.from_user.id == Vareable.ADMIN_ID, callback_query.from_user.id))
    await callback_query.answer()


@router.callback_query(lambda callback: callback.data == "send_friend" or callback.data == "send_santa")
async def handle_button_send(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data == "send_friend":
        await secret_santa_bot.bot.send_message(callback_query.from_user.id, "Введите сообщение для получателя", reply_markup=markups_generators.get_cancel_keyboard())
        await callback_query.answer()
        await state.set_state(States.GetterMsgState.message)
    else:
        await secret_santa_bot.bot.send_message(callback_query.from_user.id, "Введите сообщение для санты", reply_markup=markups_generators.get_cancel_keyboard())
        await callback_query.answer()
        await state.set_state(States.SantaMsgState.message)


@router.callback_query(lambda callback: callback.data == "broadcast")
async def handle_button_global_send(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.from_user.id != Vareable.ADMIN_ID:
        await secret_santa_bot.bot.send_message(callback_query.from_user.id, Vareable.HAVE_NOT_PERMISSION)
        await callback_query.answer()
        return
    await callback_query.answer()
    await secret_santa_bot.bot.send_message(callback_query.from_user.id, "Введите сообщение:", reply_markup=markups_generators.get_cancel_keyboard())
    await callback_query.answer()
    await state.set_state(States.GlobalMsgState.message)

@router.callback_query(lambda callback: callback.data == "send_player_adm")
async def handle_button_send_player_adm(callback_query: CallbackQuery, state: FSMContext):
    uuid = secret_santa_bot.get_plr_id_from_list(callback_query.message)
    await state.update_data(uuid=uuid)
    await secret_santa_bot.bot.send_message(callback_query.from_user.id, "Введите сообщение:", reply_markup=markups_generators.get_cancel_keyboard())
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

                await secret_santa_bot.bot.send_message(Vareable.ADMIN_ID, f"Имя: {name}", reply_markup=markups_generators.get_unban_keyboard(chat.id, name))
                counter += 1
            line = fl.readline()
        if counter == 0:
            await secret_santa_bot.bot.send_message(Vareable.ADMIN_ID, f"Кажется тут пока нет нарушителей")
    await callback_query.answer()

@router.callback_query(F.data.startswith("unban:"))
async def handle_button_click_unban_user(callback_query: CallbackQuery):
    if callback_query.from_user.id != Vareable.ADMIN_ID:
        await secret_santa_bot.bot.send_message(callback_query.from_user.id, Vareable.HAVE_NOT_PERMISSION)
        await callback_query.answer()
    arr = callback_query.data.split(":")
    uuid = int(arr[1])
    name = arr[2]
    secret_santa_bot.unban(uuid)
    await secret_santa_bot.bot.send_message(Vareable.ADMIN_ID, f"Пользователь {name} разблокирован!")
    await secret_santa_bot.bot.send_message(uuid, "Вы разблокированы и снова можете пользоватся ботом.\n Обновите меню введя /menu")
    await callback_query.answer()

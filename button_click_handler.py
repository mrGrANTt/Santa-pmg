from aiogram import Router
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
        await secret_santa_bot.bot.send_message(callback_query.from_user.id, Vareable.PRINT_NAME_MSG)
        await state.set_state(States.JoinGameState.waiting_for_name)
    else:
        await secret_santa_bot.bot.send_message(callback_query.from_user.id, Vareable.YOU_BANED_MSG)

@router.callback_query(lambda callback: callback.data == "cancel")
async def handle_button_click_cancel(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await state.clear()
    await secret_santa_bot.bot.send_message(callback_query.from_user.id, "Ввод отменён")


@router.callback_query(lambda callback: callback.data == "send_admin")
async def handle_button_click_send_admin(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    if not Vareable.ADMIN_ID:
        await secret_santa_bot.bot.send_message(callback_query.from_user.id, "Администратор не назначен, невозможно отправить ему сообщение...")
        return
    await secret_santa_bot.bot.send_message(callback_query.from_user.id, "Введите сообщение", reply_markup=markups_generators.get_cancel_keyboard())
    await state.set_state(States.AdmMsgState.message)


@router.callback_query(lambda callback: callback.data == "kick")
async def handle_button_click_kick(callback_query: CallbackQuery):
    await callback_query.answer()
    us_id = secret_santa_bot.get_plr_id_from_list(callback_query.message)
    if not us_id:
        await secret_santa_bot.bot.send_message(callback_query.from_user.id, "Проверьте актуальность данных!\nВведите /users_list ещё раз")
        return

    secret_santa_bot.cursor.execute("DELETE FROM users WHERE user_id = ?", (us_id,))

    await secret_santa_bot.bot.send_message(us_id, Vareable.YOU_KICKED_MSG)
    await secret_santa_bot.bot.send_message(callback_query.from_user.id, "Пользователь удалён и уведамлён об этом!")


@router.callback_query(lambda callback: callback.data == "edit")
async def handle_button_click_edit(callback_query: CallbackQuery):
    await callback_query.answer()
    await secret_santa_bot.bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        reply_markup=markups_generators.get_player_edit_keyboard())


@router.callback_query(lambda callback: callback.data == "edit_back")
async def handle_button_click_edit_back(callback_query: CallbackQuery):
    await callback_query.answer()
    await secret_santa_bot.bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        reply_markup=markups_generators.get_player_settings_keyboard())


@router.callback_query(lambda callback: callback.data == "edit_name" or callback.data == "edit_wishes")
async def handle_button_click_edit_think(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()

    us_id = secret_santa_bot.get_plr_id_from_list(callback_query.message)
    if not us_id:
        await secret_santa_bot.bot.send_message(callback_query.from_user.id, "Проверьте актуальность данных!\nВведите /users_list ещё раз")
        return

    if callback_query.data == "edit_name":
        edit_type = "новое имя"
    else:
        edit_type = "новые предпочтения"

    await secret_santa_bot.bot.send_message(callback_query.from_user.id, f"Введите {edit_type}!", reply_markup=markups_generators.get_cancel_keyboard())
    await state.update_data(edit_name_plr=us_id, edit_type=callback_query.data)
    await state.set_state(States.MsgState.message)


@router.callback_query(lambda callback: callback.data == "edit_plr")
async def handle_button_click_edit_plr(callback_query: CallbackQuery):
    await callback_query.answer()
    await secret_santa_bot.bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        reply_markup=markups_generators.get_player_edit_keyboard(1))


@router.callback_query(lambda callback: callback.data == "edit_plr_back")
async def handle_button_click_edit_plr_back(callback_query: CallbackQuery):
    await callback_query.answer()
    await secret_santa_bot.bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        reply_markup=markups_generators.get_main_menu_keyboard(callback_query.from_user.id == Vareable.ADMIN_ID))


@router.callback_query(lambda callback: callback.data == "admin_menu")
async def handle_button_click_admin_menu(callback_query: CallbackQuery):
    await callback_query.answer()
    await secret_santa_bot.bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        reply_markup=markups_generators.get_admin_keyboard())


@router.callback_query(lambda callback: callback.data == "edit_plr_name" or callback.data == "edit_plr_wishes")
async def handle_button_click_edit_plr_think(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    if callback_query.data == "edit_plr_name":
        edit_type = "новое имя"
    else:
        edit_type = "новые предпочтения"

    await secret_santa_bot.bot.send_message(callback_query.from_user.id, f"Введите {edit_type}!", reply_markup=markups_generators.get_cancel_keyboard())
    await state.update_data(edit_name_plr=callback_query.from_user.id, edit_type=callback_query.data)
    await state.set_state(States.MsgState.message)


@router.callback_query(lambda callback: callback.data == "ban")
async def handle_button_click_ban(callback_query: CallbackQuery):
    await callback_query.answer()

    us_id = secret_santa_bot.get_plr_id_from_list(callback_query.message)
    if not us_id:
        await secret_santa_bot.bot.send_message(callback_query.from_user.id,
                               "Проверьте актуальность данных!\nВведите /users_list ещё раз")
        return

    secret_santa_bot.ban(us_id)

    await secret_santa_bot.bot.send_message(us_id,"Вы были заблокированы в игре, вы не можете повторно зарегестрироваться")
    await secret_santa_bot.bot.send_message(callback_query.from_user.id, "Пользователь заблокирован и уведамлён об этом!")


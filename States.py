from aiogram.fsm.state import StatesGroup, State


class JoinGameState(StatesGroup):
    waiting_for_name = State()
    waiting_for_wishes = State()

class MsgState(StatesGroup):
    message = State()

class AdmMsgState(StatesGroup):
    message = State()
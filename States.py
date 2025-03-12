from aiogram.fsm.state import StatesGroup, State


class JoinGameState(StatesGroup):
    waiting_for_name = State()
    waiting_for_wishes = State()

class MsgState(StatesGroup):
    message = State()

class AdmMsgState(StatesGroup):
    message = State()

class SantaMsgState(StatesGroup):
    message = State()

class GetterMsgState(StatesGroup):
    message = State()

class GlobalMsgState(StatesGroup):
    message = State()

class UserMsgState(StatesGroup):
    message = State()

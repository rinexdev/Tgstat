from aiogram.fsm.state import StatesGroup, State

class GetID(StatesGroup): #Get info about scamer
    cid = State()
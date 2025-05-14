from aiogram.fsm.state import State, StatesGroup

class Username(StatesGroup):
    username = State()

class AddUsername(StatesGroup):
    user = State()

class AddMediaState(StatesGroup):
    title = State()
    file = State()
    genre = State()

class IdMediaSearchState(StatesGroup):
    id_search = State()
    title_search = State()
    genre_search = State()
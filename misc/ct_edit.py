from aiogram.fsm.state import StatesGroup, State


class CtEditState(StatesGroup):
    """
    * State for editing
    """

    main = State()
    name = State()
    message = State()
    url = State()
    remove = State()
    words_remove = State()
    words_add = State()

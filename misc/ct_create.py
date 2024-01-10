from aiogram.fsm.state import StatesGroup, State



class CtCreateState(StatesGroup):
    """
    * State for creating
    """

    name = State()
    message = State()
    words = State()
    url = State()


cancel_by_state = {
    CtCreateState.name.state : None,
    CtCreateState.message.state : CtCreateState.name,
    CtCreateState.words : CtCreateState.message,
    CtCreateState.url : CtCreateState.words,

}


state_by_state = {
    CtCreateState.name.state : CtCreateState.message,
    CtCreateState.message.state : CtCreateState.words,
    CtCreateState.words.state : CtCreateState.url,
    CtCreateState.url.state : None,
}


args_by_state = {
    CtCreateState.name.state : "ct_create_name",
    CtCreateState.message.state : "ct_create_message",
    CtCreateState.words.state : "ct_create_words",
    CtCreateState.url.state : "ct_create_url",
}
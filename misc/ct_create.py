from aiogram.fsm.state import StatesGroup, State



class CtCreateState(StatesGroup):
    """
    * State for creating
    """

    name = State()
    message = State()
    url = State()


cancel_by_state = {
    CtCreateState.name.state : None,
    CtCreateState.message.state : CtCreateState.name,
    CtCreateState.url : CtCreateState.message
}


state_by_state = {
    CtCreateState.name.state : CtCreateState.message,
    CtCreateState.message.state : CtCreateState.url,
    CtCreateState.url.state : None,
}


args_by_state = {
    CtCreateState.name.state : "ct_create_name",
    CtCreateState.message.state : "ct_create_message",
    CtCreateState.url.state: "ct_create_url",
}
from aiogram import Dispatcher

from State.form import EditText, RefLinkStates
from handler.message import message_edit_text, process_ref_token, process_ref_name


async def register_handlers_message(dp: Dispatcher):
    dp.message.register(message_edit_text, EditText.message)
    dp.message.register(process_ref_name, RefLinkStates.waiting_for_name)
    dp.message.register(process_ref_token, RefLinkStates.waiting_for_token)



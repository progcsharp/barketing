from aiogram import Dispatcher, F

from handler.callback import call_step1, call_step2, call_step3, process_fullprice, process_price2, process_special, \
    check_payment, send_materials, edit_texts_menu, show_text_to_edit, request_new_text, admin_back, ref_links_menu, \
    view_ref_links, ref_link_detail, confirm_delete, add_ref_link_start, cancel_ref_creation


async def register_handlers_callback(dp: Dispatcher):
    dp.callback_query.register(call_step1, F.data == 'step1')
    dp.callback_query.register(call_step2, F.data == 'step2')
    dp.callback_query.register(call_step3, F.data == 'step3')
    dp.callback_query.register(process_fullprice, F.data == 'fullprice')
    dp.callback_query.register(process_price2, F.data == 'price2')
    dp.callback_query.register(process_special, F.data == 'Special course')
    dp.callback_query.register(check_payment, F.data.startswith('check_payment'))
    dp.callback_query.register(send_materials, F.data.startswith('get_materials'))
    ##admin
    dp.callback_query.register(edit_texts_menu, F.data == 'admin_edit_texts')
    dp.callback_query.register(show_text_to_edit, F.data.startswith("edit_text_"))
    dp.callback_query.register(request_new_text, F.data.startswith("change_text_"))
    dp.callback_query.register(admin_back, F.data == 'admin_back')
    dp.callback_query.register(ref_links_menu, F.data == 'admin_ref_links')
    dp.callback_query.register(view_ref_links, F.data == "view_ref_links")
    dp.callback_query.register(ref_link_detail, F.data.startswith("ref_link_detail_"))
    dp.callback_query.register(confirm_delete, F.data.startswith("delete_ref_link_"))
    dp.callback_query.register(add_ref_link_start, F.data == "add_ref_link")
    dp.callback_query.register(cancel_ref_creation, F.data == "cancel_ref_creation")



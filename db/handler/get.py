from db import make_session, User, Link, Message


async def get_user_by_tg_id(tg_id):
    session = make_session()
    user = session.query(User).filter(User.tg_id == tg_id).first()
    session.close()
    if user:
        return False
    return True


async def get_links():
    session = make_session()
    links = session.query(Link)
    session.close()
    return links


async def get_link(link_id):
    session = make_session()
    link = session.query(Link).filter(Link.id == link_id).first()
    session.close()
    return link


async def get_message(slug):
    session = make_session()
    message = session.query(Message).filter(Message.slug == slug).first()
    session.close()
    return message.message


async def get_messages():
    session = make_session()
    message = session.query(Message)
    session.close()
    return message


def check_pay_course(tg_id):
    print(tg_id)
    session = make_session()
    user = session.query(User).filter(User.tg_id == tg_id).first()
    session.close()
    if user.pay_course is None:
        return True
    return False

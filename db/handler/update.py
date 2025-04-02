from db import make_session, Message, Link, User


def update_message(slug, new_message):
    session = make_session()
    message = session.query(Message).filter(Message.slug == slug).first()
    if not message:
        raise ValueError(f"Сообщение с slug '{slug}' не найдено")

    message.message = new_message
    session.commit()
    session.close()
    return message


def update_link(url):
    session = make_session()
    link = session.query(Link).filter(Link.url == url).first()
    link.count += 1
    session.commit()
    session.close()
    return link


def update_user(tg_id):
    session = make_session()
    user = session.query(User).filter(User.tg_id == tg_id).first()
    user.pay_course = 1
    session.commit()
    session.close()
    return user

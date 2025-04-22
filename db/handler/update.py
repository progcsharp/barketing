from db import make_session, Message, Link, User, Tariff


def update_message(slug, new_message):
    session = make_session()
    message = session.query(Message).filter(Message.slug == slug).first()
    if not message:
        raise ValueError(f"Сообщение с slug '{slug}' не найдено")

    message.message = new_message
    session.commit()
    session.close()
    return message


def update_link(tg_id, url):
    session = make_session()
    link = session.query(Link).filter(Link.url == url).first()
    user = session.query(User).filter(User.tg_id == tg_id).first()
    user.referal = url
    link.count += 1
    session.commit()
    session.close()
    return link


def update_link_pay_count(tg_id, tariff_name):
    session = make_session()
    user = session.query(User).filter(User.tg_id == tg_id).first()
    if user.referal is not None:
        link = session.query(Link).filter(Link.url == user.referal).first()
        tariff = session.query(Tariff).filter(Tariff.tariff_name == tariff_name).first()
        print(tariff.price)
        link.pay_count += int(tariff.price)
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


async def update_tariff_price(tariff_name, new_price):
    session = make_session()
    tariff = session.query(Tariff).filter(Tariff.tariff_name == tariff_name).first()
    tariff.price = new_price
    session.commit()
    session.close()
    return tariff

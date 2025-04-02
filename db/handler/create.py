from db import make_session, User, Link


async def create_user(tg_id, nickname):
    session = make_session()
    user = User(tg_id=tg_id, nickname=nickname)
    session.add(user)
    session.commit()
    session.close()
    return True


async def create_link(url, name):
    session = make_session()
    link = Link(url=url, name=name)
    session.add(link)
    session.commit()
    session.close()

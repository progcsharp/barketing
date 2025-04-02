from db import make_session, Link


async def delete_link(link_id):
    session = make_session()
    link = session.query(Link).filter(Link.id == link_id).first()
    session.delete(link)
    session.commit()
    session.close()
    return link

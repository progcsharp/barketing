from sqlalchemy import create_engine

from config import BD


def engine() -> object:
    print("[0] Generate engine (lazy)...")
    _engine = create_engine(BD, echo=True)
    print("[!] Generated, ready to pending!")
    return _engine

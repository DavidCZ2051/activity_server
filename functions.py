import random as rand
from globals import *


def get_new_id(things: list, type: IdType) -> int or None:
    limit: int = id_limits[type]

    new_id: int = rand.randint(0, limit - 1)

    if len(things) >= limit:
        return None

    for thing in things:
        if thing.id == new_id:
            return get_new_id(things, type)

    return new_id


def session_exists(session_id: int, sessions: list) -> bool:
    for session in sessions:
        if session.id == session_id:
            return True
    return False


def get_session(session_id: int, sessions: list) -> Session:
    for session in sessions:
        if session.id == session_id:
            return session
    return None


def session_is_full(session_id: int, sessions: list) -> bool:
    session: Session = get_session(session_id=session_id, sessions=sessions)

    return session.get_total_player_count() >= PLAYER_SESSION_LIMIT

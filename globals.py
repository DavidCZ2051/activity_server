from typing import List
from classes import *

SERVER_VERSION: str = "0.0.1"
DEBUG: bool = True
PORT: int = 8000

SESSION_LIMIT: int = 10
PLAYER_SESSION_LIMIT: int = 6
TEAM_SESSION_LIMIT: int = 3
PLAYER_TEAM_LIMIT: int = 2

sessions: List[Session] = []

id_limits: dict = {
    IdType.SESSION: SESSION_LIMIT,
    IdType.PLAYER: PLAYER_SESSION_LIMIT,
    IdType.TEAM: TEAM_SESSION_LIMIT,
}

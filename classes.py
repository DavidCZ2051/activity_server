from enum import Enum


class IdType(Enum):
    SESSION = 1
    PLAYER = 2
    TEAM = 3


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3
    YELLOW = 4
    ORANGE = 5
    PURPLE = 6


class Player:
    id: int
    nickname: str
    # only for players without a team
    points: int or None
    color: Color or None

    def __init__(self, id: int, nickname: str) -> None:
        self.id = id
        self.nickname = nickname

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nickname": self.nickname,
            "points": self.points,
            "color": self.color,
        }


class Team:
    id: int
    players: list
    color: Color
    points: int

    def __init__(self, id: int) -> None:
        self.id = id
        self.points = 0
        self.players = []


class Session:
    id: int
    settings: dict
    players: list
    unassigned_players: list
    teams: list

    def __init__(self, id: int) -> None:
        self.id = id
        self.teams = []
        self.players = []
        self.unassigned_players = []
        self.settings = {
            "pantomime": True,
            "speaking": True,
            "drawing": True,
        }

    def get_team(self, team_id: int) -> Team or None:
        for team in self.teams:
            if team.id == team_id:
                return team
        return None

    def get_total_player_count(self) -> int:
        return len(self.all_players())

    def all_players(self) -> list:
        all_players: list = []
        for team in self.teams:
            all_players += team.players
        all_players += self.unassigned_players
        all_players += self.players
        return all_players

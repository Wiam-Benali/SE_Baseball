from dataclasses import dataclass

@dataclass
class Team:
    team_code: str
    name: str

    def __hash__(self):
        return hash(self.team_code)
import random
import json
from Team import Team
from Athlete import Athlete
from Sport import Sport
class Game:
    def __init__(self, A:Team, B:Team):
        self.team_a = (A, "local")
        self.team_b = (B, "visitor")
        self.score = {
            A.name: 0, B.name: 0
        }
    def set_team_a(self, team: Team, role: str):
        if isinstance(team, Team):
            if role == "local":
                self.team_a = team
            elif role == "visitor":
                self.team_b = team
            else:
                raise ValueError("Role must be 'local' or 'visitor'")
        else:
            raise ValueError("Team must be an instance of the Team class")
    def play(self):
        self.score[self.team_a.name] = random.randint(0, Sport.max_score[self.team_a.sport.name])
        self.score[self.team_b.name] = random.randint(0, Sport.max_score[self.team_b.sport.name])
    def __str__(self):
        return f"{self.team_a.name} vs {self.team_b.name} - Score: {self.score[self.team_a.name]}:{self.score[self.team_b.name]}"
    def __repr__(self):
        return f"Game(team_a={repr(self.team_a)}, team_b={repr(self.team_b)}, score={repr(self.score)})"
    def to_json(self):
        return {
            "team_a": self.team_a.to_json(),
            "team_b": self.team_b.to_json(),
            "score": self.score
        }
     
def a_game():
    players_mex = ['Chicharito', 'Hugo Sánchez', 'Cuauhtémoc Blanco', 'Rafa Márquez', 'Javier Hernández']
    players_arg = ['Lionel Messi', 'Diego Maradona', 'Gabriel Batistuta', 'Juan Román Riquelme', 'Ángel Di María']
    sport = Sport("Futbol", 11, "FIFA")
    team_mex = Team("Mexico", sport)
    team_arg = Team("Argentina", sport)
    for player in players_mex:
        team_mex.add_athlete(Athlete(player))
    game = Game(team_mex, team_arg)
    game_string = game.to_json()
    return game_string

def save_game(game: Game, filename):
    with open(filename, 'w') as f:
        json.dump(game.to_json(), f, indent=4)
if __name__ == "__main__":
    string_game = a_game()
    save_game_to_json(string_game, "game.json")
import random
import json
from Game import Game
from Team import Team
from Sport import Sport
from Athlete import Athlete

class Tournament:
    """ Tournament class represents a tournament. It has a name, a list of games, and a list of teams. """

    def __init__(self, name):
        """ Custom constructor for Tournament class. """
        self.name = name
        self.games = []
        self.teams = []

    def add_team(self, team):
        """ Add a team to the tournament. """
        if isinstance(team, Team):
            self.teams.append(team)
        else:
            raise ValueError("Only Team objects can be added to the tournament.")

    def add_game(self, game):
        """ Add a game to the tournament. """
        if isinstance(game, Game):
            self.games.append(game)
        else:
            raise ValueError("Only Game objects can be added to the tournament.")

    def __str__(self):
        """ String representation of the Tournament class. """
        return f"Tournament: {self.name} - Teams: {len(self.teams)} - Games: {len(self.games)}"

    def __repr__(self):
        """ String representation of the Tournament class. """
        return f"Tournament(name={self.name}, teams={len(self.teams)}, games={len(self.games)})"

    def to_json(self):
        """ Convert the Tournament object to a JSON string. """
        return {
            "name": self.name,
            "teams": [team.to_json() for team in self.teams],
            "games": [game.to_json() for game in self.games]
        }
    
    def load_json(self, filename):
        """ Load a Tournament object from a JSON file. """
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for team_data in data["teams"]:
            team = Team(team_data["name"], team_data["sport"])
            players = team_data["athletes"]
            for player in players:
                team.add_athlete(Athlete(player))
            self.add_team(team)
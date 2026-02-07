class Sport:
    def __init__(self, name, num_players, league):
        self.name = name
        self.league = league
        self.num_players = num_players
    def __str__(self):
        return f"{self.name}({self.league}) - {self.num_players} players"
    def __repr__(self):
        return f"Sport(name={self.name}, league={self.league}), players={self.num_players})" 
    def to_json(self):
        return {
            "name": self.name,
            "league": self.league,
            "num_players": self.num_players
        }
    
if __name__ == "__main__":
    sport = Sport("Basketball", 10, "NBA")
    print(sport)
    print(sport.to_json())
    print(repr(sport))
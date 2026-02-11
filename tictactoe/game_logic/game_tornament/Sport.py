class Sport:
    max_score = {
            "Futbol": 5,
            "Basketball": 130,
            "Futbol Americano": 60,
            "Baseball": 20,
            "Hockey": 10
        }
    def __init__(self, name, num_players, league):
        self.name = name
        self.league = league
        self.num_players = num_players
    def add_name(self, name):
        if name in self.max_score:
            self.name = name
        else:            
            raise ValueError(f"Sport name must be one of {list(self.max_score.keys())}") 
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
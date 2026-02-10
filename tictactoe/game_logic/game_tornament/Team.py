from Athlete import Athlete
from Sport import Sport

class Team:
    def __init__(self, name, sport:Sport):
        self.name = name
        self.set_sport(sport)
        self.athletes = []
    def set_sport(self, sport):
        if isinstance(sport, Sport):
            self.sport = sport
        else:
            raise ValueError("Sport must be an instance of the Sport class")
    def add_athlete(self, athlete):
        if isinstance(athlete, Athlete):
            self.athletes.append(athlete)
        else:
            raise ValueError("Only Athlete instances can be added to the team")
    def __str__(self):
        return f"{self.name} - {self.sport.name} ({len(self.athletes)} athletes)"
    def __repr__(self):
        return f"Team(name={self.name}, sport={repr(self.sport)})"
    def to_json(self):
        return {
            "name": self.name,
            "sport": self.sport.to_json(),
            "athletes": [athlete.to_json() for athlete in self.athletes]
        } 

if __name__ == "__main__":
    a = Athlete("Lionel Messi")
    b = Athlete("Diego Maradona")
    s = Sport("Futbol",11,"FIFA")
    argentina = Team("Argentina", s)
    argentina.add_athlete(a)
    argentina.add_athlete(b)
    print(argentina)
    print(repr(argentina))
    print(argentina.to_json())
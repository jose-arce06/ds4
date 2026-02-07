from Athlete import Athlete
from Sport import Sport

class Team:
    def __init__(self, name, sport:Sport):
        self.name = name
        self.sport = sport
        self.athletes = []
    def add_athlete(self, athlete):
        if isinstance(athlete, Athlete):
            self.athletes.append(athlete)
        else:
            raise ValueError("Only Athlete instances can be added to the team")
        
if __name__ == "__main__":
    basketball = Sport("Basketball", 10, "NBA")
    team = Team("Lakers", basketball)
    athlete1 = Athlete("LeBron James")
    athlete1.set_number(23)
    team.add_athlete(athlete1)
    print(team.name)
    print(team.sport)
    print(team.athletes)
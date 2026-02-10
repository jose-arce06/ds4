class Athlete:
    """
    Docstring for Athlete
    """
    def __init__(self, name):
        """ Custom constructor for Athlete class"""
        self.name = name
        self.number=0

    def __str__(self):
        """
        String representation of Athlete
        """        
        return f"Athlete: {self.name}, Number: {self.number}"
    def __repr__(self):
        """"""
        return f"Athlete(name={self.name}, number={self.number})"
    def set_number(self, number):
        """ Set the athlete's number
        """
        self.number = number
    def to_json(self):
        return {
            "name": self.name,
            "number": self.number
        }
    
if __name__ == "__main__":
    athlete1 = Athlete("Lionel Messi")
    athlete1.number = 10
    print(athlete1)
    print(repr(athlete1))
    
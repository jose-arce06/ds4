"""
Tic Tac Toe Game
Author: Jose Arce
"""
from game_logic import game

def main():
    """
    Main function to start the game
    """
    playing = True
    scores = {'X': 0, 'O': 0, 'Ties': 0}
    while playing:
        winner = game()
        if len(winner) > 0:
            print(f"Winner: Player {winner}")
        else:
            print("It's a tie!")
            winner = 'Ties'
        scores[winner] += 1
        replay = input("Do you want to play again? (y/n): ").strip().lower()
        if replay != 'y':
            playing = False
        print(f"Score: x = {scores['X']}, O = {scores['O']}, Ties = {scores['Ties']}")

if __name__ == "__main__":
    main()
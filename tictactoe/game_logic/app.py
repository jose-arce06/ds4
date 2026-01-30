"""
Tic Tac Toe Game
Author: Jose Arce
"""
from game_logic import game
from game_logic import two_players
from menu import display_menu

def main():
    """
    Main function to run the Tic Tac Toe game
    """
    while True:
        choice = display_menu()
        if choice == 1:
            print("One player game is not implemented yet.")
            # Here you can implement the one player game logic
        elif choice == 2:
            two_players()
        elif choice == 3:
            print("Exiting the game. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main()
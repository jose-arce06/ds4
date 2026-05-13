"""
Docstring for menu
"""

def display_menu()-> int:
    """
    Displays the main menu and returns the user's choice as an integer.
    """
    print("Welcome to Tic Tac Toe!")
    print("1. one player game")
    print("2. two player game")
    print("3. exit")
    choice = input("please select an opcion (1-3): ")
    return int(choice)

if __name__ == "__main__":
    display_menu()
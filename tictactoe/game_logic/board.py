"""
Docstring for tictactoe.game_logic.board
Author: jose arce
"""

def display_board(dboard:dict)->None:
    """
    Docstring for display_board
    """
    d= dboard
    print(f"{dboard[0]}|{dboard[1]}|{dboard[2]}")
    print("-+-+-")
    print(f"{dboard[3]}|{dboard[4]}|{dboard[5]}")
    print("-+-+-")
    print(f"{dboard[6]}|{dboard[7]}|{dboard[8]}")


# Example usage
if __name__ == "__main__":
    board = {x:str(x) for x in range(9)}
    display_board(board)
    board[0] = 'X'
    board[4] = 'O'
    display_board(board)   
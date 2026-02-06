"""
Docstring for tictactoe.game_logic.board
Author: Jose Arce
"""

def display_board(dboard:dict)->None:
    """
    Display game board of Tictactoe
    """
    d= dboard
    print(f"{dboard[0]}|{dboard[1]}|{dboard[2]}")
    print("-+-+-")
    print(f"{dboard[3]}|{dboard[4]}|{dboard[5]}")
    print("-+-+-")
    print(f"{dboard[6]}|{dboard[7]}|{dboard[8]}")

def player_turn(player:str, dboard:dict)->bool:
    """
    Ask player for their turn
    """
    valid_move = False
    user_input = input(f"Player {player}, enter your move (0-8): ")
    user_input = int(user_input)
    print(f"value entered: {user_input} type: {type(user_input)}")
    if user_input in dboard.keys():
        if dboard[user_input] not in ['X', 'O']:
            dboard[user_input] = player
            valid_move = True
        else:
            print("Invalid move! cell already occupied.")
    else:
        print("Invalid move! cell ")
    return valid_move

if __name__ == "__main__":
    board = {x:str(x) for x in range(9)}
    display_board(board)
    move =player_turn('X', board,)
    print(f"Move valid: {move}")
    display_board(board)  

    move =player_turn('O', board,)
    print(f"Move valid: {move}")
    display_board(board) 
    print(board)
     
    # board[0] = 'X'
    # board[4] = 'O'
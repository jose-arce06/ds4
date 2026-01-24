"""

"""
import board

def check_winner(d:dict, combo_list:list)->bool:
    """
    Check if there is a winner
    """
    for combo in combo_list:
        if d[combo[0]] == d[combo[1]] == d[combo[2]]:
            return True
    return False
def game():
    """
    Here lives the main game logic
    """
    turn = 0
    dboard = {x:str(x) for x in range(9)}
    combo_list = [
        [0,1,2], [3,4,5], [6,7,8], # rows
        [0,3,6], [1,4,7], [2,5,8], # columns
        [0,4,8], [2,4,6]           # diagonals
    ]
    x_players = 'X'
    o_players = 'O'
    current_player = x_players
    while turn < 9:
        board.display_board(dboard)
        valid_move = False
        while not valid_move:
            valid_move = board.player_turn(current_player, dboard)
        turn += 1
        if current_player == x_players:
            current_player = o_players
        else:
            current_player = x_players

if __name__ == "__main__":
    game()

"""

"""
import board

def game():
    """
    Here lives the main game logic
    """
    turn = 0
    dboard = {x:str(x) for x in range(9)}
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

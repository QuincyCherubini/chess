import MCTS
import cProfile
from board import Game


def run():
    new_game = Game()
    new_game.position.display_position("W")

    while True:

        if new_game.curr_player == "W":

            # get the move
            curr_col = input_number("Enter curr_col: ")
            if curr_col == 99:
                break
            curr_row = input_number("Enter curr_row: ")
            next_col = input_number("Enter next_col: ")
            next_row = input_number("Enter next_row: ")

            new_game.move(curr_col, curr_row, next_col, next_row)

            # new_game.move(4, 1, 4, 3)

        # us the MCTS for black's move
        else:
            move = MCTS.run(2, 30, new_game)
            new_game.move(move.from_x, move.from_y, move.to_x, move.to_y)

        new_game.position.display_position("W")

        if new_game.game_is_over():
            break


def input_number(message):

    while True:
        try:
            userInput = int(input(message))
        except ValueError:
            print("Please enter an integer.")
            continue

        return userInput


if __name__ == "__main__":
    pr = cProfile.Profile()
    pr.enable()
    run()
    pr.disable()
    pr.print_stats()

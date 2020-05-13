from board import Game


def run():
    new_game = Game()
    new_game.position.display_position("W")

    while True:

        # get the move
        curr_col = input_number("Enter curr_col: ")
        if curr_col == 99:
            break
        curr_row = input_number("Enter curr_row: ")
        next_col = input_number("Enter next_col: ")
        next_row = input_number("Enter next_row: ")

        new_game.move(curr_col, curr_row, next_col, next_row)
        new_game.position.display_position("W")

        # test FEN
        print("FEN list: {}".format(new_game.position_history))

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
    run()

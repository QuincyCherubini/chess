from board import board


def run():
    new_board = board()
    new_board.display_board("W")

    while True:

        # todo: test to make sure ints
        # get the move
        curr_col = inputNumber("Enter curr_col: ")
        if curr_col == 99:
            break
        curr_row = inputNumber("Enter curr_row: ")
        next_col = inputNumber("Enter next_col: ")
        next_row = inputNumber("Enter next_row: ")

        new_board.move(curr_col, curr_row, next_col, next_row)
        new_board.display_board("W")


def inputNumber(message):

    while True:
        try:
            userInput = int(input(message))
        except ValueError:
            print("Please enter an integer.")
            continue

        return userInput


if __name__ == "__main__":
    run()

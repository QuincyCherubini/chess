class Piece:

    # colour = {W, B)
    # name = {p, N, B, R, Q, K}
    def __init__(self, colour, name):
        self.colour = colour
        self.name = name

    def get_colour(self):
        return self.colour

    def get_name(self):
        return self.name


# defines the move from one location to another
class Move:

    def __init__(self, from_x, from_y, to_x, to_y, position, curr_player):
        self.from_x = from_x
        self.from_y = from_y
        self.to_x = to_x
        self.to_y = to_y
        self.position = position
        self.curr_player = curr_player

        # set a variable for the opposing player
        if curr_player == "W":
            self.opp_player = "B"
        else:
            self.opp_player = "W"

        # pieces at the locations
        self.curr_piece = position.locations[from_x][from_y]
        self.next_piece = position.locations[to_x][to_y]

    # curr, next are an array of [row, col]
    # note this is only called after is_legal_move check has been completed
    def execute(self):

        self.position.locations[self.to_x][self.to_y] = self.position.locations[self.from_x][self.from_y]
        self.position.locations[self.from_x][self.from_y] = None

        # todo: currently auto promotes to Queen
        # promote pawn
        if self.curr_piece.colour == "W" and self.curr_piece.name == "p" and self.to_y == 7:
            # new_peice = self.get_pawn_promotion()
            # self.position.locations[self.to_x][self.to_y] = Piece("W", new_peice)
            self.position.locations[self.to_x][self.to_y] = Piece("W", "Q")

        if self.curr_piece.colour == "B" and self.curr_piece.name == "p" and self.to_y == 0:
            # new_peice = self.get_pawn_promotion()
            # self.position.locations[self.to_x][self.to_y] = Piece("B", new_peice)
            self.position.locations[self.to_x][self.to_y] = Piece("B", "Q")

        # en passant
        if self.curr_player == "W" and self.curr_piece.name == "p":
            side_piece = self.position.locations[self.to_x][self.to_y - 1]
            if self.from_y == 4 and self.to_y == 5 and abs(self.to_x - self.from_x) == 1 and side_piece is not None and \
                    side_piece.colour == "B" and side_piece.name == "p" and self.position.B_passant == self.to_x:
                self.position.locations[self.to_x][self.to_y - 1] = None

        elif self.curr_player == "B" and self.curr_piece.name == "p":
            side_piece = self.position.locations[self.to_x][self.to_y + 1]
            if self.from_y == 3 and self.to_y == 2 and abs(self.to_x - self.from_x) == 1 and side_piece is not None and \
                    side_piece.colour == "W" and side_piece.name == "p" and self.position.W_passant == self.to_x:
                self.position.locations[self.to_x][self.to_y + 1] = None

        # move the rook for castling
        if self.curr_piece.name == "K":

            # update the Kings location tracker
            if self.curr_piece.colour == "W":
                self.position.W_King_loc = [self.to_x, self.to_y]
            else:
                self.position.B_King_loc = [self.to_x, self.to_y]

            # white castling short
            if self.from_x == 4 and self.from_y == 0 and self.to_x == 6 and self.to_y == 0:
                self.position.locations[7][0] = None
                self.position.locations[5][0] = Piece("W", "R")
                self.position.W_King_moved = True
                self.position.W_7_Rook_moved = True

            # white castling long
            elif self.from_x == 4 and self.from_y == 0 and self.to_x == 2 and self.to_y == 0:
                self.position.locations[0][0] = None
                self.position.locations[3][0] = Piece("W", "R")
                self.position.W_King_moved = True
                self.position.W_0_Rook_moved = True

            # black castling short
            if self.from_x == 4 and self.from_y == 7 and self.to_x == 6 and self.to_y == 7:
                self.position.locations[7][7] = None
                self.position.locations[5][7] = Piece("B", "R")
                self.position.B_King_moved = True
                self.position.B_7_Rook_moved = True

            # black castling long
            elif self.from_x == 4 and self.from_y == 7 and self.to_x == 2 and self.to_y == 7:
                self.position.locations[0][7] = None
                self.position.locations[3][7] = Piece("B", "R")
                self.position.B_King_moved = True
                self.position.B_0_Rook_moved = True

        # check if the move put the other King is in check here
        if self.curr_player == "W":
            self.position.W_King_check = False
            King_pos = self.position.get_King_loc("B")
            self.position.B_King_check = self.position.is_attacked(King_pos[0], King_pos[1], "W")
        else:
            self.position.B_King_check = False
            King_pos = self.position.get_King_loc("W")
            self.position.W_King_check = self.position.is_attacked(King_pos[0], King_pos[1], "B")

    # test if a move is legal
    def is_legal_move(self):

        # check to make sure both positions are on the position
        if self.from_x < 0 or self.from_x > 7:
            return False
        if self.from_y < 0 or self.from_y > 7:
            return False
        if self.to_x < 0 or self.to_x > 7:
            return False
        if self.to_y < 0 or self.to_y > 7:
            return False

        # check if the piece at the current move is the current players
        if self.curr_piece is None or self.curr_piece.colour != self.curr_player:
            return False

        # check to make sure the next location does not contain a piece of the current player's colour
        # This will also catch trying to move to the current spot
        if self.next_piece is not None and self.next_piece.colour == self.curr_player:
            return False

        # check if the piece moves how it's supposed to
        if self.curr_piece.name == "p":
            # return self.is_legal_pawn_move()
            if not self.is_legal_pawn_move():
                return False

        elif self.curr_piece.name == "B":
            if not self.is_legal_bishop_move():
                return False

        elif self.curr_piece.name == "N":
            if not self.is_legal_knight_move():
                return False

        elif self.curr_piece.name == "R":
            if not self.is_legal_rook_move():
                return False

        elif self.curr_piece.name == "Q":
            if not self.is_legal_queen_move():
                return False

        elif self.curr_piece.name == "K":
            if not self.is_legal_king_move():
                return False

        # this should never happen
        else:
            print("You have passed an invalid piece")
            return False

        if self.King_is_in_check():
            return False
        else:
            return True

    def is_legal_pawn_move(self):

        # white player
        if self.curr_player == "W":

            # reset white passant status
            self.position.W_passant = None

            # moving one piece forward
            if self.from_x == self.to_x and self.to_y - self.from_y == 1 and self.next_piece is None:
                return True

            # move two piece forward
            if self.from_x == self.to_x and self.to_y - self.from_y == 2 and self.next_piece is None and \
                self.from_y == 1 and self.position.locations[self.from_x][2] is None:
                self.position.W_passant = self.from_x
                return True

            # taking out a piece
            if self.to_y - self.from_y == 1 and abs(self.from_x - self.to_x) == 1 and self.next_piece is not None and \
                    self.next_piece.colour == "B":
                return True

            # en passant
            side_piece = self.position.locations[self.to_x][self.to_y - 1]
            if self.from_y == 4 and self.to_y == 5 and abs(self.to_x - self.from_x) == 1 and side_piece is not None and \
                    side_piece.colour == "B" and side_piece.name == "p" and self.position.B_passant == self.to_x:
                return True

            # if it is not one of these moves return False
            return False

        # Black's Turn
        elif self.curr_player == "B":

            # reset white passant status
            self.position.B_passant = None

            # moving one piece forward
            if self.from_x == self.to_x and self.from_y - self.to_y == 1 and self.next_piece is None:
                return True

            # move two piece forward
            if self.from_x == self.to_x and self.from_y - self.to_y == 2 and self.next_piece is None and \
                    self.from_y == 6 and self.position.locations[self.from_x][5] is None:
                self.position.B_passant = self.from_x
                return True

            # taking out a piece
            if self.from_y - self.to_y == 1 and abs(self.from_x - self.to_x) == 1 and self.next_piece is not None and \
                    self.next_piece.colour == "W":
                return True

            # en passant
            side_piece = self.position.locations[self.to_x][self.to_y + 1]
            if self.from_y == 3 and self.to_y == 2 and abs(self.to_x - self.from_x) == 1 and side_piece is not None and \
                    side_piece.colour == "W" and side_piece.name == "p" and self.position.W_passant == self.to_x:
                return True

            # if it is not one of these moves return False
            return False

        # this should never happen
        else:
            print("You have passed an invalid current player")
            return False

    def is_legal_bishop_move(self):

        # if the bishop does not move on a diagonal return False
        if self.from_x - self.from_y != self.to_x - self.to_y and self.from_x + self.from_y != self.to_x + self.to_y:
            return False

        # up and right
        if self.to_x > self.from_x and self.to_y > self.from_y:
            from_x_temp = self.from_x + 1
            from_y_temp = self.from_y + 1
            while from_x_temp < self.to_x:
                if self.position.locations[from_x_temp][from_y_temp] is not None:
                    return False
                from_x_temp += 1
                from_y_temp += 1

        # up and left
        if self.to_x < self.from_x and self.to_y > self.from_y:
            to_x_temp = self.to_x + 1
            from_y_temp = self.from_y + 1
            while to_x_temp < self.to_x:
                if self.position.locations[to_x_temp][from_y_temp] is not None:
                    return False
                to_x_temp += 1
                from_y_temp += 1

        # down and right
        if self.to_x > self.from_x and self.to_y < self.from_y:
            from_x_temp = self.from_x + 1
            to_y_temp = self.to_y + 1
            while from_x_temp < self.to_x:
                if self.position.locations[from_x_temp][to_y_temp] is not None:
                    return False
                from_x_temp += 1
                to_y_temp += 1

        # down and left
        if self.to_x < self.from_x and self.to_y < self.from_y:
            to_x_temp = self.to_x + 1
            to_y_temp = self.from_y + 1
            while to_x_temp < self.to_x:
                if self.position.locations[to_x_temp][to_y_temp] is not None:
                    return False
                to_x_temp += 1
                to_y_temp += 1

        # otherwise return True
        return True

    def is_legal_knight_move(self):

        x_diff = abs(self.from_x - self.to_x)
        y_diff = abs(self.from_y - self.to_y)

        if (x_diff == 1 and y_diff == 2) or (x_diff == 2 and y_diff == 1):
            return True
        else:
            return False

    def is_legal_rook_move(self):

        # rooks have to move along a rank or file
        if self.from_x != self.to_x and self.from_y != self.to_y:
            return False

        # up
        if self.to_y > self.from_y:
            from_y_temp = self.from_y + 1
            while from_y_temp < self.to_y:
                if self.position.locations[self.from_x][from_y_temp] is not None:
                    return False
                from_y_temp += 1

        # down
        elif self.to_y < self.from_y:
            to_y_temp = self.to_y + 1
            while to_y_temp < self.from_y:
                if self.position.locations[self.from_x][to_y_temp] is not None:
                    return False
                to_y_temp += 1

        # left
        elif self.to_x < self.from_x:
            to_x_temp = self.to_x + 1
            while to_x_temp < self.from_x:
                if self.position.locations[to_x_temp][self.from_y] is not None:
                    return False
                to_x_temp += 1

        # right
        elif self.to_x > self.from_x:
            from_x_temp = self.from_x + 1
            while from_x_temp < self.to_x:
                if self.position.locations[from_x_temp][self.from_y] is not None:
                    return False
                from_x_temp += 1

        return True

    def is_legal_queen_move(self):

        if self.is_legal_rook_move():
            return True
        else:
            return self.is_legal_bishop_move()

    def is_legal_king_move(self):

        # regular king move
        x_diff = abs(self.from_x - self.to_x)
        y_diff = abs(self.from_y - self.to_y)

        # check if the King is only moving one square
        if (x_diff == 0 and y_diff == 1) or (x_diff == 1 and y_diff == 0) or (x_diff == 1 and y_diff == 1):
            if self.curr_piece.colour == 'W':
                self.position.W_King_moved = False
            elif self.curr_piece.colour == 'B':
                self.position.B_King_moved = False
            return True

        # white castling short
        if self.from_x == 4 and self.from_y == 0 and self.to_x == 6 and self.to_y == 0:
            # check if King and Rook haven't moved
            if not self.position.W_King_moved and not self.position.W_7_Rook_moved:
                # check if the squares in between are blank (6, 0 is tested by default in legal move check)
                if self.position.locations[5][0] is None:
                    # check to make sure King does not move through check
                    if not self.position.is_attacked(4, 0, "B") and not self.position.is_attacked(5, 0, "B") and \
                            not self.position.is_attacked(6, 0, "B"):
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False

        # white castling long
        elif self.from_x == 4 and self.from_y == 0 and self.to_x == 2 and self.to_y == 0:
            # check if King and Rook haven't moved
            if not self.position.W_King_moved and not self.position.W_0_Rook_moved:
                # check if the squares in between are blank
                if self.position.locations[3][0] is None and self.position.locations[1][0] is None:
                    # check to make sure King does not move through check
                    if not self.position.is_attacked(4, 0, "B") and not self.position.is_attacked(3, 0, "B") and \
                            not self.position.is_attacked(2, 0, "B"):
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False

        # black castling short
        if self.from_x == 4 and self.from_y == 7 and self.to_x == 6 and self.to_y == 7:
            # check if King and Rook haven't moved
            if not self.position.B_King_moved and not self.position.B_0_Rook_moved:
                # check if the squares in between are blank
                if self.position.locations[5][7] is None:
                    # check to make sure King does not move through check
                    if not self.position.is_attacked(4, 7, "W") and not self.position.is_attacked(5, 7, "W") and \
                            not self.position.is_attacked(6, 7, "W"):
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False

        # black castling long
        elif self.from_x == 4 and self.from_y == 7 and self.to_x == 2 and self.to_y == 7:
            # check if King and Rook haven't moved
            if not self.position.B_King_moved and not self.position.B_0_Rook_moved:
                # check if the squares in between are blank
                if self.position.locations[3][7] is None and self.position.locations[1][7] is None:
                    # check to make sure King does not move through check
                    if not self.position.is_attacked(4, 7, "W") and not self.position.is_attacked(3, 7, "W") and \
                            not self.position.is_attacked(2, 7, "W"):
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False

        # if none of these criteria are met return False
        return False

    # only do this if the piece moving is on the same rank, file, or diagonal as the King or if the King is in check
    # check if King would be in check
    # alter the game board to be the new position and then change it back
    def King_is_in_check(self):

        if self.curr_piece.name == "K":
            King_pos = [self.to_x, self.to_y]
        else:
            King_pos = self.position.get_King_loc(self.curr_player)

        if self.curr_player == "W":
            King_check = self.position.W_King_check
        else:
            King_check = self.position.B_King_check

        # do a full check if King is in check or the King has moved
        if self.curr_piece.name == "K" or King_check:

            # store the two important pieces
            new_loc_piece = self.position.locations[self.to_x][self.to_y]
            orig_loc_piece = self.position.locations[self.from_x][self.from_y]

            # update the board to the new potential position
            self.position.locations[self.from_x][self.from_y] = None
            self.position.locations[self.to_x][self.to_y] = orig_loc_piece

            # If the King would be under attack return False
            if self.position.is_attacked(King_pos[0], King_pos[1], self.opp_player):
                self.position.locations[self.from_x][self.from_y] = orig_loc_piece
                self.position.locations[self.to_x][self.to_y] = new_loc_piece
                return True
            else:
                self.position.locations[self.from_x][self.from_y] = orig_loc_piece
                self.position.locations[self.to_x][self.to_y] = new_loc_piece
                return False

        # if a piece from the same rank or file has moved only check Rook/Queen checks
        elif self.from_x == King_pos[0] or self.from_y == King_pos[1]:

            # store the two important pieces
            new_loc_piece = self.position.locations[self.to_x][self.to_y]
            orig_loc_piece = self.position.locations[self.from_x][self.from_y]

            # update the board to the new potential position
            self.position.locations[self.from_x][self.from_y] = None
            self.position.locations[self.to_x][self.to_y] = orig_loc_piece

            # If the King would be under attack return False
            if self.position.is_attacked_rook(King_pos[0], King_pos[1], self.opp_player):
                self.position.locations[self.from_x][self.from_y] = orig_loc_piece
                self.position.locations[self.to_x][self.to_y] = new_loc_piece
                return True
            else:
                self.position.locations[self.from_x][self.from_y] = orig_loc_piece
                self.position.locations[self.to_x][self.to_y] = new_loc_piece
                return False

        # if a piece is moved on the same diagonal only check for bishop attack
        elif self.from_x + self.from_y == King_pos[0] + King_pos[1] or self.from_x - self.from_y == King_pos[0] - \
                King_pos[1]:

            # store the two important pieces
            new_loc_piece = self.position.locations[self.to_x][self.to_y]
            orig_loc_piece = self.position.locations[self.from_x][self.from_y]

            # update the board to the new potential position
            self.position.locations[self.from_x][self.from_y] = None
            self.position.locations[self.to_x][self.to_y] = orig_loc_piece

            # If the King would be under attack return False
            if self.position.is_attacked_bishop(King_pos[0], King_pos[1], self.opp_player):
                self.position.locations[self.from_x][self.from_y] = orig_loc_piece
                self.position.locations[self.to_x][self.to_y] = new_loc_piece
                return True
            else:
                self.position.locations[self.from_x][self.from_y] = orig_loc_piece
                self.position.locations[self.to_x][self.to_y] = new_loc_piece
                return False

        else:
            return False

    # get user input for what piece to promote a pawn to
    def get_pawn_promotion(self):

        while True:
            userInput = input("Pick a piece to promote pawn to: ")

            if userInput in ["Q", "R", "B", "N"]:
                return userInput
            else:
                print("Please enter a valid piece")

    def print_move(self):
        print("From [{}, {}] to [{}, {}]".format(self.from_x, self.from_y, self.to_x, self.to_y))

    def move_to_str(self):
        move_string = "From [" + str(self.from_x) + " , " + str(self.from_y) + "] to [" + str(self.to_x) +\
                      ", " + str(self.to_y) + "]"
        return move_string


class Position:

    # first element is row, second is column
    # 0=a, 1=b, ... 7=h
    def __init__(self):
        self.locations = [[None for _ in [0, 1, 2, 3, 4, 5, 6, 7]] for _ in [0, 1, 2, 3, 4, 5, 6, 7]]

        # track the conditions for castling
        self.W_King_moved = False
        self.W_0_Rook_moved = False
        self.W_7_Rook_moved = False
        self.B_King_moved = False
        self.B_0_Rook_moved = False
        self.B_7_Rook_moved = False

        # track which coloumns are currently available to en passant
        self.W_passant = None
        self.B_passant = None

        # set the white pieces
        self.locations[0][1] = Piece("W", "p")
        self.locations[1][1] = Piece("W", "p")
        self.locations[2][1] = Piece("W", "p")
        self.locations[3][1] = Piece("W", "p")
        self.locations[4][1] = Piece("W", "p")
        self.locations[5][1] = Piece("W", "p")
        self.locations[6][1] = Piece("W", "p")
        self.locations[7][1] = Piece("W", "p")
        self.locations[0][0] = Piece("W", "R")
        self.locations[1][0] = Piece("W", "N")
        self.locations[2][0] = Piece("W", "B")
        self.locations[3][0] = Piece("W", "Q")
        self.locations[4][0] = Piece("W", "K")
        self.locations[5][0] = Piece("W", "B")
        self.locations[6][0] = Piece("W", "N")
        self.locations[7][0] = Piece("W", "R")

        # set the black pieces
        self.locations[0][6] = Piece("B", "p")
        self.locations[1][6] = Piece("B", "p")
        self.locations[2][6] = Piece("B", "p")
        self.locations[3][6] = Piece("B", "p")
        self.locations[4][6] = Piece("B", "p")
        self.locations[5][6] = Piece("B", "p")
        self.locations[6][6] = Piece("B", "p")
        self.locations[7][6] = Piece("B", "p")
        self.locations[0][7] = Piece("B", "R")
        self.locations[1][7] = Piece("B", "N")
        self.locations[2][7] = Piece("B", "B")
        self.locations[3][7] = Piece("B", "Q")
        self.locations[4][7] = Piece("B", "K")
        self.locations[5][7] = Piece("B", "B")
        self.locations[6][7] = Piece("B", "N")
        self.locations[7][7] = Piece("B", "R")

        # track some elements to make calculations easier
        self.W_King_loc = [4, 0]
        self.B_King_loc = [4, 7]
        self.W_King_check = False
        self.B_King_check = False

    def display_position(self, player):

        if player == "W":
            print("  -----------------------------------------")
            for row in [7, 6, 5, 4, 3, 2, 1, 0]:
                row_string = str(row) + " |"
                for col in [0, 1, 2, 3, 4, 5, 6, 7]:
                    if self.locations[col][row] is None:
                        row_string = row_string + "    |"
                    else:
                        piece = self.locations[col][row]
                        row_string = row_string + " " + piece.colour + piece.name + " |"
                print(row_string)
                print("  -----------------------------------------")
            print("    0    1    2    3    4    5    6    7")

        elif player == "B":
            print("-----------------------------------------")
            for row in [0, 1, 2, 3, 4, 5, 6, 7]:
                row_string = str(row) + " |"
                for col in [7, 6, 5, 4, 3, 2, 1, 0]:
                    if self.locations[col][row] is None:
                        row_string = row_string + "    |"
                    else:
                        piece = self.locations[col][row]
                        row_string = row_string + " " + piece.colour + piece.name + " |"
                print(row_string)
                print("-----------------------------------------")

        else:
            print("display_position error: please pass a valid player value")

    # check if a give position is being attacked by attacking_colour
    def is_attacked(self, x_pos, y_pos, attacking_colour):

        if self.is_attacked_pawn(x_pos, y_pos, attacking_colour):
            return True

        # check 8 possible knight squares (if valid positions)
        if self.is_attacked_knight(x_pos, y_pos, attacking_colour):
            return True

        # check vertically for the first piece, return true if it is a R or Q of attacking_colour
        if self.is_attacked_bishop(x_pos, y_pos, attacking_colour):
            return True

        # check horizontally for the first piece, return true if it is a R or Q of attacking_colour
        if self.is_attacked_rook(x_pos, y_pos, attacking_colour):
            return True

        # check diagonally for the first piece, return true if it is a B or Q of attacking_colour
        if self.is_attacked_King(x_pos, y_pos, attacking_colour):
            return True

        return False

    # check if a location is attacked by a pawn
    def is_attacked_pawn(self, x_pos, y_pos, attacking_colour):

        # check below for white pawns or above for black pawns
        if attacking_colour == "B":
            new_y = y_pos + 1
        else:
            new_y = y_pos - 1

        if 0 <= new_y <= 7:
            # check each pawn location
            for i in [-1, 1]:
                if 0 <= x_pos + i <= 7:
                    pawn = self.locations[x_pos + i][new_y]
                    if pawn is not None and pawn.colour == attacking_colour and pawn.name == "p":
                        return True

        # if now pawn is attacking the spot return False
        return False

    # check if a location is attacked by a knight
    def is_attacked_knight(self, x_pos, y_pos, attacking_colour):

        for x in [-1, 1]:
            if 0 <= x_pos + x <= 7:
                for y in [-2, 2]:
                    if 0 <= y_pos + y <= 7:
                        knight = self.locations[x_pos + x][y_pos + y]
                        if knight is not None and knight.colour == attacking_colour and knight.name == "N":
                            return True

        for x in [-2, 2]:
            if 0 <= x_pos + x <= 7:
                for y in [-1, 1]:
                    if 0 <= y_pos + y <= 7:
                        knight = self.locations[x_pos + x][y_pos + y]
                        if knight is not None and knight.colour == attacking_colour and knight.name == "N":
                            return True

        # if no knights are attacking return False
        return False

    # check if a location is attacked by a bishop or Queen
    def is_attacked_bishop(self, x_pos, y_pos, attacking_colour):

        # top right for loop
        temp_x = x_pos + 1
        temp_y = y_pos + 1
        while temp_y < 8 and temp_x < 8:
            temp_piece = self.locations[temp_x][temp_y]
            if temp_piece is not None:
                if (temp_piece.name == "B" or temp_piece.name == "Q") and temp_piece.colour == attacking_colour:
                    return True
                else:
                    break
            temp_y += 1
            temp_x += 1

        # find the first piece on each diagonal from the initial location
        # to top right
        temp_x = x_pos + 1
        temp_y = y_pos + 1
        while temp_y < 8 and temp_x < 8:
            temp_piece = self.locations[temp_x][temp_y]
            if temp_piece is not None:
                if (temp_piece.name == "B" or temp_piece.name == "Q") and temp_piece.colour == attacking_colour:
                    return True
                else:
                    break
            temp_y += 1
            temp_x += 1

        # to top left
        temp_x = x_pos - 1
        temp_y = y_pos + 1
        while temp_y < 8 and temp_x >= 0:
            temp_piece = self.locations[temp_x][temp_y]
            if temp_piece is not None:
                if (temp_piece.name == "B" or temp_piece.name == "Q") and temp_piece.colour == attacking_colour:
                    return True
                else:
                    break
            temp_y += 1
            temp_x -= 1

        # bottom right
        temp_x = x_pos + 1
        temp_y = y_pos - 1
        while temp_y >= 0 and temp_x < 8:
            temp_piece = self.locations[temp_x][temp_y]
            if temp_piece is not None:
                if (temp_piece.name == "B" or temp_piece.name == "Q") and temp_piece.colour == attacking_colour:
                    return True
                else:
                    break
            temp_y -= 1
            temp_x += 1

        # bottom left
        temp_x = x_pos - 1
        temp_y = y_pos - 1
        while temp_y >= 0 and temp_x >= 0:
            temp_piece = self.locations[temp_x][temp_y]
            if temp_piece is not None:
                if (temp_piece.name == "B" or temp_piece.name == "Q") and temp_piece.colour == attacking_colour:
                    return True
                else:
                    break
            temp_y -= 1
            temp_x -= 1

        # if no diagonally is attacking return False
        return False

    # check if a location is attacked by a rook or Queen
    def is_attacked_rook(self, x_pos, y_pos, attacking_colour):

        # find the first piece on each rank or file from the initial location
        # right
        temp_x = x_pos + 1
        while temp_x < 8:
            temp_piece = self.locations[temp_x][y_pos]
            if temp_piece is not None:
                if temp_piece.colour == attacking_colour and (temp_piece.name == "R" or temp_piece.name == "Q"):
                    return True
                else:
                    break
            temp_x += 1

        # left
        temp_x = x_pos - 1
        while temp_x >= 0:
            temp_piece = self.locations[temp_x][y_pos]
            if temp_piece is not None:
                if temp_piece.colour == attacking_colour and (temp_piece.name == "R" or temp_piece.name == "Q"):
                    return True
                else:
                    break
            temp_x -= 1

        # down
        temp_y = y_pos - 1
        while temp_y >= 0:
            temp_piece = self.locations[x_pos][temp_y]
            if temp_piece is not None:
                if temp_piece.colour == attacking_colour and (temp_piece.name == "R" or temp_piece.name == "Q"):
                    return True
                else:
                    break
            temp_y -= 1

        # up
        temp_y = y_pos + 1
        while temp_y < 8:
            temp_piece = self.locations[x_pos][temp_y]
            if temp_piece is not None:
                if temp_piece.colour == attacking_colour and (temp_piece.name == "R" or temp_piece.name == "Q"):
                    return True
                else:
                    break
            temp_y += 1

        # if no rook or queen is attacking return False
        return False

    # check if a location is attacked by a King
    def is_attacked_King(self, x_pos, y_pos, attacking_colour):

        # check the surrounding 8 squares for a king of the attacking colour
        for x in [-1, 0, 1]:
            if 0 <= x_pos + x <= 7:
                for y in [-1, 0, 1]:
                    if 0 <= y_pos + y <= 7:
                        king = self.locations[x_pos + x][y_pos + y]
                        if king is not None and king.colour == attacking_colour and king.name == "K":
                            return True

        # if none of the surrounding pieces contain a King return False
        return False

    def get_King_loc(self, King_colour):

        if King_colour == "W":
            return self.W_King_loc
        else:
            return self.B_King_loc


class Game:

    def __init__(self):

        self.position = Position()  # set up a new position on game start
        self.drawing_moves = 0  # resets on a pawn move or piece capture, if this number reaches 50 the game is a draw
        self.curr_player = "W"
        self.opp_player = "B"

        fen_converter = FEN_converter(self.position, self.curr_player)
        fen = fen_converter.convert_to_FEN()
        self.position_history = [fen]  # this will log all of the positions then check if the same has been reached 3 times

    # executes a move
    def move(self, from_x, from_y, to_x, to_y):

        my_move = Move(from_x, from_y, to_x, to_y, self.position, self.curr_player)

        from_piece = self.position.locations[from_x][from_y]
        to_piece = self.position.locations[to_x][to_y]

        my_move.execute()

        # check if the move is a pawn move or a capture, if so reset self.drawing_moves
        if from_piece.name == "p":
            self.drawing_moves = 0
        elif to_piece is not None:
            self.drawing_moves = 0
        # up the count after blacks turn
        elif from_piece.colour == "B":
            self.drawing_moves += 1

        if self.curr_player == "W":
            self.curr_player = "B"
            self.opp_player = "W"
        else:
            self.curr_player = "W"
            self.opp_player = "B"

        # add the new position to the list of positions
        fen_converter = FEN_converter(self.position, self.curr_player)
        fen = fen_converter.convert_to_FEN()
        self.position_history.append(fen)

    def game_is_over(self):

        if self.is_checkmated(self.curr_player):
            print("{} Wins!".format(self.opp_player))
            return True

        if self.is_stalemate(self.curr_player):
            print("Stalemate!")
            return True

        if self.is_repeated_position():
            print("Draw by repeated position!")
            return True

        if self.is_50_moves():
            print("Draw, 50 moves without capture or pawn move")
            return True

        if self.is_insufficient_material():
            print("Draw by insufficient material!")
            return True

        return False

    # this is for use in the MCTS
    # todo: add wins based on material advantage
    def get_game_result_MCTS(self):

        # a player is in checkmate
        if self.is_checkmated(self.curr_player):
            return self.opp_player

        # Stalemate
        if self.is_stalemate(self.curr_player):
            return "D"

        # Draw, 50 moves without capture or pawn move
        if self.is_50_moves():
            return "D"

        # Draw by insufficient material
        if self.is_insufficient_material():
            return "D"

        if self.winning_material():
            return self.curr_player

        return None

    # test if the player player_colour is checkmated
    def is_checkmated(self, player_colour):

        # check to see if there is a legal move, if there is it's not checkmate
        if self.has_legal_move():
            return False

        # if the King is attacked it is checkmate

        if player_colour == "B":
            attacking_colour = "W"
        else:
            attacking_colour = "B"

        King_pos = self.position.get_King_loc(player_colour)

        # if the King is not attacked return False, it can't be mate
        return self.position.is_attacked(King_pos[0], King_pos[1], attacking_colour)

    # checks if the player who's turn it is (turn_colour) is in a stalemate
    def is_stalemate(self, player_colour):

        # King must not be attacked
        # King must not be able to move
        # no other pieces of the player may be able to move

       # check if there is a legal move
        if self.has_legal_move():
            # print("There is a legal move")
            return False

        # check if the King is attacked

        if player_colour == "B":
            attacking_colour = "W"
        else:
            attacking_colour = "B"

        King_pos = self.position.get_King_loc(player_colour)

        # if the King is attacked return False
        if self.position.is_attacked(King_pos[0], King_pos[1], attacking_colour):
            return False
        else:
            return True

    # if same position is reached 3 times a player can call a draw
    def is_repeated_position(self):

        # get the current position
        fen_converter = FEN_converter(self.position, self.curr_player)
        fen = fen_converter.convert_to_FEN()

        # check if this position has been reached 3 times
        count = self.position_history.count(fen)

        # should only be 3 or less but have > just in case
        if count >= 3:
            return True

        return False

    # if no piece has been captured or pawn moved in 50 turns a player can claim a draw
    def is_50_moves(self):
        return self.drawing_moves == 50

    # todo: update QvQ scenarios
    # if insuffiencient material for a checkmate by either side the game is a draw
    # the draws are K vs.K, K+B vs. K, K+N vs. K, and K+B vs K+B of same colour
    # I also include pieces where a checkmate cannot be forced with reasonably play to simulate agreeing to a draw
    # these combos are: K+N+N v K, K+R vs. K+R, K+R vs. K+N or K+B, K+B vs K+B of opposite colours, K+N vs K+N
    #
    # K+Q vs K+Q is a draw other than some rare positions will count as a draw for now may update later
    def is_insufficient_material(self):

        # get the pieces for each player
        black_pieces = []
        white_pieces = []
        for x in [0, 1, 2, 3, 4, 5, 6, 7]:
            for y in [0, 1, 2, 3, 4, 5, 6, 7]:
                curr_piece = self.position.locations[x][y]
                if curr_piece is not None:
                    # if any player has a pawn return False, no need to do the whole loop
                    if curr_piece.name == "p":
                        return False
                    if curr_piece.colour == "W":
                        white_pieces.append(curr_piece.name)
                    else:
                        black_pieces.append(curr_piece.name)

        # King vs King
        if len(white_pieces) == 1 and len(black_pieces) == 1:
            return True

        # if one side has 3 or more pieces it is not a draw other than K+N+N vs K
        if len(black_pieces) >= 3 or len(white_pieces) >= 3:
            # check if K+N+N vs K, note all positions of length 1 are just the King
            if len(black_pieces) == 3 and len(white_pieces) == 1:
                if black_pieces.count("N") == 2:
                    return True
            if len(white_pieces) == 3 and len(black_pieces) == 1:
                if white_pieces.count("N") == 2:
                    return True
            return False

        # 1v2
        # Check when black has 1 piece and white has 2
        if len(black_pieces) == 1:
            if white_pieces.count("N") == 1 or white_pieces.count("B") == 1:
                return True
            return False

        # Check when black has 1 piece and white has 2
        if len(white_pieces) == 1:
            if black_pieces.count("N") == 1 or black_pieces.count("B") == 1:
                return True
            return False

        # 2v2
        # check for Q vs. Q
        if black_pieces.count("Q") == 1 and white_pieces.count("Q") == 1:
            return True

        # if one side has a queen return False, the Queen wins
        if black_pieces.count("Q") == 1 or white_pieces.count("Q") == 1:
            return True

        # all other 2 piece vs 2 piece scenarios are draws
        return True

    # winning material
    # may add a function to consider a game won for the MCTS if we reach K vs. K+R, K vs. K+Q, or K vs. K+B+B
    # K+Q vs K+R, K+Q vs. K+B, K+Q vs K+N, K vs. K+N+B or K vs any 3+ peices
    # todo : implement the below
    # if one player has a winning combo and other pieces or pawns it is also a win
    # Assuming the King cannot immediately capture one of these pieces
    def winning_material(self):

        # get the pieces for each player
        curr_pieces = []
        opp_pieces = []
        for x in [0, 1, 2, 3, 4, 5, 6, 7]:
            for y in [0, 1, 2, 3, 4, 5, 6, 7]:
                curr_piece = self.position.locations[x][y]
                if curr_piece is not None:
                    # if opp player has a pawn return False, no need to do the whole loop
                    if curr_piece.name == "p" and curr_piece.colour == self.opp_player:
                        return False
                    if curr_piece.colour == self.curr_player:
                        curr_pieces.append(curr_piece.name)
                    else:
                        opp_pieces.append(curr_piece.name)

        # if the current player only has a king return False
        if len(curr_pieces) == 1:
            return False

        # opponent only has a King
        if len(opp_pieces) == 1:
            if "Q" in curr_pieces:
                return True
            elif "R" in curr_pieces:
                return True
            elif "B" in curr_pieces and "N" in curr_pieces:
                return True
            elif curr_pieces.count("B") >= 2:
                return True
        else:
            return False

        return False

    # todo: Should this be broken up?
    # todo: add promotion
    def get_all_legal_moves(self):

        legal_moves = []

        if self.curr_player == "W":
            king_check = self.position.W_King_check
        else:
            king_check = self.position.B_King_check

        # loop through all locations to find player's pieces
        for x in [0, 1, 2, 3, 4, 5, 6, 7]:
            for y in [0, 1, 2, 3, 4, 5, 6, 7]:
                cur_loc = self.position.locations[x][y]

                if cur_loc is not None and cur_loc.colour == self.curr_player:
                    # Pawn
                    if cur_loc.name == "p":
                        # the y positions of possible next moves, dub_y is for moving 2 spaces on a first move
                        if self.curr_player == "W":
                            next_y = y + 1
                            dub_y = y + 2
                        else:
                            next_y = y - 1
                            dub_y = y - 2

                        # check if pawn can move forward
                        if 0 <= next_y <= 7:
                            new_move = Move(x, y, x, next_y, self.position, self.curr_player)
                            if new_move.is_legal_move():
                                legal_moves.append(new_move)

                            # check if the pawn can capture
                            if 0 <= x - 1 <= 7:
                                new_move = Move(x, y, x - 1, next_y, self.position, self.curr_player)
                                if new_move.is_legal_move():
                                    legal_moves.append(new_move)

                            if 0 <= x + 1 <= 7:
                                new_move = Move(x, y, x + 1, next_y, self.position, self.curr_player)
                                if new_move.is_legal_move():
                                    legal_moves.append(new_move)

                        # check if pawn can move forward 2 steps
                        if 0 <= dub_y <= 7:
                            new_move = Move(x, y, x, dub_y, self.position, self.curr_player)
                            if new_move.is_legal_move():
                                legal_moves.append(new_move)

                    # Knight
                    if cur_loc.name == "N":
                        for new_x in [x-2, x-1, x+1, x+2]:
                            if 0 <= new_x <= 7:
                                for new_y in [y-2, y-1, y+1, y+2]:
                                    if 0 <= new_y <= 7:
                                        new_move = Move(x, y, new_x, new_y, self.position, self.curr_player)
                                        if new_move.is_legal_move():
                                            legal_moves.append(new_move)

                    # Bishop or Queen
                    if cur_loc.name == "B" or cur_loc.name == "Q":

                        # up and left
                        new_x = x + 1
                        new_y = y + 1
                        while new_x <= 7 and new_y <= 7:
                            new_move = Move(x, y, new_x, new_y, self.position, self.curr_player)
                            if new_move.is_legal_move():
                                legal_moves.append(new_move)
                            # if the King is not in check all furter bishop moves are illegal
                            elif not king_check:
                                break
                            new_x += 1
                            new_y += 1

                        # down and left
                        new_x = x + 1
                        new_y = y - 1
                        while new_x <= 7 and new_y >= 0:
                            new_move = Move(x, y, new_x, new_y, self.position, self.curr_player)
                            if new_move.is_legal_move():
                                legal_moves.append(new_move)
                            elif not king_check:
                                break
                            new_x += 1
                            new_y -= 1

                        # up and right
                        new_x = x - 1
                        new_y = y + 1
                        while new_x >= 0 and new_y <= 7:
                            new_move = Move(x, y, new_x, new_y, self.position, self.curr_player)
                            if new_move.is_legal_move():
                                legal_moves.append(new_move)
                            elif not king_check:
                                break
                            new_x -= 1
                            new_y += 1

                        # down and left
                        new_x = x - 1
                        new_y = y - 1
                        while new_x >= 0 and new_y >= 0:
                            new_move = Move(x, y, new_x, new_y, self.position, self.curr_player)
                            if new_move.is_legal_move():
                                legal_moves.append(new_move)
                            elif not king_check:
                                break
                            new_x -= 1
                            new_y -= 1

                    # Rook or Queen
                    if cur_loc.name == "R" or cur_loc.name == "Q":

                        # up
                        new_y = y + 1
                        while new_y <= 7:
                            new_move = Move(x, y, x, new_y, self.position, self.curr_player)
                            if new_move.is_legal_move():
                                legal_moves.append(new_move)
                            elif not king_check:
                                break
                            new_y += 1

                        # down
                        new_y = y - 1
                        while new_y >= 0:
                            new_move = Move(x, y, x, new_y, self.position, self.curr_player)
                            if new_move.is_legal_move():
                                legal_moves.append(new_move)
                            elif not king_check:
                                break
                            new_y -= 1

                        # left
                        new_x = x - 1
                        while new_x >= 0:
                            new_move = Move(x, y, new_x, y, self.position, self.curr_player)
                            if new_move.is_legal_move():
                                legal_moves.append(new_move)
                            elif not king_check:
                                break
                            new_x -= 1

                        # right
                        new_x = x + 1
                        while new_x <= 7:
                            new_move = Move(x, y, new_x, y, self.position, self.curr_player)
                            if new_move.is_legal_move():
                                legal_moves.append(new_move)
                            elif not king_check:
                                break
                            new_x += 1

                    # King
                    if cur_loc.name == "K":

                        # regular King move
                        new_x = x-1
                        while new_x < x + 2:
                            if 0 <= new_x <= 7:
                                new_y = y - 1
                                while new_y < y + 2:
                                    if 0 <= new_y <= 7:
                                        new_move = Move(x, y, new_x, new_y, self.position, self.curr_player)
                                        if new_move.is_legal_move():
                                            legal_moves.append(new_move)
                                    new_y += 1
                            new_x += 1

                        # castling
                        # White
                        if self.curr_player == "W" and x == 4 and y == 0:
                            short_castle = Move(x, y, 6, 0, self.position, self.curr_player)
                            if short_castle.is_legal_move():
                                legal_moves.append(short_castle)

                            long_castle = Move(x, y, 2, 0, self.position, self.curr_player)
                            if long_castle.is_legal_move():
                                legal_moves.append(long_castle)
                        elif self.curr_player == "B" and x == 4 and y == 7:
                            short_castle = Move(x, y, 6, 7, self.position, self.curr_player)
                            if short_castle.is_legal_move():
                                legal_moves.append(short_castle)

                            long_castle = Move(x, y, 2, 7, self.position, self.curr_player)
                            if long_castle.is_legal_move():
                                legal_moves.append(long_castle)

        return legal_moves

    # check if there is at least one legal move for use in stalemate
    def has_legal_move(self):

        # loop through all locations to find player's pieces
        for x in [0, 1, 2, 3, 4, 5, 6, 7]:
            for y in [0, 1, 2, 3, 4, 5, 6, 7]:
                cur_loc = self.position.locations[x][y]

                if cur_loc is not None and cur_loc.colour == self.curr_player:
                    # Pawn
                    if cur_loc.name == "p":
                        # the y positions of possible next moves, dub_y is for moving 2 spaces on a first move
                        if self.curr_player == "W":
                            next_y = y + 1
                            dub_y = y + 2
                        else:
                            next_y = y - 1
                            dub_y = y - 2

                        # check if pawn can move forward
                        if 0 <= next_y <= 7:
                            new_move = Move(x, y, x, next_y, self.position, self.curr_player)
                            if new_move.is_legal_move():
                                return True

                            # check if the pawn can capture
                            if 0 <= x - 1 <= 7:
                                new_move = Move(x, y, x - 1, next_y, self.position, self.curr_player)
                                if new_move.is_legal_move():
                                    return True

                            if 0 <= x + 1 <= 7:
                                new_move = Move(x, y, x + 1, next_y, self.position, self.curr_player)
                                if new_move.is_legal_move():
                                    return True

                        # check if pawn can move forward 2 steps
                        if 0 <= dub_y <= 7:
                            new_move = Move(x, y, x, dub_y, self.position, self.curr_player)
                            if new_move.is_legal_move():
                                return True

                    # Knight
                    if cur_loc.name == "N":
                        for new_x in [x-2, x-1, x+1, x+2]:
                            if 0 <= new_x <= 7:
                                for new_y in [y-2, y-1, y+1, y+2]:
                                    if 0 <= new_y <= 7:
                                        new_move = Move(x, y, new_x, new_y, self.position, self.curr_player)
                                        if new_move.is_legal_move():
                                            return True

                    # Bishop or Queen
                    if cur_loc.name == "B" or cur_loc.name == "Q":

                        # up and left
                        new_x = x + 1
                        new_y = y + 1
                        while new_x <= 7 and new_y <= 7:
                            new_move = Move(x, y, new_x, new_y, self.position, self.curr_player)
                            if new_move.is_legal_move():
                                return True
                            new_x += 1
                            new_y += 1

                        # down and left
                        new_x = x + 1
                        new_y = y - 1
                        while new_x <= 7 and new_y >= 0:
                            new_move = Move(x, y, new_x, new_y, self.position, self.curr_player)
                            if new_move.is_legal_move():
                                return True
                            new_x += 1
                            new_y -= 1

                        # up and right
                        new_x = x - 1
                        new_y = y + 1
                        while new_x >= 0 and new_y <= 7:
                            new_move = Move(x, y, new_x, new_y, self.position, self.curr_player)
                            if new_move.is_legal_move():
                                return True
                            new_x -= 1
                            new_y += 1

                        # down and left
                        new_x = x - 1
                        new_y = y - 1
                        while new_x >= 0 and new_y >= 0:
                            new_move = Move(x, y, new_x, new_y, self.position, self.curr_player)
                            if new_move.is_legal_move():
                                return True
                            new_x -= 1
                            new_y -= 1

                    # Rook or Queen
                    if cur_loc.name == "R" or cur_loc.name == "Q":

                        # up
                        new_y = y + 1
                        while new_y <= 7:
                            new_move = Move(x, y, x, new_y, self.position, self.curr_player)
                            if new_move.is_legal_move():
                                return True
                            new_y += 1

                        # down
                        new_y = y - 1
                        while new_y >= 0:
                            new_move = Move(x, y, x, new_y, self.position, self.curr_player)
                            if new_move.is_legal_move():
                                return True
                            new_y -= 1

                        # left
                        new_x = x - 1
                        while new_x >= 0:
                            new_move = Move(x, y, new_x, y, self.position, self.curr_player)
                            if new_move.is_legal_move():
                                return True
                            new_x -= 1

                        # right
                        new_x = x + 1
                        while new_x <= 7:
                            new_move = Move(x, y, new_x, y, self.position, self.curr_player)
                            if new_move.is_legal_move():
                                return True
                            new_x += 1

                    # King
                    if cur_loc.name == "K":

                        # regular King move
                        new_x = x - 1
                        while new_x < x + 2:
                            if 0 <= new_x <= 7:
                                new_y = y - 1
                                while new_y < y + 2:
                                    if 0 <= new_y <= 7:
                                        new_move = Move(x, y, new_x, new_y, self.position, self.curr_player)
                                        if new_move.is_legal_move():
                                            return True
                                    new_y += 1
                            new_x += 1

                        # castling
                        # White
                        if self.curr_player == "W" and x == 4 and y == 0:
                            short_castle = Move(x, y, 6, 0, self.position, self.curr_player)
                            if short_castle.is_legal_move():
                                return True

                            long_castle = Move(x, y, 2, 0, self.position, self.curr_player)
                            if long_castle.is_legal_move():
                                return True
                        elif self.curr_player == "B" and x == 4 and y == 7:
                            short_castle = Move(x, y, 6, 7, self.position, self.curr_player)
                            if short_castle.is_legal_move():
                                return True

                            long_castle = Move(x, y, 2, 7, self.position, self.curr_player)
                            if long_castle.is_legal_move():
                                return True

        return False

    def get_potential_moves(self):

        potential_moves = []

        if self.curr_player == "W":
            king_check = self.position.W_King_check
        else:
            king_check = self.position.B_King_check

        # loop through all locations to find player's pieces
        for x in [0, 1, 2, 3, 4, 5, 6, 7]:
            for y in [0, 1, 2, 3, 4, 5, 6, 7]:
                cur_loc = self.position.locations[x][y]

                if cur_loc is not None and cur_loc.colour == self.curr_player:
                    # Pawn
                    if cur_loc.name == "p":
                        # the y positions of possible next moves, dub_y is for moving 2 spaces on a first move
                        if self.curr_player == "W":
                            next_y = y + 1
                            dub_y = y + 2
                        else:
                            next_y = y - 1
                            dub_y = y - 2

                        # check if pawn can move forward
                        if 0 <= next_y <= 7:
                            new_move = Move(x, y, x, next_y, self.position, self.curr_player)
                            potential_moves.append(new_move)

                            # check if the pawn can capture
                            if 0 <= x - 1 <= 7:
                                new_move = Move(x, y, x - 1, next_y, self.position, self.curr_player)
                                potential_moves.append(new_move)

                            if 0 <= x + 1 <= 7:
                                new_move = Move(x, y, x + 1, next_y, self.position, self.curr_player)
                                potential_moves.append(new_move)

                        # check if pawn can move forward 2 steps
                        if 0 <= dub_y <= 7:
                            new_move = Move(x, y, x, dub_y, self.position, self.curr_player)
                            potential_moves.append(new_move)

                    # Knight
                    if cur_loc.name == "N":
                        for new_x in [x-2, x-1, x+1, x+2]:
                            if 0 <= new_x <= 7:
                                for new_y in [y-2, y-1, y+1, y+2]:
                                    if 0 <= new_y <= 7:
                                        new_move = Move(x, y, new_x, new_y, self.position, self.curr_player)
                                        potential_moves.append(new_move)

                    # Bishop or Queen
                    if cur_loc.name == "B" or cur_loc.name == "Q":

                        # up and left
                        new_x = x + 1
                        new_y = y + 1
                        while new_x <= 7 and new_y <= 7:
                            new_move = Move(x, y, new_x, new_y, self.position, self.curr_player)
                            potential_moves.append(new_move)
                            new_x += 1
                            new_y += 1

                        # down and left
                        new_x = x + 1
                        new_y = y - 1
                        while new_x <= 7 and new_y >= 0:
                            new_move = Move(x, y, new_x, new_y, self.position, self.curr_player)
                            potential_moves.append(new_move)
                            new_x += 1
                            new_y -= 1

                        # up and right
                        new_x = x - 1
                        new_y = y + 1
                        while new_x >= 0 and new_y <= 7:
                            new_move = Move(x, y, new_x, new_y, self.position, self.curr_player)
                            potential_moves.append(new_move)
                            new_x -= 1
                            new_y += 1

                        # down and left
                        new_x = x - 1
                        new_y = y - 1
                        while new_x >= 0 and new_y >= 0:
                            new_move = Move(x, y, new_x, new_y, self.position, self.curr_player)
                            potential_moves.append(new_move)
                            new_x -= 1
                            new_y -= 1

                    # Rook or Queen
                    if cur_loc.name == "R" or cur_loc.name == "Q":

                        # up
                        new_y = y + 1
                        while new_y <= 7:
                            new_move = Move(x, y, x, new_y, self.position, self.curr_player)
                            potential_moves.append(new_move)
                            new_y += 1

                        # down
                        new_y = y - 1
                        while new_y >= 0:
                            new_move = Move(x, y, x, new_y, self.position, self.curr_player)
                            potential_moves.append(new_move)
                            new_y -= 1

                        # left
                        new_x = x - 1
                        while new_x >= 0:
                            new_move = Move(x, y, new_x, y, self.position, self.curr_player)
                            potential_moves.append(new_move)
                            new_x -= 1

                        # right
                        new_x = x + 1
                        while new_x <= 7:
                            new_move = Move(x, y, new_x, y, self.position, self.curr_player)
                            potential_moves.append(new_move)
                            new_x += 1

                    # King
                    if cur_loc.name == "K":

                        # regular King move
                        new_x = x-1
                        while new_x < x + 2:
                            if 0 <= new_x <= 7:
                                new_y = y - 1
                                while new_y < y + 2:
                                    if 0 <= new_y <= 7:
                                        new_move = Move(x, y, new_x, new_y, self.position, self.curr_player)
                                        potential_moves.append(new_move)
                                    new_y += 1
                            new_x += 1

                        # castling
                        # White
                        if self.curr_player == "W" and x == 4 and y == 0:
                            short_castle = Move(x, y, 6, 0, self.position, self.curr_player)
                            potential_moves.append(short_castle)

                            long_castle = Move(x, y, 2, 0, self.position, self.curr_player)
                            potential_moves.append(long_castle)
                        elif self.curr_player == "B" and x == 4 and y == 7:
                            short_castle = Move(x, y, 6, 7, self.position, self.curr_player)
                            potential_moves.append(short_castle)

                            long_castle = Move(x, y, 2, 7, self.position, self.curr_player)
                            potential_moves.append(long_castle)

        return potential_moves

class FEN_converter:
    ################################################################################
    # This class converts a chess position to FEN Notation
    # (https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation)
    #
    # within a game all positions reached are stored in order to check if a draw
    # by repeated positions has occurred
    #
    # Note: Since this is only used to consider repeated positions only those elements
    # needed will be included (will not use turn number etc.)
    ################################################################################

    def __init__(self, position, curr_player):
        self.position = position
        self.curr_player = curr_player

    def convert_to_FEN(self):

        FEN = ""

        # record the positions of the pieces
        for row in [7, 6, 5, 4, 3, 2, 1, 0]:
            blank_count = 0

            for col in [0, 1, 2, 3, 4, 5, 6, 7]:
                piece = self.position.locations[col][row]
                if piece is None:
                    blank_count += 1
                else:
                    piece_nm = piece.name
                    # convert to upper case for white or lower case for black
                    if piece.colour == "W":
                        piece_nm = piece_nm.upper()
                    else:
                        piece_nm = piece_nm.lower()

                    # check if the previous pieces were blanks, if so add the count to the string and reset
                    if blank_count > 0:
                        FEN += str(blank_count)
                        blank_count = 0

                    # add the peice to the FEN
                    FEN += piece_nm

            # add on the last blank count if required
            if blank_count > 0:
                FEN += str(blank_count)

            # add a "/" at the end of each line other than the last which has a " "
            if row != 0:
                FEN += "/"
            else:
                FEN += " "

        # add the current player
        FEN = FEN + self.curr_player + " "

        # add castling
        castle_string = ""
        if not self.position.W_King_moved:
            if not self.position.W_7_Rook_moved:
                castle_string += "K"
            if not self.position.W_0_Rook_moved:
                castle_string += "Q"
        if not self.position.B_King_moved:
            if not self.position.B_7_Rook_moved:
                castle_string += "k"
            if not self.position.B_0_Rook_moved:
                castle_string += "q"
        # if no castling is available use "-"
        if castle_string == "":
            castle_string = "-"

        FEN += castle_string
        FEN += " "

        # add en passant piece
        if self.curr_player == "W":
            if self.position.B_passant is not None:
                FEN += str(self.position.B_passant)
            else:
                FEN += "-"
        else:
            if self.position.W_passant is not None:
                FEN += str(self.position.W_passant)
            else:
                FEN += "-"

        return FEN



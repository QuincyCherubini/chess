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
    def execute(self):

        # check if the move is legal, then perform it
        if self.is_legal_move():
            self.position.locations[self.to_x][self.to_y] = self.position.locations[self.from_x][self.from_y]
            self.position.locations[self.from_x][self.from_y] = None

            # promote pawn
            if self.curr_piece.colour == "W" and self.curr_piece.name == "p" and self.to_y == 7:
                new_peice = self.get_pawn_promotion()
                self.position.locations[self.to_x][self.to_y] = Piece("W", new_peice)

            if self.curr_piece.colour == "B" and self.curr_piece.name == "p" and self.to_y == 0:
                new_peice = self.get_pawn_promotion()
                self.position.locations[self.to_x][self.to_y] = Piece("B", new_peice)

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

    # test if a move is legal
    def is_legal_move(self):

        # check to make sure both positions are on the position
        if not self.position.is_in_range(self.from_x, self.from_y):
            return False
        if not self.position.is_in_range(self.to_x, self.to_y):
            return False

        # check if the piece at the current move is the current players
        if self.curr_piece is None or self.curr_piece.colour != self.curr_player:
            return False

        # check to make sure the next location does not contain a piece of the current player's colour
        # This will also catch trying to move to the current spot
        if self.next_piece is not None and self.next_piece.colour == self.curr_player:
            return False

        # todo: check if King would be in check still

        if self.curr_piece.name == "p":
            return self.is_legal_pawn_move()

        elif self.curr_piece.name == "B":
            return self.is_legal_bishop_move()

        elif self.curr_piece.name == "N":
            return self.is_legal_knight_move()

        elif self.curr_piece.name == "R":
            return self.is_legal_rook_move()

        elif self.curr_piece.name == "Q":
            return self.is_legal_queen_move()

        elif self.curr_piece.name == "K":
            return self.is_legal_king_move()

        # this should never happen
        else:
            print("You have passed an invalid piece")
            return False

    def is_legal_pawn_move(self):

        # white player
        if self.curr_player == "W":

            # reset white passant status
            self.position.W_passant = None

            # moving one piece forward
            if self.from_x == self.to_x and self.to_y - self.from_y == 1 and self.next_piece is None:
                return True

            # move two piece forward
            if self.from_x == self.to_x and self.to_y - self.from_y == 2 and self.next_piece is None and self.from_y == 1:
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
            if self.from_x == self.to_x and self.from_y - self.to_y == 2 and self.next_piece is None and self.from_y == 6:
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
        if abs(self.from_x - self.to_x) != abs(self.from_y - self.to_y):
            return False

        # check if any of the in between spots have a piece on them
        if self.to_x > self.from_x:
            x_range = range(self.from_x + 1, self.to_x)
        else:
            x_range = range(self.to_x + 1, self.from_x)[::-1]

        if self.to_y > self.from_y:
            y_range = range(self.from_y + 1, self.to_y)
        else:
            y_range = range(self.to_y + 1, self.from_y)[::-1]

        for i in range(abs(self.from_x - self.to_x) - 1):
            if self.position.locations[x_range[i]][y_range[i]] is not None:
                return False

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

        # check if there are any pieces in the way
        if self.from_x == self.to_x:
            if self.to_y > self.from_y:
                y_range = range(self.from_y + 1, self.to_y)
            elif self.to_y < self.from_y:
                y_range = range(self.to_y + 1, self.from_y)[::-1]

            for i in range(abs(self.from_y - self.to_y) - 1):
                if self.position.locations[self.to_x][y_range[i]] is not None:
                    return False

        elif self.from_y == self.to_y:
            if self.to_x > self.from_x:
                x_range = range(self.from_x + 1, self.to_x)
            elif self.to_x < self.from_x:
                x_range = range(self.to_x + 1, self.from_x)[::-1]

            for i in range(abs(self.from_x - self.to_x) - 1):
                if self.position.locations[x_range[i]][self.to_y] is not None:
                    return False

        # if the move is not on the same rank or file
        else:
            return False

        # track that the rook has moved
        if self.curr_piece.colour == "W":
            if self.from_x == 0 and self.from_y == 0:
                self.W_0_Rook_moved = True
            elif self.from_x == 7 and self.from_y == 0:
                self.W_7_Rook_moved = True

        elif self.curr_piece.colour == "B":
            if self.from_x == 0 and self.from_y == 7:
                self.B_0_Rook_moved = True
            elif self.from_x == 7 and self.from_y == 7:
                self.B_7_Rook_moved = True

        return True

    def is_legal_queen_move(self):

        # check if the queen moves like a rook
        if self.from_x == self.to_x:
            if self.to_y > self.from_y:
                y_range = range(self.from_y + 1, self.to_y)
            elif self.to_y < self.from_y:
                y_range = range(self.to_y + 1, self.from_y)[::-1]

            for i in range(abs(self.from_y - self.to_y) - 1):
                if self.position.locations[self.to_x][y_range[i]] is not None:
                    return False
            return True

        elif self.from_y == self.to_y:
            if self.to_x > self.from_x:
                x_range = range(self.from_x + 1, self.to_x)
            elif self.to_x < self.from_x:
                x_range = range(self.to_x + 1, self.from_x)[::-1]

            for i in range(abs(self.from_x - self.to_x) - 1):
                if self.position.locations[x_range[i]][self.to_y] is not None:
                    return False
            return True

        # if it doesn't move like a rook does it move like a bishop
        return self.is_legal_bishop_move()

    def is_legal_king_move(self):

        # regular king move
        x_diff = abs(self.from_x - self.to_x)
        y_diff = abs(self.from_y - self.to_y)

        if (x_diff == 0 and y_diff == 1) or (x_diff == 1 and y_diff == 0):
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
                        # todo: make sure the actual move handles these variables
                        # self.position.W_King_moved = True
                        # self.W_7_Rook_moved = True
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

    # get user input for what piece to promote a pawn to
    def get_pawn_promotion(self):

        while True:
            userInput = input("Pick a piece to promote pawn to: ")

            if userInput in ["Q", "R", "B", "N"]:
                return userInput
            else:
                print("Please enter a valid piece")


class Position:

    # first element is row, second is column
    # 0=a, 1=b, ... 7=h
    def __init__(self):
        self.locations = [[None for _ in range(8)] for _ in range(8)]

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

    #player can be "W" or "B"
    def display_position(self, player):

        if player == "W":
            print("  -----------------------------------------")
            for row in reversed(range(8)):
                row_string = str(row) + " |"
                for col in range(8):
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
            for row in range(8):
                row_string = str(row) + " |"
                for col in reversed(range(8)):
                    if self.locations[col][row] is None:
                        row_string = row_string + "    |"
                    else:
                        piece = self.locations[col][row]
                        row_string = row_string + " " + piece.colour + piece.name + " |"
                print(row_string)
                print("-----------------------------------------")

        else:
            print("display_position error: please pass a valid player value")

    # check if a location is on the board
    def is_in_range(self, x_pos, y_pos):

        if x_pos > 7 or x_pos < 0:
            return False
        if y_pos > 7 or y_pos < 0:
            return False

        return True

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

        # check each pawn location
        for i in range(-1, 2):

            if self.is_in_range(x_pos - 1, new_y):
                pawn = self.locations[x_pos - 1][new_y]

                if pawn is not None and pawn.colour == attacking_colour and pawn.name == "p":
                    return True

        # if now pawn is attacking the spot return False
        return False

    # check if a location is attacked by a knight
    def is_attacked_knight(self, x_pos, y_pos, attacking_colour):

        for x in [-1, 1]:
            for y in [-2, 2]:
                if self.is_in_range(x_pos + x, y_pos + y):
                    knight = self.locations[x_pos + x][y_pos + y]
                    if knight is not None and knight.colour == attacking_colour and knight.name == "N":
                        return True

        for x in [-2, 2]:
            for y in [-1, 1]:
                if self.is_in_range(x_pos + x, y_pos + y):
                    knight = self.locations[x_pos + x][y_pos + y]
                    if knight is not None and knight.colour == attacking_colour and knight.name == "N":
                        return True

        # if no knights are attacking return False
        return False

    # check if a location is attacked by a bishop or Queen
    def is_attacked_bishop(self, x_pos, y_pos, attacking_colour):

        # find the first piece on each diagonal from the initial location
        # to top right
        temp_x = x_pos + 1
        temp_y = y_pos + 1
        while temp_y < 8 and temp_x < 8:
            temp_piece = self.locations[temp_x][temp_y]
            if temp_piece is not None:
                if temp_piece.colour == attacking_colour and (temp_piece.name == "B" or temp_piece.name == "Q"):
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
                if temp_piece.colour == attacking_colour and (temp_piece.name == "B" or temp_piece.name == "Q"):
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
                if temp_piece.colour == attacking_colour and (temp_piece.name == "B" or temp_piece.name == "Q"):
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
                if temp_piece.colour == attacking_colour and (temp_piece.name == "B" or temp_piece.name == "Q"):
                    return True
                else:
                    break
            temp_y += 1
            temp_x += 1

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
        for x in range(-1, 2):
            for y in range(-1, 2):

                if self.is_in_range(x_pos + x, y_pos + y):
                    king = self.locations[x_pos + x][y_pos + y]

                    if king is not None and king.colour == attacking_colour and king.name == "K":
                        return True

        # if none of the surrounding pieces contain a King return False
        return False


class Game:

    def __init__(self):

        self.position = Position()  # set up a new position on game start
        self.drawing_moves = 0  # resets on a pawn move or piece capture, if this number reaches 50 the game is a draw
        self.position_history = []  # this will log all of the positions and then check if the same has been reached 3 times
        self.curr_player = "W"
        self.opp_player = "B"

    # executes a move
    def move(self, from_x, from_y, to_x, to_y):

        my_move = Move(from_x, from_y, to_x, to_y, self.position, self.curr_player)

        # if the move is legal make it
        if my_move.is_legal_move():

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

            # add the new position to the list of positions
            fen_converter = FEN_converter(self.position, self.curr_player)
            fen = fen_converter.convert_to_FEN()
            self.position_history.append(fen)

            if self.curr_player == "W":
                self.curr_player = "B"
                self.opp_player = "W"
            else:
                self.curr_player = "W"
                self.opp_player = "B"

        # if the move provided was not legal:
        else:
            print("Illegal move passed to Game")

    def game_is_over(self):

        if self.is_checkmated(self.curr_player):
            print("{} Wins!".format(self.opp_player))
            return True

        if self.is_stalemate(self.curr_player):
            print("Stalemate!")
            return True

        if self.repeated_position():
            print("Draw by repeated position!")
            return True

        if self.is_50_moves():
            print("Draw, 50 moves without capture or pawn move")
            return True

        if self.is_insuffient_material():
            print("Draw by insufficient material!")
            return True

        return False

    # test if the player player_colour is checkmated
    def is_checkmated(self, player_colour):

        if player_colour == "B":
            attacking_colour = "W"
        else:
            attacking_colour = "B"

        # get the location of the player's King
        King_pos = None
        for x in range(0, 8):
            for y in range(0, 8):
                cur_loc = self.position.locations[x][y]
                if cur_loc is not None and cur_loc.name == "K" and cur_loc.colour == player_colour:
                    King_pos = [x, y]
                    break
            if King_pos is not None:
                break

        # if the King is not attacked return False, it can't be mate
        if not self.position.is_attacked(King_pos[0], King_pos[1], attacking_colour):
            return False

        # Check if each square surrounding the King is attacked or contains a piece of the same colour
        for x_pos in range(King_pos[0] - 1, King_pos[0] + 2):
            for y_pos in range(King_pos[1] - 1, King_pos[1] + 2):
                if self.position.is_in_range(x_pos, y_pos) and (x_pos != King_pos[0] and y_pos != King_pos[1]):
                    # check if there is a player's piece
                    cur_loc = self.position.locations[x_pos][y_pos]
                    if cur_loc is not None and cur_loc.colour == player_colour:
                        continue
                    if not self.position.is_attacked(x_pos, y_pos, attacking_colour):
                        return False

        # This can only be reached if checkmate has occurred
        return True

    # checks if the player who's turn it is (turn_colour) is in a stalemate
    def is_stalemate(self, player_colour):

        # King must not be attacked
        # King must not be able to move
        # no other pieces of the player may be able to move

        if player_colour == "B":
            attacking_colour = "W"
        else:
            attacking_colour = "B"

        # get the location of the player's King
        King_pos = None
        for x in range(0, 8):
            for y in range(0, 8):
                cur_loc = self.position.locations[x][y]
                if cur_loc is not None and cur_loc.name == "K" and cur_loc.colour == player_colour:
                    King_pos = [x, y]
                    break
            if King_pos is not None:
                break

        # if the King is attacked return False
        if self.position.is_attacked(King_pos[0], King_pos[1], attacking_colour):
            return False

        # get a list of all legal moves, if there are none it is stalemate
        legal_moves = self.get_all_legal_moves()
        return len(legal_moves) == 0

    # todo:
    # if same position is reached 3 times a player can call a draw
    def repeated_position(self):
        return False

    # if no piece has been captured or pawn moved in 50 turns a player can claim a draw
    def is_50_moves(self):
        return self.drawing_moves == 50

    # todo:
    # if insuffiencient material for a checkmate by either side the game is a draw
    # the draws are K vs.K, K+B vs. K, K+N vs. K, and K+B vs K+B of same colour
    # however I may also include pieces where a checkmate cannot be forced with reasonably play
    # these combos are: K+N+N v K, K+R vs. K+R and K+R vs. K+N or K+B
    def is_insuffient_material(self):

        black_pieces = []
        white_pieces = []

        return False

    # todo
    # winning material
    # may add a function to consider a game won for the MCTS if we reach K vs. K+R, K vs. K+Q, or K vs. K+B+B
    # Assuming the King cannot immediately capture one of these pieces
    def winning_material(self):

        black_pieces = []
        white_pieces = []

        return False

    # todo: Should this be broken up?
    def get_all_legal_moves(self):

        legal_moves = []

        # loop through all locations to find player's pieces
        for x in range(0, 8):
            for y in range(0, 8):
                cur_loc = self.position.locations[x][y]

                if cur_loc is not None and cur_loc.colour == self.curr_player:
                    # Pawn
                    if cur_loc.name == "p":
                        if self.curr_player == "W":
                            next_y = y + 1
                        else:
                            next_y = y - 1

                        # check if pawn can move forward
                        new_move = Move(x, y, x, next_y, self.position, self.curr_player)
                        if new_move.is_legal_move():
                            legal_moves.append(new_move)

                        # check if pawn can capture
                        if self.position.is_in_range(x - 1, next_y):
                            new_move = Move(x, y, x - 1, next_y, self.position, self.curr_player)
                            if new_move.is_legal_move():
                                legal_moves.append(new_move)
                        if self.position.is_in_range(x + 1, next_y):
                            new_move = Move(x, y, x + 1, next_y, self.position, self.curr_player)
                            if new_move.is_legal_move():
                                legal_moves.append(new_move)

                    # Knight
                    elif cur_loc.name == "N":
                        for new_x in [x-2, x-1, x+1, x+2]:
                            for new_y in [y-2, y-1, y+1, y+2]:
                                if self.position.is_in_range(new_x, new_y):
                                    new_move = Move(x, y, new_x, new_y, self.position, self.curr_player)
                                    if new_move.is_legal_move():
                                        legal_moves.append(new_move)

                    # Bishop or Queen
                    elif cur_loc.name == "B" or cur_loc.name == "Q":

                        # up and left
                        new_x = x + 1
                        new_y = y + 1
                        while new_x <= 7 and new_y <= 7:
                            if self.position.is_in_range(new_x, new_y):
                                new_move = Move(x, y, new_x, new_y, self.position, self.curr_player)
                                if new_move.is_legal_move():
                                    legal_moves.append(new_move)
                            new_x += 1
                            new_y += 1

                        # down and left
                        new_x = x + 1
                        new_y = y - 1
                        while new_x <= 7 and new_y >= 0:
                            if self.position.is_in_range(new_x, new_y):
                                new_move = Move(x, y, new_x, new_y, self.position, self.curr_player)
                                if new_move.is_legal_move():
                                    legal_moves.append(new_move)
                            new_x += 1
                            new_y -= 1

                        # up and right
                        new_x = x - 1
                        new_y = y + 1
                        while new_x >= 0 and new_y <= 7:
                            if self.position.is_in_range(new_x, new_y):
                                new_move = Move(x, y, new_x, new_y, self.position, self.curr_player)
                                if new_move.is_legal_move():
                                    legal_moves.append(new_move)
                            new_x -= 1
                            new_y += 1

                        # down and left
                        new_x = x - 1
                        new_y = y - 1
                        while new_x >= 0 and new_y >= 0:
                            if self.position.is_in_range(new_x, new_y):
                                new_move = Move(x, y, new_x, new_y, self.position, self.curr_player)
                                if new_move.is_legal_move():
                                    legal_moves.append(new_move)
                            new_x -= 1
                            new_y -= 1

                    # Rook or Queen
                    elif cur_loc.name == "R" or cur_loc.name == "Q":

                        # up
                        new_y = y + 1
                        while new_y <= 7:
                            if self.position.is_in_range(x, new_y):
                                new_move = Move(x, y, x, new_y, self.position, self.curr_player)
                                if new_move.is_legal_move():
                                    legal_moves.append(new_move)
                            new_y += 1

                        # down
                        new_y = y - 1
                        while new_y >= 0:
                            if self.position.is_in_range(x, new_y):
                                new_move = Move(x, y, x, new_y, self.position, self.curr_player)
                                if new_move.is_legal_move():
                                    legal_moves.append(new_move)
                            new_y -= 1

                        # left
                        new_x = x - 1
                        while new_x >= 0:
                            if self.position.is_in_range(new_x, y):
                                new_move = Move(x, y, new_x, y, self.position, self.curr_player)
                                if new_move.is_legal_move():
                                    legal_moves.append(new_move)
                            new_x -= 1

                        # right
                        new_x = x + 1
                        while new_x <= 7:
                            if self.position.is_in_range(new_x, y):
                                new_move = Move(x, y, new_x, y, self.position, self.curr_player)
                                if new_move.is_legal_move():
                                    legal_moves.append(new_move)
                            new_x += 1

                    # King
                    elif cur_loc.name == "K":
                        for new_x in range(x - 1, x + 2):
                            for new_y in range(y - 1, y + 2):
                                if self.position.is_in_range(new_x, new_y):
                                    new_move = Move(x, y, new_x, new_y, self.position, self.curr_player)
                                    if new_move.is_legal_move():
                                        legal_moves.append(new_move)

        return legal_moves


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



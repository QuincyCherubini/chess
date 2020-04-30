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

    def __init__(self, from_x, from_y, to_x, to_y, board, curr_player):
        self.from_x = from_x
        self.from_y = from_y
        self.to_x = to_x
        self.to_y = to_y
        self.board = board
        self.curr_player = curr_player

        # set a variable for the opposing player
        if curr_player == "W":
            self.opp_player = "B"
        else:
            self.opp_player = "W"

        # pieces at the locations
        self.curr_piece = board.locations[from_x][from_y]
        self.next_piece = board.locations[to_x][to_y]

    # curr, next are an array of [row, col]
    def move(self):

        # check if the move is legal, then perform it
        if self.is_legal_move(self.from_x, self.from_y, self.to_x, self.to_y, self.curr_piece, self.next_piece):
            self.board.locations[self.to_x][self.to_y] = self.board.locations[self.from_x][self.from_y]
            self.board.locations[self.from_x][self.from_y] = None

            # promote pawn
            if self.curr_piece.colour == "W" and self.curr_piece.name == "p" and self.to_y == 7:
                new_peice = self.get_pawn_promotion()
                self.board.locations[self.to_x][self.to_y] = Piece("W", new_peice)

            if self.curr_piece.colour == "B" and self.curr_piece.name == "p" and self.to_y == 0:
                new_peice = self.get_pawn_promotion()
                self.board.locations[self.to_x][self.to_y] = Piece("B", new_peice)

            # en passant
            if self.curr_player == "W":
                side_piece = self.board.locations[self.to_x][self.to_y - 1]
                if self.from_y == 4 and self.to_y == 5 and abs(self.to_x - self.from_x) == 1 and side_piece is not None and \
                        side_piece.colour == "B" and side_piece.name == "p" and self.B_passant == self.to_x:
                    self.board.locations[self.to_x][self.to_y - 1] = None

            elif self.curr_player == "B":
                side_piece = self.board.locations[self.to_x][self.to_y + 1]
                if self.from_y == 3 and self.to_y == 2 and abs(self.to_x - self.from_x) == 1 and side_piece is not None and \
                        side_piece.colour == "W" and side_piece.name == "p" and self.A_passant == self.to_x:
                    self.board.locations[self.to_x][self.to_y + 1] = None

            # move the rook for castling
            if self.curr_piece.name == "K":
                # white castling short
                if self.from_x == 4 and self.from_y == 0 and self.to_x == 6 and self.to_y == 0:
                    self.board.locations[7][0] = None
                    self.board.locations[5][0] = Piece("W", "R")

                # white castling long
                elif self.from_x == 4 and self.from_y == 0 and self.to_x == 2 and self.to_y == 0:
                    self.board.locations[0][0] = None
                    self.board.locations[3][0] = Piece("W", "R")

                # black castling short
                if self.from_x == 4 and self.from_y == 7 and self.to_x == 6 and self.to_y == 7:
                    self.board.locations[7][7] = None
                    self.board.locations[5][7] = Piece("B", "R")

                # black castling long
                elif self.from_x == 4 and self.from_y == 7 and self.to_x == 2 and self.to_y == 7:
                    self.board.locations[0][7] = None
                    self.board.locations[3][7] = Piece("B", "R")

    # test if a move is legal
    def is_legal_move(self):

        # check to make sure both positions are on the board
        if not self.board.is_in_range(self.from_x, self.from_y):
            return False

        if not self.board.is_in_range(self.to_x, self.to_y):
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
            self.W_passant = None

            # moving one piece forward
            if self.from_x == self.to_x and self.to_y - self.from_y == 1 and self.next_piece is None:
                return True

            # move two piece forward
            if self.from_x == self.to_x and self.to_y - self.from_y == 2 and self.next_piece is None and self.from_y == 1:
                self.W_passant = self.from_x
                return True

            # taking out a piece
            if self.to_y - self.from_y == 1 and abs(self.from_x - self.to_x) == 1 and self.next_piece is not None and \
                    self.next_piece.colour == "B":
                return True

            # en passant
            side_piece = self.board.locations[self.to_x][self.to_y - 1]
            if self.from_y == 4 and self.to_y == 5 and abs(self.to_x - self.from_x) == 1 and side_piece is not None and \
                    side_piece.colour == "B" and side_piece.name == "p" and self.B_passant == self.to_x:
                return True

            # if it is not one of these moves return False
            return False

        # Black's Turn
        elif self.curr_player == "B":

            # reset white passant status
            self.B_passant = None

            # moving one piece forward
            if self.from_x == self.to_x and self.from_y - self.to_y == 1 and self.next_piece is None:
                return True

            # move two piece forward
            if self.from_x == self.to_x and self.from_y - self.to_y == 2 and self.next_piece is None and self.from_y == 6:
                self.B_passant = self.from_x
                return True

            # taking out a piece
            if self.from_y - self.to_y == 1 and abs(self.from_x - self.to_x) == 1 and self.next_piece is not None and \
                    self.next_piece.colour == "W":
                return True

            # en passant
            side_piece = self.board.locations[self.to_x][self.to_y + 1]
            if self.from_y == 3 and self.to_y == 2 and abs(self.to_x - self.from_x) == 1 and side_piece is not None and \
                    side_piece.colour == "W" and side_piece.name == "p" and self.A_passant == self.to_x:
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
            if self.board.locations[x_range[i]][y_range[i]] is not None:
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
                if self.board.locations[self.to_x][y_range[i]] is not None:
                    return False

        elif self.from_y == self.to_y:
            if self.to_x > self.from_x:
                x_range = range(self.from_x + 1, self.to_x)
            elif self.to_x < self.from_x:
                x_range = range(self.to_x + 1, self.from_x)[::-1]

            for i in range(abs(self.from_x - self.to_x) - 1):
                if self.board.locations[x_range[i]][self.to_y] is not None:
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
                if self.board.locations[self.to_x][y_range[i]] is not None:
                    return False
            return True

        elif self.from_y == self.to_y:
            if self.to_x > self.from_x:
                x_range = range(self.from_x + 1, self.to_x)
            elif self.to_x < self.from_x:
                x_range = range(self.to_x + 1, self.from_x)[::-1]

            for i in range(abs(self.from_x - self.to_x) - 1):
                if self.board.locations[x_range[i]][self.to_y] is not None:
                    return False
            return True

        # if it doesn't move like a rook does it move like a bishop
        return self.is_legal_bishop_move()

    # and king not in check
    def is_legal_king_move(self):

        # regular king move
        x_diff = abs(self.from_x - self.to_x)
        y_diff = abs(self.from_y - self.to_y)

        if (x_diff == 0 and y_diff == 1) or (x_diff == 1 and y_diff == 0):
            if self.curr_piece.colour == 'W':
                self.W_King_moved = False
            elif self.curr_piece.colour == 'B':
                self.B_King_moved = False
            return True

        # white castling short
        if self.from_x == 4 and self.from_y == 0 and self.to_x == 6 and self.to_y == 0:
            # check if King and Rook haven't moved
            if not self.W_King_moved and not self.W_7_Rook_moved and self.board.locations[5][0] is None and not \
                    self.is_attacked(4, 0, "B") and not self.is_attacked(5, 0, "B") and not self.is_attacked(6, 0,
                                                                                                             "B"):
                self.W_King_moved = True
                self.W_7_Rook_moved = True
                # todo: check to make sure the King doesn't move through check
                return True

        # white castling long
        # todo: fix this if statement
        elif self.from_x == 4 and self.from_y == 0 and self.to_x == 2 and self.to_y == 0:
            # check if King and Rook haven't moved
            if not self.W_King_moved and not self.W_0_Rook_moved and self.board.locations[3][0] is None and \
                    self.board.locations[1][0] and not self.is_attacked(5, 0, "B") is None:
                self.W_King_moved = True
                self.W_0_Rook_moved = True
                # todo: check to make sure the King doesn't move through check
                return True

        # black castling short
        if self.from_x == 4 and self.from_y == 7 and self.to_x == 6 and self.to_y == 7:
            # check if King and Rook haven't moved
            if not self.B_King_moved and not self.B_0_Rook_moved and self.board.locations[5][7] is None:
                self.B_King_moved = True
                self.B_0_Rook_moved = True
                # todo: check to make sure the King doesn't move through check
                return True

        # black castling long
        elif self.from_x == 4 and self.from_y == 7 and self.to_x == 2 and self.to_y == 7:
            # check if King and Rook haven't moved
            if not self.B_King_moved and not self.B_0_Rook_moved and self.board.locations[3][7] is None and \
                    self.board.locations[1][7] is None:
                self.B_King_moved = True
                self.B_0_Rook_moved = True
                # todo: check to make sure the King doesn't move through check
                return True

        # if none of these criteria are met return False
        return False

    def get_all_legal_moves(self):

        if player_colour == "B":
            attacking_colour = "W"
        else:
            attacking_colour = "B"

        legal_moves = []

        return legal_moves

class Board:

    # first element is row, second is colum
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

        # track which coloums are currently available to en passant
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
    def display_board(self, player):

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
            print("display_board error: please pass a valid player value")

    # get user input for what piece to promote a pawn to
    def get_pawn_promotion(self):

        while True:
            userInput = input("Pick a piece to promote pawn to: ")

            if userInput in ["Q", "R", "B", "N"]:
                return userInput
            else:
                print("Please enter a valid piece")

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
        elif attacking_colour == "W":
            new_y = y_pos - 1

        # check each pawn location
        for i in range(-1, 2):
            try:
                pawn = self.locations[x_pos - 1][new_y]
            except IndexError:
                pawn = None

            if pawn is not None and pawn.colour == attacking_colour and pawn.name == "p":
                return True

        # if now pawn is attacking the spot return False
        return False

    # check if a location is attacked by a knight
    def is_attacked_knight(self, x_pos, y_pos, attacking_colour):

        for x in [-1, 1]:
            for y in [-2, 2]:

                try:
                    knight = self.locations[x_pos + x][y_pos + y]
                except IndexError:
                    knight = None

                if knight is not None and knight.colour == attacking_colour and knight.name == "N":
                    return True

        for x in [-2, 2]:
            for y in [-1, 1]:

                try:
                    knight = self.locations[x_pos + x][y_pos + y]
                except IndexError:
                    knight = None

                if knight is not None and knight.colour == attacking_colour and knight.name == "N":
                    return True

        # if no knights are attacking return Flase
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

                try:
                    king = self.locations[x_pos + x][y_pos + y]
                except IndexError:
                    king = None

                if king is not None and king.colour == attacking_colour and king.name == "K":
                    return True

        # if none of the surrounding pieces contain a King return False
        return False

    # test if the player player_colour is checkmated
    def is_checkmated(self, player_colour):

        if player_colour == "B":
            attacking_colour = "W"
        else:
            attacking_colour = "B"

        # get the location of the player's King
        King_pos = None
        for x in self.locations:
            for y in x:
                cur_loc = self.locations[x][y]
                if piece is not None and cur_loc.name == "K" and cur_loc.colour == player_colour:
                    King_pos = [x, y]
                    break
            if King_pos is not None:
                break

        # if the King is not attacked return False, it can't be mate
        if not self.is_attacked(King_pos[0], King_pos[1], attacking_colour):
            return False

        # Check if each square surrounding the King is attacked or contains a piece of the same colour
        for x_pos in range(King_pos[0] - 1, King_pos[0] + 2):
            for y_pos in range(King_pos[1] - 1, King_pos[1] + 2):
                if self.is_in_range(x_pos, y_pos) and (x_pos != King_pos[0] and y_pos != King_pos[1]):
                    # check if there is a player's piece
                    cur_loc = self.locations[x_pos][y_pos]
                    if cur_loc is not None and cur_loc.colour == player_colour:
                        continue
                    if not self.is_attacked(x_pos, y_pos, attacking_colour):
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
        for x in self.locations:
            for y in x:
                cur_loc = self.locations[x][y]
                if cur_loc is not None and cur_loc.name == "K" and cur_loc.colour == player_colour:
                    King_pos = [x, y]
                    break
            if King_pos is not None:
                break

        # if the King is attacked return False
        if self.is_attacked(King_pos[0], King_pos[1], attacking_colour):
            return False

        # check if there is a square the King can move too
        for x_pos in range(King_pos[0] - 1, King_pos[0] + 2):
            for y_pos in range(King_pos[1] - 1, King_pos[1] + 2):
                if self.is_in_range(x_pos, y_pos) and (x_pos != King_pos[0] and y_pos != King_pos[1]):
                    # check if there is a player's piece
                    cur_loc = self.locations[x_pos][y_pos]
                    if cur_loc is not None and cur_loc.colour == player_colour:
                        continue
                    if not self.is_attacked(x_pos, y_pos, attacking_colour):
                        return False

        # check if another of the player's pieces can move
        # pieces cannot move if they are blocked in by their own pieces or pinned to the King

        # loop through all locations to find player's pieces
        for x in self.locations:
            for y in x:
                cur_loc = self.locations[x][y]
                # todo: check for pins
                if cur_loc is not None and cur_loc.colour == player_colour:
                    # if pawn can move forward or take return false
                    if cur_loc.name == "p":
                        # check if pawn can move forward
                        # check if pawn can capture
                    elif cur_loc.name == "N":
                        # stuff
                    elif cur_loc.name == "B":
                        # stuff
                    elif cur_loc.name == "R":
                        # stuff
                    elif cur_loc.name == "Q":
                        # stuff

        # if it's reached this point it's stalemate
        return True


    # if same position is reached 3 times a player can call a draw

    # if no piece has been captured or pawn moved in 50 turns a player can claim a draw
    def is_50_moves(self):
        return self.drawing_moves == 50

    # if insuffiencient material for a checkmate by either side the game is a draw
    # the draws are K vs.K, K+B vs. K, K+N vs. K, and K+B vs K+B of same colour
    # however I may also include pieces where a checkmate cannot be forced with reasonably play
    # these combos are: K+N+N v K, K+R vs. K+R and K+R vs. K+N or K+B

    # winning material
    # may add a function to consider a game won for the MCTS if we reach K vs. K+R, K vs. K+Q, or K vs. K+B+B

class Game:

    def __init__(self):

        # set up a new board on game start
        self.board = Board()
        # resets on a pawn move or piece capture, if this number reaches 50 the game is a draw
        self.drawing_moves = 0
        # this will log all of the positions and then check if the same has been reached 3 times
        self.position_history = []
        self.curr_player = "W"

    # executes a move
    def move(self, from_x, from_y, to_x, to_y):

        my_move = Move(from_x, from_y, to_x, to_y, self.board, self.curr_player)

        # if the move is legal make it
        if my_move.is_legal_move():
            my_move.execute()

            # todo: check if move resets draw counter
            # check if the move is a pawn move or a capture, if so reset self.drawing_moves
            from_piece = self.board.locations[from_x][from_y]
            to_piece = self.board.locations[to_x][to_y]

            if from_piece.name == "p":
                self.drawing_moves = 0
            elif to_piece is not None:
                self.drawing_moves = 0
            # up the count after blacks turn
            elif from_piece.colour == "B":
                self.drawing_moves += 1

            # todo: check if the move resulted in a checkmate

            # todo: add the new position to the list of positions

            # todo: check if the omve resulted in a draw

            if self.curr_player == "W":
                self.curr_player = "B"
            else:
                self.curr_player == "W"

        # if the move provided was not legal:
        else:
            print("Illegal move passed to Game")

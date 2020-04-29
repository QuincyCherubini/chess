class piece:

    # colour = {W, B)
    # name = {p, N, B, R, Q, K}
    def __init__(self, colour, name):
        self.colour = colour
        self.name = name

    def get_colour(self):
        return self.colour

    def get_name(self):
        return self.name

class board:

    # first element is row, second is location
    # 0=a, 1=b, ... 7=h
    def __init__(self):
        self.locations = [[None for _ in range(8)] for _ in range(8)]
        self.curr_player = "W"

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
        self.locations[0][1] = piece("W", "p")
        self.locations[1][1] = piece("W", "p")
        self.locations[2][1] = piece("W", "p")
        self.locations[3][1] = piece("W", "p")
        self.locations[4][1] = piece("W", "p")
        self.locations[5][1] = piece("W", "p")
        self.locations[6][1] = piece("W", "p")
        self.locations[7][1] = piece("W", "p")
        self.locations[0][0] = piece("W", "R")
        self.locations[1][0] = piece("W", "N")
        self.locations[2][0] = piece("W", "B")
        self.locations[3][0] = piece("W", "Q")
        self.locations[4][0] = piece("W", "K")
        self.locations[5][0] = piece("W", "B")
        self.locations[6][0] = piece("W", "N")
        self.locations[7][0] = piece("W", "R")

        # set the black pieces
        self.locations[0][6] = piece("B", "p")
        self.locations[1][6] = piece("B", "p")
        self.locations[2][6] = piece("B", "p")
        self.locations[3][6] = piece("B", "p")
        self.locations[4][6] = piece("B", "p")
        self.locations[5][6] = piece("B", "p")
        self.locations[6][6] = piece("B", "p")
        self.locations[7][6] = piece("B", "p")
        self.locations[0][7] = piece("B", "R")
        self.locations[1][7] = piece("B", "N")
        self.locations[2][7] = piece("B", "B")
        self.locations[3][7] = piece("B", "Q")
        self.locations[4][7] = piece("B", "K")
        self.locations[5][7] = piece("B", "B")
        self.locations[6][7] = piece("B", "N")
        self.locations[7][7] = piece("B", "R")

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

    # curr, next are an array of [row, col]
    def move(self, curr_x, curr_y, next_x, next_y):

        # piece at the current location
        curr_piece = self.locations[curr_x][curr_y]
        next_piece = self.locations[next_x][next_y]

        # check if the move is legal, then perform it
        if self.is_legal_move(curr_x, curr_y, next_x, next_y, curr_piece, next_piece):
            self.locations[next_x][next_y] = self.locations[curr_x][curr_y]
            self.locations[curr_x][curr_y] = None

            # promote pawn
            if curr_piece.colour == "W" and curr_piece.name == "p" and next_y == 7:
                new_peice = self.get_pawn_promotion()
                self.locations[next_x][next_y] = piece("W", new_peice)

            if curr_piece.colour == "B" and curr_piece.name == "p" and next_y == 0:
                new_peice = self.get_pawn_promotion()
                self.locations[next_x][next_y] = piece("B", new_peice)

            # en passant
            if self.curr_player == "W":
                side_piece = self.locations[next_x][next_y - 1]
                if curr_y == 4 and next_y == 5 and abs(next_x - curr_x) == 1 and side_piece is not None and \
                        side_piece.colour == "B" and side_piece.name == "p" and self.B_passant == next_x:
                    self.locations[next_x][next_y - 1] = None

            elif self.curr_player == "B":
                side_piece = self.locations[next_x][next_y + 1]
                if curr_y == 3 and next_y == 2 and abs(next_x - curr_x) == 1 and side_piece is not None and \
                        side_piece.colour == "W" and side_piece.name == "p" and self.A_passant == next_x:
                    self.locations[next_x][next_y + 1] = None

            # move the rook for castling
            if curr_piece.name == "K":
                # white castling short
                if curr_x == 4 and curr_y == 0 and next_x == 6 and next_y == 0:
                    self.locations[7][0] = None
                    self.locations[5][0] = piece("W", "R")

                # white castling long
                elif curr_x == 4 and curr_y == 0 and next_x == 2 and next_y == 0:
                    self.locations[0][0] = None
                    self.locations[3][0] = piece("W", "R")

                # black castling short
                if curr_x == 4 and curr_y == 7 and next_x == 6 and next_y == 7:
                    self.locations[7][7] = None
                    self.locations[5][7] = piece("B", "R")

                # black castling long
                elif curr_x == 4 and curr_y == 7 and next_x == 2 and next_y == 7:
                    self.locations[0][7] = None
                    self.locations[3][7] = piece("B", "R")

            # switch the which player's turn it is
            if self.curr_player == "W":
                self.curr_player = "B"
            else:
                self.curr_player = "W"
        else:
            print("this is not a valid move")

    # test if a move is legal
    def is_legal_move(self, curr_x, curr_y, next_x, next_y, curr_piece, next_piece):

        # check to make sure both positions are on the board
        if curr_x > 7 or curr_x < 0:
            return False
        if curr_y > 7 or curr_y < 0:
            return False
        if next_x > 7 or next_x < 0:
            return False
        if next_y > 7 or next_y < 0:
            return False

        # check if the piece at the current move is the current players
        if curr_piece is None or curr_piece.colour != self.curr_player:
            return False

        # check to make sure the next location does not contain a piece of the current player's colour
        # This will also catch trying to move to the current spot
        if next_piece is not None and next_piece.colour == self.curr_player:
            return False

        # todo: check if King would be in check still

        if curr_piece.name == "p":
            return self.is_legal_pawn_move(curr_x, curr_y, next_x, next_y, next_piece)

        elif curr_piece.name == "B":
            return self.is_legal_bishop_move(curr_x, curr_y, next_x, next_y)

        elif curr_piece.name == "N":
            return self.is_legal_knight_move(curr_x, curr_y, next_x, next_y)

        elif curr_piece.name == "R":
            return self.is_legal_rook_move(curr_x, curr_y, next_x, next_y, curr_piece)

        elif curr_piece.name == "Q":
            return self.is_legal_queen_move(curr_x, curr_y, next_x, next_y)

        elif curr_piece.name == "K":
            return self.is_legal_king_move(curr_x, curr_y, next_x, next_y, curr_piece)

        # this should never happen
        else:
            print("You have passed an invalid piece")
            return False

    def is_legal_pawn_move(self, curr_x, curr_y, next_x, next_y, next_piece):

        # white player
        if self.curr_player == "W":

            # reset white passant status
            self.W_passant = None

            # moving one piece forward
            if curr_x == next_x and next_y - curr_y == 1 and next_piece is None:
                return True

            # move two piece forward
            if curr_x == next_x and next_y - curr_y == 2 and next_piece is None and curr_y == 1:
                self.W_passant = curr_x
                return True

            # taking out a piece
            if next_y - curr_y == 1 and abs(curr_x - next_x) == 1 and next_piece is not None and \
                    next_piece.colour == "B":
                return True

            # en passant
            side_piece = self.locations[next_x][next_y - 1]
            if curr_y == 4 and next_y == 5 and abs(next_x - curr_x) == 1 and side_piece is not None and \
                    side_piece.colour == "B" and side_piece.name == "p" and self.B_passant == next_x:
                return True

            # if it is not one of these moves return False
            return False

        # Black's Turn
        elif self.curr_player == "B":

            # reset white passant status
            self.B_passant = None

            # moving one piece forward
            if curr_x == next_x and curr_y - next_y == 1 and next_piece is None:
                return True

            # move two piece forward
            if curr_x == next_x and curr_y - next_y == 2 and next_piece is None and curr_y == 6:
                self.B_passant = curr_x
                return True

            # taking out a piece
            if curr_y - next_y == 1 and abs(curr_x - next_x) == 1 and next_piece is not None and \
                    next_piece.colour == "W":
                return True

            # en passant
            side_piece = self.locations[next_x][next_y + 1]
            if curr_y == 3 and next_y == 2 and abs(next_x - curr_x) == 1 and side_piece is not None and \
                    side_piece.colour == "W" and side_piece.name == "p" and self.A_passant == next_x:
                return True

            # if it is not one of these moves return False
            return False

        # this should never happen
        else:
            print("You have passed an invalid current player")
            return False

    def is_legal_bishop_move(self, curr_x, curr_y, next_x, next_y):

        # if the bishop does not move on a diagonal return False
        if abs(curr_x - next_x) != abs(curr_y - next_y):
            return False

        # check if any of the in between spots have a piece on them
        if next_x > curr_x:
            x_range = range(curr_x + 1, next_x)
        else:
            x_range = range(next_x + 1, curr_x)[::-1]

        if next_y > curr_y:
            y_range = range(curr_y + 1, next_y)
        else:
            y_range = range(next_y + 1, curr_y)[::-1]

        for i in range(abs(curr_x - next_x) - 1):
            if self.locations[x_range[i]][y_range[i]] is not None:
                return False

        # otherwise return True
        return True

    def is_legal_knight_move(self, curr_x, curr_y, next_x, next_y):

        x_diff = abs(curr_x - next_x)
        y_diff = abs(curr_y - next_y)

        if (x_diff == 1 and y_diff == 2) or (x_diff == 2 and y_diff == 1):
            return True
        else:
            return False

    def is_legal_rook_move(self, curr_x, curr_y, next_x, next_y, curr_piece):

        # check if there are any pieces in the way
        if curr_x == next_x:
            if next_y > curr_y:
                y_range = range(curr_y + 1, next_y)
            elif next_y < curr_y:
                y_range = range(next_y + 1, curr_y)[::-1]

            for i in range(abs(curr_y - next_y) - 1):
                if self.locations[next_x][y_range[i]] is not None:
                    return False

        elif curr_y == next_y:
            if next_x > curr_x:
                x_range = range(curr_x + 1, next_x)
            elif next_x < curr_x:
                x_range = range(next_x + 1, curr_x)[::-1]

            for i in range(abs(curr_x - next_x) - 1):
                if self.locations[x_range[i]][next_y] is not None:
                    return False

        # if the move is not on the same rank or file
        else:
            return False

        # track that the rook has moved
        if curr_piece.colour == "W":
            if curr_x == 0 and curr_y == 0:
                self.W_0_Rook_moved = True
            elif curr_x == 7 and curr_y == 0:
                self.W_7_Rook_moved = True

        elif curr_piece.colour == "B":
            if curr_x == 0 and curr_y == 7:
                self.B_0_Rook_moved = True
            elif curr_x == 7 and curr_y == 7:
                self.B_7_Rook_moved = True

        return True

    def is_legal_queen_move(self, curr_x, curr_y, next_x, next_y):

        # check if the queen moves like a rook
        if curr_x == next_x:
            if next_y > curr_y:
                y_range = range(curr_y + 1, next_y)
            elif next_y < curr_y:
                y_range = range(next_y + 1, curr_y)[::-1]

            for i in range(abs(curr_y - next_y) - 1):
                if self.locations[next_x][y_range[i]] is not None:
                    return False
            return True

        elif curr_y == next_y:
            if next_x > curr_x:
                x_range = range(curr_x + 1, next_x)
            elif next_x < curr_x:
                x_range = range(next_x + 1, curr_x)[::-1]

            for i in range(abs(curr_x - next_x) - 1):
                if self.locations[x_range[i]][next_y] is not None:
                    return False
            return True

        # if it doesn't move like a rook does it move like a bishop
        return self.is_legal_bishop_move(curr_x, curr_y, next_x, next_y)

    # and king not in check
    def is_legal_king_move(self, curr_x, curr_y, next_x, next_y, curr_piece):

        # regular king move
        x_diff = abs(curr_x - next_x)
        y_diff = abs(curr_y - next_y)

        if (x_diff == 0 and y_diff == 1) or (x_diff == 1 and y_diff == 0):
            if curr_piece.colour == 'W':
                self.W_King_moved = False
            elif curr_piece.colour == 'B':
                self.B_King_moved = False
            return True

        # white castling short
        if curr_x == 4 and curr_y == 0 and next_x == 6 and next_y == 0:
            # check if King and Rook haven't moved
            if not self.W_King_moved and not self.W_7_Rook_moved and self.locations[5][0] is None and not \
                    self.is_attacked(4, 0, "B") and not self.is_attacked(5, 0, "B") and not self.is_attacked(6, 0, "B"):
                self.W_King_moved = True
                self.W_7_Rook_moved = True
                # todo: check to make sure the King doesn't move through check
                return True

        # white castling long
        elif curr_x == 4 and curr_y == 0 and next_x == 2 and next_y == 0:
            # check if King and Rook haven't moved
            if not self.W_King_moved and not self.W_0_Rook_moved and self.locations[3][0] is None and self.locations[1][0]\
                    and not self.is_attacked(5, 0, "B") is None:
                self.W_King_moved = True
                self.W_0_Rook_moved = True
                # todo: check to make sure the King doesn't move through check
                return True

        # black castling short
        if curr_x == 4 and curr_y == 7 and next_x == 6 and next_y == 7:
            # check if King and Rook haven't moved
            if not self.B_King_moved and not self.B_0_Rook_moved and self.locations[5][7] is None:
                self.B_King_moved = True
                self.B_0_Rook_moved = True
                # todo: check to make sure the King doesn't move through check
                return True

        # black castling long
        elif curr_x == 4 and curr_y == 7 and next_x == 2 and next_y == 7:
            # check if King and Rook haven't moved
            if not self.B_King_moved and not self.B_0_Rook_moved and self.locations[3][7] is None and self.locations[1][7] is None:
                self.B_King_moved = True
                self.B_0_Rook_moved = True
                # todo: check to make sure the King doesn't move through check
                return True

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

    # check if a give postition is being attacked by attackaing_colour
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
        # check if the King is currently attacked and all squares around it are either attacked or contain an opposite colour piece

        return False

    # checks if the player who's turn it is (turn_colour) is in a stalemate
    def is_stalemate(self, turn_colour):
        return False

    # if same position is reached 3 times a player can call a draw

    # if no piece has been captured or pawn moved in 50 turns a player can claim a draw

    # if insuffiencient material for a checkmate the game is a draw

    # 
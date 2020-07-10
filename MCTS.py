# this runs one turn of the MCTS

from board import Game
import numpy as np
import math
import time
import random
import cProfile

class Node:

    def __init__(self, state, move=None, parent=None, expansion=math.sqrt(2), player_turn="B"):

        self.state = state  # this is a game
        self.parent = parent  # this is a node
        self.children = []  # this is a list of nodes
        self.visits = 0
        self.tot_reward = 0  # 1 for a win 0 for a draw -1 for a loss
        self.expansion = expansion  # the expansion co-efficient - higher represents more exploration
        self.player_turn = player_turn  # weather it is white or Blacks turn
        self.move = move  # this logs which move was made for the child node

    def get_UCB(self):
        UCB = self.tot_reward/self.visits + self.expansion*math.sqrt(math.log2(self.parent.visits) / self.visits)
        return UCB

    def is_leaf(self):
        return len(self.children) == 0

    def is_unchecked(self):
        return self.visits == 0

    def get_max_child_UCB(self):

        max_UCB = -999999999
        max_child_index = 99999

        for child in self.children:
            if child.get_UCB() > max_UCB:  # and not child.is_terminal_node():
                max_UCB = child.get_UCB()
                max_child_index = self.children.index(child)

        if max_child_index != 99999:
            return max_child_index
        # This should never happen is only here for testing purposes
        else:
            print("INDEX OUT OF RANGE: max_UCB: {} max_child_index: {}".format(max_UCB, max_child_index))
            print("len(self.children): {}".format(len(self.children)))
            print("player_turn: {}".format(self.player_turn))
            print("is_leaf(): {}".format(self.is_leaf()))
            print("is_terminal_node(): {}".format(self.is_terminal_node()))

            for child in self.children:
                print("get_UCB(): {} is_terminal_node: {}".format(child.get_UCB(), child.is_terminal_node()))

            return max_child_index

    # todo: test
    def back_prop(self, score):
        self.visits += 1

        if self.player_turn == "B":
            self.tot_reward -= score
        else:
            self.tot_reward += score

        if self.parent is not None:
            self.parent.back_prop(score)

    # todo test
    def rollout(self):
        # print("rollout")

        temp_game = self.duplicate_game()

        while True:

            # temp_game.position.display_position("W")

            # if the game is over exit the loop and back prop
            result = temp_game.get_game_result_MCTS()
            if result is not None:

                if result == "D":
                    reward = 0
                elif result == "W":
                    reward = 1
                else:
                    reward = -1

                self.back_prop(reward)
                break

            # otherwise perform a random legal move
            else:

                potential_moves = temp_game.get_potential_moves()

                rand_int = int(len(potential_moves) * random.random())
                rand_move = potential_moves[rand_int]

                while not rand_move.is_legal_move():
                    rand_int = int(len(potential_moves) * random.random())
                    rand_move = potential_moves[rand_int]

                temp_game.move(rand_move.from_x, rand_move.from_y, rand_move.to_x, rand_move.to_y)

    # todo: test
    def expand(self):

        # get all legal moves
        legal_moves = self.state.get_all_legal_moves()

        # create a new game instance for each legal move
        for move in legal_moves:

            temp_game = self.duplicate_game()

            # apply the move
            temp_game.move(move.from_x, move.from_y, move.to_x, move.to_y)

            if self.player_turn == "W":
                new_turn = "B"
            else:
                new_turn = "W"

            # create a child Node based on the position
            child = Node(temp_game, move, self, player_turn=new_turn)
            self.children.append(child)

    # note this should only be run on the parent node
    def get_best_move(self):

        max_visits = 0

        for child in self.children:
            if child.visits > max_visits:
                max_visits = child.visits
                max_move = child.move

        return max_move

    def is_terminal_node(self):
        return self.state.game_is_over()

    # todo: test
    def duplicate_game(self):
        temp_game = Game()

        # copy the position
        for x in [0, 1, 2, 3, 4, 5, 6, 7]:
            for y in [0, 1, 2, 3, 4, 5, 6, 7]:
                temp_game.position.locations[x][y] = self.state.position.locations[x][y]

        temp_game.position.W_King_moved = self.state.position.W_King_moved
        temp_game.position.W_0_Rook_moved = self.state.position.W_0_Rook_moved
        temp_game.position.W_7_Rook_moved = self.state.position.W_7_Rook_moved
        temp_game.position.B_King_moved = self.state.position.B_King_moved
        temp_game.position.B_0_Rook_moved = self.state.position.B_0_Rook_moved
        temp_game.position.B_7_Rook_moved = self.state.position.B_7_Rook_moved
        temp_game.position.W_passant = self.state.position.W_passant
        temp_game.position.B_passant = self.state.position.B_passant
        temp_game.position.W_King_loc = self.state.position.W_King_loc
        temp_game.position.B_King_loc = self.state.position.B_King_loc
        temp_game.position.W_King_check = self.state.position.W_King_check
        temp_game.position.B_King_check = self.state.position.B_King_check

        # copy game attributes
        temp_game.drawing_moves = self.state.drawing_moves
        temp_game.curr_player = self.state.curr_player
        temp_game.opp_player = self.state.opp_player

        # copy the state history
        temp_game.position_history = []
        for history in self.state.position_history:
            temp_game.position_history.append(history)

        return temp_game


# this might be fine as is
def take_next_step(test_node):

    # if the test_node is a leaf expand it
    if test_node.is_leaf():
        test_node.expand()

    # check if any of the children are unexplored, if so explore them
    all_children_checked = True
    for child in test_node.children:
        if child.is_unchecked():
            child.rollout()
            all_children_checked = False

    if all_children_checked:
        if not test_node.is_terminal_node():
            to_exp_child_ind = test_node.get_max_child_UCB()
            to_exp_child = test_node.children[to_exp_child_ind]
            take_next_step(to_exp_child)
        else:
            test_node.rollout()

# this is probably fine
def expand_node(test_node, time_start, max_time):

    # if the test_node is a leaf expand it
    if test_node.is_leaf():
        test_node.expand()

    # check if any of the children are unexplored, if so explore them
    for child in test_node.children:
        if child.is_unchecked():
            child.rollout()

    while time.time() - time_start <= max_time:

        to_exp_child_ind = test_node.get_max_child_UCB()
        to_exp_child = test_node.children[to_exp_child_ind]
        take_next_step(to_exp_child)

def run(exploration_num, max_time, game):

    # get node
    # create a new node based on the board
    test_node = Node(game)

    # expand the tree while I have time
    time_start = time.time()
    expand_node(test_node, time_start, max_time)

    # pick the next best move
    next_move = test_node.get_best_move()

    print("move: {}".format(next_move.move_to_str()))

    for child in test_node.children:
        print("child {} visits: {} total: {} avg: {}".format(child.move.move_to_str(), child.visits, child.tot_reward, child.tot_reward/child.visits))

    return next_move

if __name__ == "__main__":
    pr = cProfile.Profile()
    pr.enable()
    exploration_num = 2  # currently using sqrt(2) as default
    max_time = 10  # in seconds
    run(exploration_num, max_time)
    pr.disable()
    pr.print_stats()

import argparse
import copy
import sys
import time
import math


# cache = set()  # you can use this to implement state caching!


class State:
    # This class is used to represent a state.
    # board : a list of lists that represents the 8*8 board
    def __init__(self, board, player_round):

        self.board = copy.deepcopy(board)
        self.player_round = player_round  # whether is player's round. Default value is True.

        self.width = 8
        self.height = 8

    def display(self):
        for i in self.board:
            for j in i:
                print(j, end="")
            print("")
        print("")

    def change_player_round(self, update):
        # place the chess at this position
        self.player_round = update

    def is_terminal(self):
        # check whether the state is terminal state:
        status = self.check_chess_number()
        if (status['red_small'] + status['red_king'] == 0) or (status['black_small'] + status['black_king'] == 0)\
                or self.decision() == []:
            return True
        else:
            return False

    def get(self, r, c):
        # get the current state of the given position.
        return self.board[r][c]

    def check_chess_number(self):
        # calculate chesses for future purpose.
        number_status = {"red_small": 0, "red_king": 0, "black_small": 0, "black_king": 0}
        for i in range(8):
            for j in range(8):
                if self.get(i, j) == "r":
                    number_status["red_small"] += 1
                if self.get(i, j) == "R":
                    number_status["red_king"] += 1
                if self.get(i, j) == "b":
                    number_status["black_small"] += 1
                if self.get(i, j) == "B":
                    number_status["black_king"] += 1
        return number_status

    def become_king(self):
        # maybe useless? IDK. Just make sure our chess board is valid. Call it before making changes to state.
        for j in range(8):
            if self.get(0, j) == "r":
                self.board[0][j] = "R"
            if self.get(7, j) == "b":
                self.board[7][j] = "B"

    def move_up_left(self, row, col):
        # move the red chess or black king chess with up_left.
        if row > 0 and col > 0 and self.board[row - 1][col - 1] == '.':
            if self.player_round is True:  # currently is our round, move red chess
                if self.board[row][col] == 'r':
                    successor = State(self.board, not self.player_round)
                    if row == 1:  # become king dude
                        successor.board[row][col] = '.'
                        successor.board[row - 1][col - 1] = 'R'
                    else:
                        successor.board[row][col] = '.'
                        successor.board[row - 1][col - 1] = 'r'
                    return successor
                if self.board[row][col] == 'R':
                    successor = State(self.board, not self.player_round)
                    successor.board[row][col] = '.'
                    successor.board[row - 1][col - 1] = 'R'
                    return successor
            else:  # is black move dude, but only B can make this move
                if self.board[row][col] == 'B':
                    successor = State(self.board, not self.player_round)
                    successor.board[row][col] = '.'
                    successor.board[row - 1][col - 1] = 'B'
                    return successor

    def move_up_right(self, row, col):
        # move the red chess or black king chess with up_right. it has similar logic with move_up_left
        if row > 0 and col < 7 and self.board[row - 1][col + 1] == '.':
            if self.player_round is True:
                if self.board[row][col] == 'r':
                    successor = State(self.board, not self.player_round)
                    if row == 1:
                        successor.board[row - 1][col + 1] = 'R'
                        successor.board[row][col] = '.'
                    else:
                        successor.board[row - 1][col + 1] = 'r'
                        successor.board[row][col] = '.'
                    return successor
                if self.board[row][col] == 'R':
                    successor = State(self.board, not self.player_round)
                    successor.board[row][col] = '.'
                    successor.board[row - 1][col + 1] = 'R'
                    return successor
            else:
                if self.board[row][col] == 'B':
                    successor = State(self.board, not self.player_round)
                    successor.board[row][col] = '.'
                    successor.board[row - 1][col + 1] = 'B'
                    return successor

    def move_down_left(self, row, col):
        if row < 7 and col > 0 and self.board[row + 1][col - 1] == '.':
            if self.player_round is True:
                if self.board[row][col] == 'R':
                    successor = State(self.board, not self.player_round)
                    successor.board[row][col] = '.'
                    successor.board[row + 1][col - 1] = 'R'
                    return successor
            else:
                if self.board[row][col] == 'B':
                    successor = State(self.board, not self.player_round)
                    successor.board[row][col] = '.'
                    successor.board[row + 1][col - 1] = 'B'
                    return successor
                if self.board[row][col] == 'b':
                    successor = State(self.board, not self.player_round)
                    if row != 6:
                        successor.board[row][col] = '.'
                        successor.board[row + 1][col - 1] = 'b'
                    else:
                        successor.board[row][col] = '.'
                        successor.board[row + 1][col - 1] = 'B'
                    return successor

    def move_down_right(self, row, col):
        if row < 7 and col < 7 and self.board[row + 1][col + 1] == '.':
            if self.player_round is True:
                if self.board[row][col] == "R":
                    successor = State(self.board, not self.player_round)
                    successor.board[row][col] = '.'
                    successor.board[row + 1][col + 1] = 'R'
                    return successor
            else:
                if self.board[row][col] == 'B':
                    successor = State(self.board, not self.player_round)
                    successor.board[row][col] = '.'
                    successor.board[row + 1][col + 1] = "B"
                    return successor
                if self.board[row][col] == 'b':
                    successor = State(self.board, not self.player_round)
                    if row == 6:
                        successor.board[row][col] = '.'
                        successor.board[row + 1][col + 1] = 'B'
                    else:
                        successor.board[row][col] = '.'
                        successor.board[row + 1][col + 1] = 'b'
                    return successor

    def double_up_left(self, row, col):
        if row >= 2 and col >= 2 and self.board[row - 2][col - 2] == '.':
            if self.player_round is True:
                if self.board[row][col] == 'r' and (
                        self.board[row - 1][col - 1] == 'b' or self.board[row - 1][col - 1] == 'B'):
                    successor = State(self.board, not self.player_round)
                    # if row == 2:  # change to King.
                    #     successor.board[row][col] = '.'
                    #     successor.board[row - 1][col - 1] = '.'
                    #     successor.board[row - 2][col - 2] = 'R'
                    # else:
                    successor.board[row][col] = '.'
                    successor.board[row - 1][col - 1] = '.'
                    successor.board[row - 2][col - 2] = 'r'
                    return successor
                if self.board[row][col] == 'R' and (
                        self.board[row - 1][col - 1] == 'b' or self.board[row - 1][col - 1] == 'B'):
                    successor = State(self.board, not self.player_round)
                    successor.board[row][col] = '.'
                    successor.board[row - 1][col - 1] = '.'
                    successor.board[row - 2][col - 2] = 'R'
                    return successor
            else:
                if self.board[row][col] == 'B' and (
                        self.board[row - 1][col - 1] == 'r' or self.board[row - 1][col - 1] == 'R'):
                    successor = State(self.board, not self.player_round)
                    successor.board[row][col] = '.'
                    successor.board[row - 1][col - 1] = '.'
                    successor.board[row - 2][col - 2] = 'B'
                    return successor

    def double_up_right(self, row, col):
        if row >= 2 and col <= 5 and self.board[row - 2][col + 2] == '.':
            if self.player_round is True:
                if self.board[row][col] == 'r' and (
                        self.board[row - 1][col + 1] == 'b' or self.board[row - 1][col + 1] == 'B'):
                    successor = State(self.board, not self.player_round)
                    # if row == 2:
                    #     successor.board[row][col] = '.'
                    #     successor.board[row - 1][col + 1] = '.'
                    #     successor.board[row - 2][col + 2] = 'R'
                    # else:
                    successor.board[row][col] = '.'
                    successor.board[row - 1][col + 1] = '.'
                    successor.board[row - 2][col + 2] = 'r'
                    return successor
                if self.board[row][col] == 'R' and (
                        self.board[row - 1][col + 1] == 'b' or self.board[row - 1][col + 1] == 'B'):
                    successor = State(self.board, not self.player_round)
                    successor.board[row][col] = '.'
                    successor.board[row - 1][col + 1] = '.'
                    successor.board[row - 2][col + 2] = 'R'
                    return successor
            else:
                if self.board[row][col] == 'B' and (
                        self.board[row - 1][col + 1] == 'r' or self.board[row - 1][col + 1] == 'R'):
                    successor = State(self.board, not self.player_round)
                    successor.board[row][col] = '.'
                    successor.board[row - 1][col + 1] = '.'
                    successor.board[row - 2][col + 2] = 'B'
                    return successor

    def double_down_left(self, row, col):
        if row <= 5 and col >= 2 and self.board[row + 2][col - 2] == '.':
            if self.player_round:
                if self.board[row][col] == 'R' and (
                        self.board[row + 1][col - 1] == 'b' or self.board[row + 1][col - 1] == 'B'):
                    successor = State(self.board, not self.player_round)
                    successor.board[row][col] = '.'
                    successor.board[row + 1][col - 1] = '.'
                    successor.board[row + 2][col - 2] = 'R'
                    return successor
            else:
                if self.board[row][col] == 'b' and (
                        self.board[row + 1][col - 1] == 'r' or self.board[row + 1][col - 1] == 'R'):
                    successor = State(self.board, not self.player_round)
                    successor.board[row][col] = '.'
                    successor.board[row + 1][col - 1] = '.'
                    # if row == 5:
                    #     successor.board[row + 2][col - 2] = 'B'
                    # else:
                    successor.board[row + 2][col - 2] = 'b'
                    return successor
                if self.board[row][col] == 'B' and (
                        self.board[row + 1][col - 1] == 'r' or self.board[row + 1][col - 1] == 'R'):
                    successor = State(self.board, not self.player_round)
                    successor.board[row][col] = '.'
                    successor.board[row + 1][col - 1] = '.'
                    successor.board[row + 2][col - 2] = 'B'
                    return successor

    def double_down_right(self, row, col):
        if row <= 5 and col <= 5 and self.board[row + 2][col + 2] == '.':
            if self.player_round:
                if self.board[row][col] == 'R' and (
                        self.board[row + 1][col + 1] == 'b' or self.board[row + 1][col + 1] == 'B'):
                    successor = State(self.board, not self.player_round)
                    successor.board[row][col] = '.'
                    successor.board[row + 1][col + 1] = '.'
                    successor.board[row + 2][col + 2] = 'R'
                    return successor
            else:
                if self.board[row][col] == 'b' and (
                        self.board[row + 1][col + 1] == 'r' or self.board[row + 1][col + 1] == 'R'):
                    successor = State(self.board, not self.player_round)
                    successor.board[row][col] = '.'
                    successor.board[row + 1][col + 1] = '.'
                    # if row == 5:
                    #     successor.board[row + 2][col + 2] = 'B'
                    # else:
                    successor.board[row + 2][col + 2] = 'b'
                    return successor
                if self.board[row][col] == 'B' and (
                        self.board[row + 1][col + 1] == 'r' or self.board[row + 1][col + 1] == 'R'):
                    successor = State(self.board, not self.player_round)
                    successor.board[row][col] = '.'
                    successor.board[row + 1][col + 1] = '.'
                    successor.board[row + 2][col + 2] = 'B'
                    return successor

    def normal_moves_for_board(self, row, column):
        possible_states = []
        up_right = self.move_up_right(row, column)
        up_left = self.move_up_left(row, column)
        down_right = self.move_down_right(row, column)
        down_left = self.move_down_left(row, column)
        if up_right is not None:
            possible_states.append(up_right)
        if up_left is not None:
            possible_states.append(up_left)
        if down_right is not None:
            possible_states.append(down_right)
        if down_left is not None:
            possible_states.append(down_left)
        return possible_states

    def jump_checking(self, i, j):
        # this function is for checking whether the current chess can make a jump. Force for multiple jump
        if self.double_down_left(i, j) is not None or self.double_down_right(i, j) is not None:
            return True
        if self.double_up_right(i, j) is not None or self.double_up_left(i, j) is not None:
            return True
        return False  # there does not have any jump possibility.

    def double_moves_for_board(self, row, column, first=True):
        # for variable first: we do not add the very first board in our state, we want to add the not-first board.
        states = []
        if self.jump_checking(row, column) is False and first is False:  # add the final jump case to states.
            states.append(self)
        possible1 = self.double_up_left(row, column)
        possible2 = self.double_up_right(row, column)
        possible3 = self.double_down_right(row, column)
        possible4 = self.double_down_left(row, column)
        # the following iterations are finding the multiple jump and add the last board.
        if possible1 is not None:
            possible1.change_player_round(self.player_round)
            states += possible1.double_moves_for_board(row - 2, column - 2, first=False)
        if possible2 is not None:
            possible2.change_player_round(self.player_round)
            states += possible2.double_moves_for_board(row - 2, column + 2, first=False)
        if possible3 is not None:
            possible3.change_player_round(self.player_round)
            states += possible3.double_moves_for_board(row + 2, column + 2, first=False)
        if possible4 is not None:
            possible4.change_player_round(self.player_round)
            states += possible4.double_moves_for_board(row + 2, column - 2, first=False)
        # After performing all the multiple jumps, we change the player round. We need to make sure each state's player
        # round is correct.
        result = []
        for state in states:
            state.become_king()
            new_state = State(state.board, not self.player_round)
            result.append(new_state)
        return result

    def decision(self):
        single_move, jump_move = [], []
        for i in range(8):
            for j in range(8):
                single_move += self.normal_moves_for_board(i, j)
                jump_move += self.double_moves_for_board(i, j)
        if jump_move != []:
            return jump_move  # force to jump
        else:
            return single_move

    def calculate_heuristic(self):
        chess_dict = self.check_chess_number()
        utility = (2 * chess_dict["red_king"] + chess_dict["red_small"]) - (
                2 * chess_dict["black_king"] + chess_dict["black_small"])
        return utility

    def alpha_beta(self, cache, alpha=-math.inf, beta=math.inf, depth=8):
        if depth == 0 or self.is_terminal():
            return self.calculate_heuristic(), None

        board = convert_board_to_result(self)
        if board in cache:
            return cache[board], None

        if self.player_round:
            max_value = -math.inf
            best_move = None
            actions = self.decision()
            actions.sort(key=lambda x: x.calculate_heuristic())
            actions.reverse()
            for move in actions:
                value, _ = move.alpha_beta(cache, alpha, beta, depth - 1)
                if value > max_value:
                    max_value = value
                    best_move = move
                alpha = max(alpha, value)
                if beta <= alpha:
                    break

            cache[board] = max_value
            return max_value, best_move
        else:
            min_value = math.inf
            best_move = None
            actions = self.decision()
            actions.sort(key=lambda x: x.calculate_heuristic())
            for move in actions:
                value, _ = move.alpha_beta(cache, alpha, beta, depth - 1)
                if value < min_value:
                    min_value = value
                    best_move = move
                beta = min(beta, value)
                if beta <= alpha:
                    break

            cache[board] = min_value
            return min_value, best_move


def read_from_file(filename):
    f = open(filename)
    lines = f.readlines()
    board = [[str(x) for x in l.rstrip()] for l in lines]
    f.close()
    state = State(board, True)
    return state


def convert_board_to_result(board):
    result_strings = ""
    for i in range(8):
        j = 0
        while j < 8:
            result_strings += board.board[i][j]
            j += 1
        result_strings += "\n"

    return result_strings


def write_to_file(output_file, list_of_result):
    output = open(output_file, "w")
    for result_board in list_of_result:
        output.write(convert_board_to_result(result_board))
        output.write("\n")
    output.close()


def Perform(input_file, output_file):
    init_state = read_from_file(input_file)
    result_list = []
    result_list.append(init_state)
    next_successor = init_state.alpha_beta({})[1]
    result_list.append(next_successor)
    while next_successor is not None:
        store = next_successor.alpha_beta({})
        next_successor = store[1]
        print(next_successor)
        if next_successor is not None:
            result_list.append(next_successor)
    write_to_file(output_file, result_list)


# # Below functions are my test functions for each important steps: like jump moves, detacting multiple jumps and making
# decision. 
def test_decision(input_file, output_file='testdecision.txt'):
    init_state = read_from_file(input_file)
    decision = init_state.decision()
    # for i in decision:
    #     print(i.player_round)
    write_to_file(output_file, decision)


def test_jump_correctness(input_file, output_file='jumptest.txt'):
    init_state = read_from_file(input_file)
    jump_list = []
    for i in range(8):
        for j in range(8):
            jump_list += init_state.double_moves_for_board(i, j)
    if jump_list == []:
        jump_list.append(init_state)
    write_to_file(output_file, jump_list)


def test_single_jump(input_file, output_file='singlejumptest.txt'):
    init_state = read_from_file(input_file)
    state_list = []
    after_move1 = init_state.double_up_left(2, 5)
    after_move2 = init_state.double_up_right(2, 5)
    after_move3 = init_state.double_down_left(2, 5)
    after_move4 = init_state.double_down_right(2, 5)
    if after_move1 is not None:
        state_list.append(after_move1)
    if after_move2 is not None:
        state_list.append(after_move2)
    if after_move3 is not None:
        state_list.append(after_move3)
    if after_move4 is not None:
        state_list.append(after_move4)
    write_to_file(output_file, state_list)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inputfile",
        type=str,
        required=True,
        help="The input file that contains the puzzles."
    )
    parser.add_argument(
        "--outputfile",
        type=str,
        required=True,
        help="The output file that contains the solution."
    )
    args = parser.parse_args()

    Perform(args.inputfile, args.outputfile)
    # test_decision(args.inputfile)
    # test_jump_correctness(args.inputfile)
    # test_single_jump(args.inputfile)

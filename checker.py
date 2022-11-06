# csc384 assignment 2
# BY Yiteng Sun
import copy
import math
import sys


class Board:
    # In this class, we will define a 8x8 empty board.
    def __init__(self, content):
        self.length = 8
        self.content = copy.deepcopy(content)
        # the type of content should be List[list]

    def place(self, r, c, chess):
        # place the chess at this position
        self.content[r][c] = chess

    def make_empty(self, r, c):
        # After the chess is removed, its original place will be empty.
        self.content[r][c] = "."

    def get(self, r, c):
        # get the current state of the given position.
        return self.content[r][c]

    def check_chess_number(self):
        # initialize
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
        for j in range(8):
            if self.get(0, j) == "r":
                self.content[0][j] = "R"
            if self.get(7, j) == "b":
                self.content[7][j] = "B"


def read_file():
    file_name = sys.argv[1]
    file = open(file_name, "r")
    init_board = Board([[0, 0, 0, 0, 0, 0, 0, 0] for i in range(8)])
    curr_line = 0
    while (1):
        line = file.readline()
        if not line:
            break

        for i in range(0, 8):
            item = line[i]
            init_board.content[curr_line][i] = item

        curr_line += 1

    file.close()
    return init_board


def convert_board_to_result(board):
    result_strings = ""
    for i in range(8):
        j = 0
        while j < 8:
            result_strings += board.content[i][j]
            j += 1
        result_strings += "\n"

    return result_strings


def check_move(board, next_row, next_column):
    if next_row < 0 or next_row > 7:
        return False
    if next_column < 0 or next_column > 7:
        return False
    if board.get(next_row, next_column) != ".":
        return False
    else:
        return True


def available_red_moves(board):
    moves_list = []
    for row in range(8):
        for column in range(8):
            if board.get(row, column) == "r":
                if check_move(board, row - 1, column + 1):
                    moves_list.append([row, column, row - 1, column + 1])
                if check_move(board, row - 1, column - 1):
                    moves_list.append([row, column, row - 1, column - 1])
            if board.get(row, column) == "R":
                if check_move(board, row - 1, column + 1):
                    moves_list.append([row, column, row - 1, column + 1])
                if check_move(board, row - 1, column - 1):
                    moves_list.append([row, column, row - 1, column - 1])
                if check_move(board, row + 1, column + 1):
                    moves_list.append([row, column, row + 1, column + 1])
                if check_move(board, row + 1, column - 1):
                    moves_list.append([row, column, row + 1, column - 1])
    return moves_list


def available_black_moves(board):
    moves_list = []
    for row in range(8):
        for column in range(8):
            if board.get(row, column) == "b":
                if check_move(board, row + 1, column + 1):
                    moves_list.append([row, column, row + 1, column + 1])
                if check_move(board, row + 1, column - 1):
                    moves_list.append([row, column, row + 1, column - 1])
            if board.get(row, column) == "B":
                if check_move(board, row - 1, column + 1):
                    moves_list.append([row, column, row - 1, column + 1])
                if check_move(board, row - 1, column - 1):
                    moves_list.append([row, column, row - 1, column - 1])
                if check_move(board, row + 1, column + 1):
                    moves_list.append([row, column, row + 1, column + 1])
                if check_move(board, row + 1, column - 1):
                    moves_list.append([row, column, row + 1, column - 1])
    return moves_list


def make_moves(board, moves_list):
    successor_boards = []
    for moves_pair in moves_list:
        successor_board = Board(board.content)
        chess = successor_board.get(moves_pair[0], moves_pair[1])
        successor_board.place(moves_pair[2], moves_pair[3], chess)
        successor_board.make_empty(moves_pair[0], moves_pair[1])
        successor_board.become_king()
        successor_boards.append(successor_board)
    return successor_boards


def check_red_jump(board, mid_position, final_position):
    if mid_position[0] < 0 or mid_position[0] > 7:  # mid_row < 0 and mid_row > 7:
        return False
    if mid_position[1] < 0 or mid_position[1] > 7:  # mid_column < 0 and mid_column > 7:
        return False
    if final_position[0] < 0 or final_position[0] > 7:  # mid_row < 0 and mid_row > 7:
        return False
    if final_position[1] < 0 or final_position[1] > 7:  # mid_column < 0 and mid_column > 7:
        return False
    # if its upright or upleft position has the same color chess or no chess, can't jump
    if board.get(mid_position[0], mid_position[1]) != "b" and board.get(mid_position[0], mid_position[1]) != "B":
        return False
    # if its final_position have a chess to block its road, can't jump.
    if board.get(final_position[0], final_position[1]) != ".":
        return False
    return True


def check_black_jump(board, mid_position, final_position):
    if mid_position[0] < 0 or mid_position[0] > 7:  # mid_row < 0 and mid_row > 7:
        return False
    if mid_position[1] < 0 or mid_position[1] > 7:  # mid_column < 0 and mid_column > 7:
        return False
    if final_position[0] < 0 or final_position[0] > 7:  # mid_row < 0 and mid_row > 7:
        return False
    if final_position[1] < 0 or final_position[1] > 7:  # mid_column < 0 and mid_column > 7:
        return False
    # if its upright or upleft position has the same color chess or no chess, can't jump
    if board.get(mid_position[0], mid_position[1]) != "r" and board.get(mid_position[0], mid_position[1]) != "R":
        return False
    # if its final_position have a chess to block its road, can't jump.
    if board.get(final_position[0], final_position[1]) != ".":
        return False
    return True


def available_red_jump(board):
    jumps_list = []
    for row in range(8):
        for column in range(8):
            if board.get(row, column) == "r":
                if check_red_jump(board, (row - 1, column + 1), (row - 2, column + 2)):
                    jumps_list.append([row, column, row - 1, column + 1, row - 2, column + 2])
                if check_red_jump(board, (row - 1, column - 1), (row - 2, column - 2)):
                    jumps_list.append([row, column, row - 1, column - 1, row - 2, column - 2])
            if board.get(row, column) == "R":
                if check_red_jump(board, (row - 1, column + 1), (row - 2, column + 2)):
                    jumps_list.append([row, column, row - 1, column + 1, row - 2, column + 2])
                if check_red_jump(board, (row - 1, column - 1), (row - 2, column - 2)):
                    jumps_list.append([row, column, row - 1, column - 1, row - 2, column - 2])
                if check_red_jump(board, (row + 1, column - 1), (row + 2, column - 2)):
                    jumps_list.append([row, column, row + 1, column - 1, row + 2, column - 2])
                if check_red_jump(board, (row + 1, column + 1), (row + 2, column + 2)):
                    jumps_list.append([row, column, row + 1, column + 1, row + 2, column + 2])

    return jumps_list


def available_black_jump(board):
    jumps_list = []
    for row in range(8):
        for column in range(8):
            if board.get(row, column) == "b":
                if check_black_jump(board, (row + 1, column + 1), (row + 2, column + 2)):
                    jumps_list.append([row, column, row + 1, column + 1, row + 2, column + 2])
                if check_black_jump(board, (row + 1, column - 1), (row + 2, column - 2)):
                    jumps_list.append([row, column, row + 1, column - 1, row + 2, column - 2])
            if board.get(row, column) == "B":
                if check_black_jump(board, (row - 1, column + 1), (row - 2, column + 2)):
                    jumps_list.append([row, column, row - 1, column + 1, row - 2, column + 2])
                if check_black_jump(board, (row - 1, column - 1), (row - 2, column - 2)):
                    jumps_list.append([row, column, row - 1, column - 1, row - 2, column - 2])
                if check_black_jump(board, (row + 1, column - 1), (row + 2, column - 2)):
                    jumps_list.append([row, column, row + 1, column - 1, row + 2, column - 2])
                if check_black_jump(board, (row + 1, column + 1), (row + 2, column + 2)):
                    jumps_list.append([row, column, row + 1, column + 1, row + 2, column + 2])

    return jumps_list


def make_jumps(board, jumps_list):
    successor_boards = []
    for jumps_pair in jumps_list:
        successor_board = Board(board.content)
        chess = successor_board.get(jumps_pair[0], jumps_pair[1])
        successor_board.place(jumps_pair[4], jumps_pair[5], chess)
        successor_board.make_empty(jumps_pair[0], jumps_pair[1])
        successor_board.make_empty(jumps_pair[2], jumps_pair[3])
        successor_board.become_king()
        successor_boards.append(successor_board)
    return successor_boards


def all_successors(board, color):
    successors = []
    if color == "r":
        move_list = available_red_moves(board)
        jump_list = available_red_jump(board)
        successors += make_moves(board, move_list)
        successors += make_jumps(board, jump_list)
    if color == "b":
        move_list = available_black_moves(board)
        successors += make_moves(board, move_list)
        jump_list = available_black_jump(board)
        successors += make_jumps(board, jump_list)

    return successors


def calculating_heuristic(board):
    chess_status = board.check_chess_number()
    return (2 * chess_status["red_king"] + chess_status["red_small"]) - \
           (2 * chess_status["black_king"] + chess_status["black_small"])


def terminal_state(board):
    chess_status = board.check_chess_number()
    if chess_status["red_king"] + chess_status["red_small"] == 0:
        return True
    if chess_status["black_king"] + chess_status["black_small"] == 0:
        return True
    if len(all_successors(board, "r")) == 0:
        return True
    if len(all_successors(board, "b")) == 0:
        return True

    return False


def minimax(board, depth, maximize_player):
    if depth == 0 or terminal_state(board):
        return board, calculating_heuristic(board)
    if maximize_player:
        max_value = -math.inf
        max_state = None
        successors = all_successors(board, "r")
        for successor in successors:
            curr_state, curr_heuristic = minimax(successor, depth - 1, False)
            max_value = max(curr_heuristic, max_value)
            if max_value == curr_heuristic:
                max_state = successor
        return max_state, max_value
    else:
        min_value = math.inf
        min_state = None
        successors = all_successors(board, 'b')
        for successor in successors:
            curr_state, curr_heuristic = minimax(successor, depth - 1, True)
            min_value = min(curr_heuristic, min_value)
            if min_value == curr_heuristic:
                min_state = successor
        return min_state, min_value


def alpha_beta_minimax(board, depth, alpha, beta, maximize_player):
    chess_status = board.check_chess_number()
    if depth == 0 or (chess_status["red_king"] + chess_status["red_small"] == 0) or \
            (chess_status["black_king"] + chess_status["black_small"] == 0) or len(all_successors(board, 'r')) == 0 or \
            len(all_successors(board, 'b')) == 0:
        return board, calculating_heuristic(board)
    if maximize_player:
        best_value = -math.inf
        max_state = None
        successors = all_successors(board, "r")
        for successor in successors:
            curr_state, curr_heuristic = alpha_beta_minimax(successor, depth - 1, alpha, beta, False)
            best_value = max(best_value, curr_heuristic)
            alpha = max(alpha, curr_heuristic)
            if beta <= alpha:
                break
            if best_value == curr_heuristic:
                max_state = successor
        return max_state, best_value
    else:
        best_value = math.inf
        min_state = None
        successors = all_successors(board, 'b')
        for successor in successors:
            curr_state, curr_heuristic = alpha_beta_minimax(successor, depth - 1, alpha, beta, True)
            best_value = min(best_value, curr_heuristic)
            beta = min(beta, curr_heuristic)
            if beta <= alpha:
                break
            if best_value == curr_heuristic:
                min_state = successor
        return min_state, best_value


def print_result(solution):
    file_name = sys.argv[2]
    output_file = open(file_name, "w")
    output_file.write(convert_board_to_result(solution))
    output_file.close()


if __name__ == "__main__":
    board = read_file()
    print("Going through the result")
    state, value = alpha_beta_minimax(board, 6, -math.inf, math.inf, maximize_player=True)
    print_result(state)

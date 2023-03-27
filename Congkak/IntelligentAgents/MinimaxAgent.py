import copy
import math
import random
from Congkak.CongkakBoardModel import BoardModel
from Congkak.Hand import Hand

class MinimaxAgent:

    # h1 = maximise counters on players side
    # h2 = maximise the number of houses with counters in them
    # h3 = maximise the counters in the player's storeroom
    # h4 = minimise the counters in the opponent's storeroom
    # h5 = maximise the number of chain moves
    # h6 = maximise the difference between the player's and opponent's storeroom
    # h7 =

    def __init__(self, weights, maximum_depth, maximum_self_depth, maximum_number_node):
        self.final_best_value = 1
        self.final_best_move = 0
        self.board_model = BoardModel()

        self.maximum_depth = maximum_depth
        self.maximum_self_depth = maximum_self_depth
        self.maximum_number_of_node = maximum_number_node

        self.node_count = 0
        self.leaf_node_count = 0
        self.checked_opponent = False

        self.heuristics_weights = range(6)

        for weight in weights:
            self.heuristics_weights = weight

        pass

    def choose_move(self, player, board_model):

        self.node_count = 0
        self.leaf_node_count = 0
        self.checked_opponent = False

        final_best_move = 0
        available_moves = board_model.available_moves(player)
        board_model.sowing_speed = 0
        board_model.game_phase = BoardModel.SEQUENTIAL_PHASE
        board_model.ping = False

        board_model.reset_hand('a')
        board_model.reset_hand('b')
        board_model.player_a_status = BoardModel.STOP_SOWING_A
        board_model.player_b_status = BoardModel.STOP_SOWING_B

        final_best_value = 0
        if player == 'a':
            final_best_value = -math.inf
            board_model.last_active_player = 'b'
        elif player == 'b':
            final_best_value = math.inf
            board_model.last_active_player = 'a'

        optimal_board = BoardModel()

        for move in available_moves:
            self.checked_opponent = False
            new_board = copy.deepcopy(board_model)
            evaluation, board = self.minimax(board_model=new_board, move=move, depth=self.maximum_depth, self_depth=self.maximum_self_depth, player=player, alpha=-math.inf, beta=math.inf)

            if player == 'a' and (evaluation >= final_best_value):
                final_best_value = evaluation
                final_best_move = move
                optimal_board = board
            elif player == 'b' and (evaluation <= final_best_value):
                final_best_value = evaluation
                final_best_move = move
                optimal_board = board

            # print("total nodes searched: " + str(self.node_count) + " leaf nodes reached: " + str(self.leaf_node_count))
            # print("optimal board so far: ")
            # optimal_board.print_all_data()

        # print("optimal board: ")
        # optimal_board.print_all_data()
        print("minimax: total nodes searched: " + str(self.node_count) + " leaf nodes reached: " + str(self.leaf_node_count))

        return final_best_move

    def minimax(self, board_model, move, depth, self_depth, player, alpha, beta):

        self.node_count += 1

        if self.node_count % 100 == 0:
            print("total nodes searched: " + str(self.node_count))

        optimal_board = BoardModel()

        if depth == 0 or self_depth == 0:
            # print("depth reached")
            self.leaf_node_count += 1
            return self.evaluate_position(board_model, player), board_model

        hole = 0
        if player == 'a':
            hole = move + 10
        elif player == 'b':
            hole = move + 20

        new_hand = Hand(player=player, hole_pos=hole, counter_count=0)
        board_model.iterate_sowing(new_hand)
        available_moves = board_model.available_moves(player)

        if depth == 0 or len(available_moves) == 0:
            self.leaf_node_count += 1
            return self.evaluate_position(board_model, player), board_model

        if player == 'a':
            max_eva = -math.inf

            match board_model.action_to_take():

                case BoardModel.PROMPT_SOWING_BOTH: # similar to prompt sowing a
                    available_moves = board_model.available_moves('a')
                    for move in available_moves:
                        new_board = copy.deepcopy(board_model)

                        if not self.checked_opponent:
                            depth += 1
                        # else:
                        #     self_depth += 1

                        eva, board = self.minimax(new_board, move, depth - 1, self_depth - 1, 'a', alpha, beta)
                        if eva > max_eva:
                            max_eva = eva
                            optimal_board = board
                        max_eva = max(max_eva, eva)
                        alpha = max(alpha, max_eva)
                        if beta <= alpha:
                            break

                case BoardModel.PROMPT_SOWING_A:
                    available_moves = board_model.available_moves('a')
                    for move in available_moves:
                        new_board = copy.deepcopy(board_model)

                        if not self.checked_opponent:
                            depth += 1

                        eva, board = self.minimax(new_board, move, depth - 1, self_depth - 1, 'a', alpha, beta)
                        if eva > max_eva:
                            max_eva = eva
                            optimal_board = board
                        max_eva = max(max_eva, eva)
                        alpha = max(alpha, max_eva)
                        if beta <= alpha:
                            break

                case BoardModel.PROMPT_SOWING_B:
                    available_moves = board_model.available_moves('b')
                    for move in available_moves:
                        new_board = copy.deepcopy(board_model)

                        self.checked_opponent = True

                        eva, board = self.minimax(new_board, move, depth - 1, self_depth - 1, 'b', alpha, beta)
                        if eva > max_eva:
                            max_eva = eva
                            optimal_board = board
                        max_eva = max(max_eva, eva)
                        alpha = max(alpha, max_eva)
                        if beta <= alpha:
                            break

            return max_eva, optimal_board

        elif player == 'b':

            min_eva = math.inf

            match board_model.action_to_take():

                case BoardModel.PROMPT_SOWING_BOTH:  # similar to prompt sowing b
                    available_moves = board_model.available_moves('b')
                    for move in available_moves:
                        new_board = copy.deepcopy(board_model)

                        if not self.checked_opponent:
                            depth += 1

                        eva, board = self.minimax(new_board, move, depth - 1, self_depth - 1, 'b', alpha, beta)
                        if eva < min_eva:
                            min_eva = eva
                            optimal_board = board
                        min_eva = min(min_eva, eva)
                        beta = min(beta, min_eva)
                        if beta <= alpha:
                            break

                case BoardModel.PROMPT_SOWING_A:
                    available_moves = board_model.available_moves('a')
                    for move in available_moves:
                        new_board = copy.deepcopy(board_model)

                        self.checked_opponent = True

                        eva, board = self.minimax(new_board, move, depth - 1, self_depth - 1, 'a', alpha, beta)
                        if eva < min_eva:
                            min_eva = eva
                            optimal_board = board
                        min_eva = min(min_eva, eva)
                        beta = min(beta, min_eva)
                        if beta <= alpha:
                            break

                case BoardModel.PROMPT_SOWING_B:
                    available_moves = board_model.available_moves('b')
                    for move in available_moves:
                        new_board = copy.deepcopy(board_model)

                        if not self.checked_opponent:
                            depth += 1

                        eva, board = self.minimax(new_board, move, depth - 1, self_depth - 1, 'b', alpha, beta)
                        if eva < min_eva:
                            min_eva = eva
                            optimal_board = board
                        min_eva = min(min_eva, eva)
                        beta = min(beta, min_eva)
                        if beta <= alpha:
                            break

            return min_eva, optimal_board

    # def new_minimax(self, board_model, move, depth, player):
    #
    #     hole = 0
    #
    #     best_value = 0
    #
    #     if player == 'a':
    #         best_value = -math.inf
    #     elif player == 'b':
    #         best_value = math.inf
    #
    #     if player == 'a':
    #         hole = move + 10
    #     elif player == 'b':
    #         hole = move + 20
    #
    #     print("player: " + str(player) + " depth: " + str(depth))
    #
    #     new_hand = Hand(player=player, hole_pos=hole, counter_count=0)
    #     board_model.iterate_sowing(new_hand)
    #     available_moves = board_model.available_moves(player)
    #
    #     if depth == 0 or len(available_moves) == 0:
    #         # print("terminating")
    #         return self.evaluate_position(board_model, player)
    #
    #     if board_model.action_to_take() == BoardModel.PROMPT_SOWING_A and player == 'a' or \
    #             board_model.action_to_take() == BoardModel.PROMPT_SOWING_B and player == 'b':
    #         available_moves = board_model.available_moves(player)
    #         for move in available_moves:
    #             new_board = copy.deepcopy(board_model)
    #             # print("testing mini move: " + str(move))
    #             # new_board.print_holes()
    #             evaluation = self.new_minimax(new_board, move, depth, player)
    #
    #             if player == 'a' and evaluation > best_value:
    #                 best_value = evaluation
    #
    #             if player == 'b' and evaluation < best_value:
    #                 best_value = evaluation
    #
    #     else:
    #
    #         available_moves = board_model.available_moves(player)
    #         for move in available_moves:
    #             new_board = copy.deepcopy(board_model)
    #             # print("testing mini move: " + str(move))
    #             # new_board.print_holes()
    #
    #             new_player = ''
    #             if player == 'a':
    #                 new_player = 'b'
    #             elif player == 'b':
    #                 new_player = 'a'
    #
    #             evaluation = self.new_minimax(new_board, move, depth-1, new_player)
    #
    #             if player == 'a' and evaluation > best_value:
    #                 best_value = evaluation
    #
    #             if player == 'b' and evaluation < best_value:
    #                 best_value = evaluation
    #
    #     pass

    def evaluate_position(self, board_model, player):
        best_value = 0

        best_value = board_model.storeroom_a_value - board_model.storeroom_b_value

        return best_value

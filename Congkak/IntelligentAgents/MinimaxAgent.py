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

    def __init__(self, weights, maximum_depth, maximum_number_node):
        self.final_best_value = 1
        self.final_best_move = 0
        self.board_model = BoardModel()

        # self.best_a_value_sofar = -math.inf
        # self.best_b_value_sofar = math.inf

        self.maximum_depth = maximum_depth
        self.maximum_number_of_node = maximum_number_node

        self.node_count = 0

        self.heuristics_weights = range(6)

        for weight in weights:
            self.heuristics_weights = weight

        pass

    def choose_move(self, player, board_model):

        self.final_best_value = 1
        self.final_best_move = 0
        available_moves = board_model.available_moves(player)
        self.board_model = board_model
        self.board_model.sowing_speed = 0
        self.board_model.game_phase = BoardModel.SEQUENTIAL_PHASE
        self.board_model.ping = False

        self.best_a_value_sofar = -math.inf
        self.best_b_value_sofar = math.inf

        self.node_count = 0

        if player == 'a':
            self.final_best_value = -math.inf
        elif player == 'b':
            self.final_best_value = math.inf

        for move in available_moves:
            new_board = copy.deepcopy(self.board_model)
            print("testing main move: " + str(move))
            evaluation = self.minimax(board_model=new_board, move=move, depth=self.maximum_depth, player=player, alpha=-math.inf, beta=math.inf)
            print("main move " + str(move) + " tested. evaluation: " + str(evaluation))

            if player == 'a':
                if evaluation >= self.final_best_value:
                    self.final_best_value = evaluation
                    self.final_best_move = move
            elif player == 'b':
                if evaluation <= self.final_best_value:
                    self.final_best_value = evaluation
                    self.final_best_move = move

        return self.final_best_move

    def minimax(self, board_model, move, depth, player, alpha, beta):

        self.node_count += 1

        print("node count: " + str(self.node_count))

        hole = 0

        if player == 'a':
            hole = move + 10
        elif player == 'b':
            hole = move + 20

        new_hand = Hand(player=player, hole_pos=hole, counter_count=0)
        board_model.iterate_sowing(new_hand)
        available_moves = board_model.available_moves(player)
        evaluation = self.evaluate_position(board_model, player)

        if depth == 0 or len(available_moves) == 0:
            print("terminating")
            return evaluation

        if player == 'a':
            max_eva = -math.inf

            match board_model.action_to_take():

                case BoardModel.PROMPT_SOWING_BOTH: # similar to prompt sowing a
                    available_moves = board_model.available_moves('a')
                    for move in available_moves:
                        new_board = copy.deepcopy(board_model)
                        eva = self.minimax(new_board, move, depth, 'a', alpha, beta)
                        max_eva = max(max_eva, eva)
                        alpha = max(alpha, max_eva)
                        if beta <= alpha:
                            break

                case BoardModel.PROMPT_SOWING_A:
                    available_moves = board_model.available_moves('a')
                    for move in available_moves:
                        new_board = copy.deepcopy(board_model)
                        eva = self.minimax(new_board, move, depth,'a', alpha, beta)
                        max_eva = max(max_eva,eva)
                        alpha = max(alpha, max_eva)
                        if beta <= alpha:
                            break

                case BoardModel.PROMPT_SOWING_B:
                    available_moves = board_model.available_moves('b')
                    for move in available_moves:
                        new_board = copy.deepcopy(board_model)
                        eva = self.minimax(new_board, move, depth-1, 'b', alpha, beta)
                        max_eva = max(max_eva, eva)
                        alpha = max(alpha, max_eva)
                        if beta <= alpha:
                            break

            # if evaluation > self.current_best_a_value:
            #     return evaluation

            return max_eva

        elif player == 'b':

            # print("testing player b")

            min_eva = math.inf

            match board_model.action_to_take():

                case BoardModel.PROMPT_SOWING_BOTH:  # similar to prompt sowing a
                    available_moves = board_model.available_moves('b')
                    for move in available_moves:
                        new_board = copy.deepcopy(board_model)
                        eva = self.minimax(new_board, move, depth, 'b', alpha, beta)
                        min_eva = min(min_eva, eva)
                        beta = min(alpha, min_eva)
                        if beta <= alpha:
                            print("alpha beta-d")
                            break

                case BoardModel.PROMPT_SOWING_A:
                    available_moves = board_model.available_moves('a')
                    for move in available_moves:
                        new_board = copy.deepcopy(board_model)
                        eva = self.minimax(new_board, move, depth - 1, 'a', alpha, beta)
                        min_eva = min(min_eva, eva)
                        beta = min(alpha, min_eva)
                        if beta <= alpha:
                            print("alpha beta-d")
                            break

                case BoardModel.PROMPT_SOWING_B:
                    available_moves = board_model.available_moves('b')
                    for move in available_moves:
                        new_board = copy.deepcopy(board_model)
                        eva = self.minimax(new_board, move, depth, 'b', alpha, beta)
                        min_eva = min(min_eva, eva)
                        beta = min(alpha, min_eva)
                        if beta <= alpha:
                            break

            return min_eva

            #
            # if evaluation < self.current_best_b_value:
            #     return evaluation

        pass

    def maximising(self, player, move, board_model):

        self.node_count += 1

        hole = 0

        best_value = -1

        if player == 'a':
            hole = move + 10
        elif player == 'b':
            hole = move + 20

        new_hand = Hand(player=player, hole_pos=hole, counter_count=0)

        board_model.iterate_sowing(new_hand)

        evaluation = self.evaluate_position(board_model, player)

        if player == 'a' and evaluation > self.best_a_value_sofar:
            # print("optimal")
            return evaluation
        elif player == 'b' and evaluation < self.best_b_value_sofar:
            return evaluation

        # print(board_model.storeroom_a_value)

        if board_model.action_to_take() == BoardModel.PROMPT_SOWING_A and player == 'a' or \
                board_model.action_to_take() == BoardModel.PROMPT_SOWING_B and player == 'b':
            available_moves = board_model.available_moves(player)
            for move in available_moves:
                new_board = copy.deepcopy(board_model)
                # print("testing mini move: " + str(move))
                # new_board.print_holes()
                evaluation = self.maximising(player, move, new_board)

                if evaluation > self.final_best_value:
                    return evaluation

                if evaluation >= best_value:
                    best_value = evaluation
        else:

            if player == 'a':
                best_value = board_model.storeroom_a_value
            elif player == 'b':
                best_value = board_model.storeroom_b_value

    def evaluate_position(self, board_model, player):
        best_value = 0

        best_value = board_model.storeroom_a_value - board_model.storeroom_b_value
        #
        # if player == 'a':
        #     best_value = board_model.storeroom_a_value
        # elif player == 'b':
        #     best_value = -board_model.storeroom_b_value
        return best_value

import copy
import math

from Congkak.CongkakBoardModel import BoardModel
from Congkak.Hand import Hand
from statistics import mean


# h0 = maximise counters on players side
# h1 = maximise the number of houses with counters in them
# h2 = maximise the counters in the player's storeroom
# h3 = minimise the counters in the opponent's storeroom
# h4 = maximise the number of chain moves
# h5 = maximise the difference between the player's and opponent's storeroom

def evaluate_position(board_model, player, chain_count, heuristic_weights):

    heuristics = [0, 0, 0, 0, 0, 0]

    if player == 'a':
        heuristics[0] = sum(board_model.house_a_values)

        for house in board_model.house_a_values:
            if house > 0:
                heuristics[1] += 1

        heuristics[2] = board_model.storeroom_a_value

        heuristics[3] = -board_model.storeroom_b_value

        heuristics[5] = board_model.storeroom_a_value - board_model.storeroom_b_value

    elif player == 'b':
        heuristics[0] = sum(board_model.house_b_values)

        for house in board_model.house_b_values:
            if house > 0:
                heuristics[1] += 1

        heuristics[2] = board_model.storeroom_b_value

        heuristics[3] = -board_model.storeroom_a_value

        heuristics[5] = board_model.storeroom_b_value - board_model.storeroom_a_value

    heuristics[4] = chain_count

    best_value = sum([w*h for (w, h) in zip(heuristic_weights, heuristics)])

    if player == 'a':
        return best_value
    elif player == 'b':
        return -best_value


class MaxAgent:
    def __init__(self, weights,  max_depth):
        self.board_model = BoardModel()

        self.node_count = 0
        self.leaf_node_count = 0

        self.max_depth = max_depth

        self.heuristics_weights = weights

        self.all_leaves = []
        self.all_depths = []

        pass

    def choose_move(self, player, board_model):

        final_best_value = 0

        if player == 'a':
            final_best_value = -math.inf
        elif player == 'b':
            final_best_value = math.inf

        final_best_move = 0
        available_moves = board_model.available_moves(player)

        board_model.sowing_speed = 0
        board_model.game_phase = BoardModel.SEQUENTIAL_PHASE
        board_model.ping = False
        board_model.debug = False

        self.board_model.player_a_hand.reset_hand()
        self.board_model.player_b_hand.reset_hand()

        self.node_count = 0
        self.leaf_node_count = 0

        for move in available_moves:
            new_board = copy.deepcopy(board_model)
            evaluation = self.maximising(player, move, new_board, self.max_depth, 0)

            if player == 'a' and evaluation >= final_best_value or \
                    player == 'b' and evaluation <= final_best_value:
                final_best_value = evaluation
                final_best_move = move

        self.all_leaves.append(self.leaf_node_count)

        print("max: player: " + player + " total nodes searched: " + str(self.node_count) + " no of leaf nodes reached: " + str(self.leaf_node_count))
        # print("final move: " + str(final_best_move) + " final best value: " + str(final_best_value))
        return final_best_move

    def maximising(self, player, move, board_model, depth, chain_count):

        self.node_count += 1

        if self.node_count % 10000 == 0:
            print("max: total nodes searched: " + str(self.node_count) + " leaf nodes reached: " + str(self.leaf_node_count))

        if depth <= 0:

            # print("depth reached")

            self.all_depths.append(self.max_depth - depth)

            best_value = evaluate_position(board_model, player, chain_count, self.heuristics_weights)

            return best_value

        hole = 0

        best_value = 0

        if player == 'a':
            hole = move + 10
            best_value = -math.inf
        elif player == 'b':
            hole = move + 20
            best_value = math.inf

        new_hand = Hand(player=player, hole_pos=hole, counter_count=0)
        new_hand.current_state = Hand.PICKUP_STATE

        board_model.iterate_progress_player(hand=new_hand)

        if board_model.get_next_action() == BoardModel.PROMPT_SOWING_A and player == 'a' or \
                board_model.get_next_action() == BoardModel.PROMPT_SOWING_B and player == 'b':

            available_moves = board_model.available_moves(player)
            for move in available_moves:
                new_board = copy.deepcopy(board_model)
                evaluation = self.maximising(player, move, new_board, depth - 1, chain_count + 1)
                if player == 'a' and evaluation >= best_value or \
                        player == 'b' and evaluation <= best_value:
                    best_value = evaluation

        else:
            self.all_depths.append(self.max_depth - depth)
            self.leaf_node_count += 1
            best_value = evaluate_position(board_model, player, chain_count, self.heuristics_weights)

        return best_value

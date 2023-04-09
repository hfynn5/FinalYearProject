import copy

from Congkak.CongkakBoardModel import BoardModel
from Congkak.Hand import Hand
from statistics import mean


def evaluate_position(board_model, player):
    best_value = 0

    best_value = board_model.storeroom_a_value - board_model.storeroom_b_value

    if player == 'a':
        return best_value
    elif player == 'b':
        return -best_value

    return best_value


class MaxAgent:
    def __init__(self, max_depth):
        self.board_model = BoardModel()
        self.final_best_value = 1
        self.final_best_move = 0

        self.node_count = 0
        self.leaf_node_count = 0

        self.max_depth = max_depth

        self.current_best_value = -1

        self.all_leaves = []
        self.all_depths = []

        pass

    def choose_move(self, player, board_model):
        self.final_best_value = 1
        self.final_best_move = 0
        self.current_best_value = -1
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
            evaluation = self.maximising(player, move, new_board, self.max_depth)

            if evaluation >= self.final_best_value:
                self.final_best_value = evaluation
                self.final_best_move = move

        self.all_leaves.append(self.leaf_node_count)

        print("max: total nodes searched: " + str(self.node_count) + " no of leaf nodes reached: " + str(self.leaf_node_count))
        # print("final move: " + str(self.final_best_move))
        return self.final_best_move

    def maximising(self, player, move, board_model, depth):

        self.node_count += 1

        if self.node_count % 10000 == 0:
            print("max: total nodes searched: " + str(self.node_count))

        if depth <= 0:
            # print("depth reached")
            best_value = 0
            if player == 'a':
                best_value = board_model.storeroom_a_value
            elif player == 'b':
                best_value = board_model.storeroom_b_value

            return best_value

        hole = 0

        if player == 'a':
            hole = move + 10
        elif player == 'b':
            hole = move + 20

        new_hand = Hand(player=player, hole_pos=hole, counter_count=0)
        new_hand.current_state = Hand.PICKUP_STATE

        board_model.iterate_progress_player(hand=new_hand)

        best_value = -1

        if board_model.get_next_action() == BoardModel.PROMPT_SOWING_A and player == 'a' or \
                board_model.get_next_action() == BoardModel.PROMPT_SOWING_B and player == 'b':

            available_moves = board_model.available_moves(player)
            for move in available_moves:
                new_board = copy.deepcopy(board_model)
                evaluation = self.maximising(player, move, new_board, depth - 1)

                if evaluation > self.final_best_value:
                    return evaluation

                if evaluation >= best_value:
                    best_value = evaluation
        else:
            self.all_depths.append(10-depth)
            self.leaf_node_count += 1

            best_value = evaluate_position(board_model,player)

        return best_value

import copy

from Congkak.CongkakBoardModel import BoardModel
from Congkak.Hand import Hand


class MaxAgent:
    def __init__(self):
        self.board_model = BoardModel()
        self.final_best_value = 1
        self.final_best_move = 0

        self.node_count = 0
        self.leaf_node_count = 0

        self.depth = 0

        self.current_best_value = -1

        pass

    def choose_move(self, player, board_model):
        self.final_best_value = 1
        self.final_best_move = 0
        self.depth = 1
        self.current_best_value = -1
        available_moves = board_model.available_moves(player)

        board_model.sowing_speed = 0
        board_model.game_phase = BoardModel.SEQUENTIAL_PHASE
        board_model.ping = False

        self.board_model.player_a_hand.reset_hand()
        self.board_model.player_b_hand.reset_hand()

        self.node_count = 0
        self.leaf_node_count = 0

        for move in available_moves:
            new_board = copy.deepcopy(board_model)
            evaluation = self.maximising(player, move, new_board, 1)

            if evaluation >= self.final_best_value:
                self.final_best_value = evaluation
                self.final_best_move = move

        print("max: total nodes searched: " + str(self.node_count) + " no of leaf nodes reached: " + str(self.leaf_node_count))
        print("final move: " + str(self.final_best_move))
        return self.final_best_move

    def maximising(self, player, move, board_model, depth):

        self.node_count += 1

        if self.node_count % 100 == 0:
            print("total nodes searched: " + str(self.node_count))

        self.depth = max(self.depth, depth)

        hole = 0

        best_value = -1

        if player == 'a':
            hole = move + 10
        elif player == 'b':
            hole = move + 20

        new_hand = Hand(player=player, hole_pos=hole, counter_count=0)
        new_hand.current_state = Hand.PICKUP_STATE

        board_model.iterate_progress_player(hand=new_hand)

        if player == 'a':
            best_value = board_model.storeroom_a_value
        elif player == 'b':
            best_value = board_model.storeroom_b_value

        if best_value > self.current_best_value:
            self.current_best_value = best_value
            return best_value

        best_value = -1

        if board_model.get_next_action() == BoardModel.PROMPT_SOWING_A and player == 'a' or \
                board_model.get_next_action() == BoardModel.PROMPT_SOWING_B and player == 'b':

            available_moves = board_model.available_moves(player)
            for move in available_moves:
                new_board = copy.deepcopy(board_model)
                evaluation = self.maximising(player, move, new_board, depth + 1)

                if evaluation > self.final_best_value:
                    return evaluation

                if evaluation >= best_value:
                    best_value = evaluation
        else:
            self.leaf_node_count += 1
            if player == 'a':
                best_value = board_model.storeroom_a_value
            elif player == 'b':
                best_value = board_model.storeroom_b_value

        return best_value

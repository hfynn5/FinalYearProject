import copy

from Congkak.CongkakBoardModel import BoardModel
from Congkak.Hand import Hand


class MaxAgent:
    def __init__(self):
        self.board_model = BoardModel()
        self.final_best_value = 1
        self.final_best_move = 0

        self.no_of_node = 0

        self.depth = 0

        pass

    def choose_move(self, player, board_model):
        self.final_best_value = 1
        self.final_best_move = 0
        self.depth = 1
        available_moves = board_model.available_moves(player)

        board_model.sowing_speed = 0
        board_model.game_phase = BoardModel.SEQUENTIAL_PHASE
        board_model.ping = False

        board_model.reset_hand('a')
        board_model.reset_hand('b')
        board_model.player_a_status = BoardModel.STOP_SOWING_A
        board_model.player_b_status = BoardModel.STOP_SOWING_B

        self.no_of_node = 0

        for move in available_moves:
            new_board = copy.deepcopy(board_model)
            evaluation = self.maximising(player, move, new_board, 1)

            if evaluation >= self.final_best_value:
                self.final_best_value = evaluation
                self.final_best_move = move

        print("max: total nodes searched: " + str(self.no_of_node))
        return self.final_best_move

    def maximising(self, player, move, board_model, depth):

        self.no_of_node += 1

        self.depth = max(self.depth, depth)

        hole = 0

        best_value = -1

        if player == 'a':
            hole = move + 10
        elif player == 'b':
            hole = move + 20

        new_hand = Hand(player=player, hole_pos=hole, counter_count=0)

        board_model.iterate_sowing(new_hand)

        if board_model.action_to_take() == BoardModel.PROMPT_SOWING_A and player == 'a' or \
                board_model.action_to_take() == BoardModel.PROMPT_SOWING_B and player == 'b':
            available_moves = board_model.available_moves(player)
            for move in available_moves:
                new_board = copy.deepcopy(board_model)
                evaluation = self.maximising(player, move, new_board, depth + 1)

                if evaluation > self.final_best_value:
                    return evaluation

                if evaluation >= best_value:
                    best_value = evaluation
        else:
            if player == 'a':
                best_value = board_model.storeroom_a_value
            elif player == 'b':
                best_value = board_model.storeroom_b_value

        return best_value

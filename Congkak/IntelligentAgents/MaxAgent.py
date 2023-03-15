import copy

from Congkak.CongkakBoardModel import BoardModel
from Congkak.Hand import Hand


class MaxAgent:
    def __init__(self):
        self.board_model = BoardModel()

        self.final_best_value = 1
        self.final_best_move = 0

        pass

    def choose_move(self, player, board_model):
        self.final_best_value = 1
        self.final_best_move = 0
        available_moves = board_model.available_moves(player)
        self.board_model = board_model
        self.board_model.sowing_speed = 0
        self.board_model.game_phase = BoardModel.SEQUENTIAL_PHASE
        self.board_model.ping = False

        for move in available_moves:
            new_board = copy.deepcopy(self.board_model)
            # print("testing main move: " + str(move))
            # new_board.print_holes()
            evaluation = self.evaluate(player, move, new_board)
            # print("main move " + str(move) + " tested. evaluation: " + str(evaluation))
            if evaluation >= self.final_best_value:
                self.final_best_value = evaluation
                self.final_best_move = move

        # print("final eval: " + str(self.final_best_value))
        # print("final best move: " + str(self.final_best_move))
        return self.final_best_move

    def evaluate(self, player, move, board_model):

        hole = 0

        best_value = -1

        if player == 'a':
            hole = move + 10
        elif player == 'b':
            hole = move + 20

        new_hand = Hand(player=player, hole_pos=hole, counter_count=0)

        board_model.iterate_sowing(new_hand)

        if player == 'a' and board_model.storeroom_a_value > self.final_best_value:
            # print("optimal")
            return board_model.storeroom_a_value
        elif player == 'b' and board_model.storeroom_b_value > self.final_best_value:
            return board_model.storeroom_b_value

        # print(board_model.storeroom_a_value)

        if board_model.action_to_take() == BoardModel.PROMPT_SOWING_A and player == 'a' or \
                board_model.action_to_take() == BoardModel.PROMPT_SOWING_B and player == 'b':
            available_moves = board_model.available_moves(player)
            for move in available_moves:
                new_board = copy.deepcopy(board_model)
                # print("testing mini move: " + str(move))
                # new_board.print_holes()
                evaluation = self.evaluate(player, move, new_board)

                if evaluation > self.final_best_value:
                    return evaluation

                if evaluation >= best_value:
                    best_value = evaluation
        else:

            if player == 'a':
                best_value = board_model.storeroom_a_value
            elif player == 'b':
                best_value = board_model.storeroom_b_value

        # print("eval: " + str(best_value))
        return best_value

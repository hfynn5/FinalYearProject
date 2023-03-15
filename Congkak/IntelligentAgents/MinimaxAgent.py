import random
from Congkak.CongkakBoardModel import BoardModel

class MinimaxAgent:

    # h1 = maximise counters on players side
    # h2 = maximise the number of houses with counters in them
    # h3 = maximise the counters in the player's storeroom
    # h4 = minimise the counters in the opponent's storeroom
    # h5 = maximise the number of chain moves
    # h6 = maximise the difference between the player's and opponent's storeroom
    # h7 =


    def __init__(self, weights):

        self.heuristics_weights = range(6)

        for weight in weights:
            self.heuristics_weights = weight

        pass

    def choose_move(self, available_moves):
        choice = random.choice(available_moves)
        print("choice:" + str(choice))
        return choice
        pass

    def evaluate_position(self, board_model):
        pass
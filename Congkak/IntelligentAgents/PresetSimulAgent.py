import random
from Congkak.CongkakBoardModel import BoardModel

class PresetSimulAgent:
    def __init__(self):
        pass

    def choose_move(self, player, board_model):

        if board_model.house_a_values == [7,7,7,7,7,7,7]:
            # choice = random.choices([1, 2, 3, 4, 5, 6, 7], [0, 0, 0, 0, 0.143, 0, 0.857])[0]
            # choice = random.choices([1, 2, 3, 4, 5, 6, 7], [0, 0, 0, 0, 0, 0, 1])[0]
            choice = random.choices([1, 2, 3, 4, 5, 6, 7], [0, 0, 0.111, 0.111, 0.333, 0.111, 0.333])[0]
            print("choice: " + str(choice))
        else:
            available_moves = board_model.available_moves(player)
            choice = random.choice(available_moves)
            print("random choice: " + str(choice))

        return choice

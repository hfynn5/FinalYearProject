import random
from Congkak.CongkakBoardModel import BoardModel

class RandomAgent:
    def __init__(self):
        pass

    def choose_move(self, player, board_model):
        available_moves = board_model.available_moves(player)
        choice = random.choice(available_moves)

        return choice

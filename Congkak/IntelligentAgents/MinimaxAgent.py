import random


def choose_move(available_moves):
    choice = random.choice(available_moves)
    print("choice:" + str(choice))
    return choice
    pass
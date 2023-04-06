import copy
import random

from dataclasses import dataclass, field


from Congkak.CongkakBoardModel import BoardModel
from Congkak.Hand import Hand


@dataclass
class QState:
    house_a_values: list[int]
    house_b_values: list[int]
    q_value_player_a: list[int]
    q_value_player_b: list[int]
    player_a_choice: int = 0
    player_b_choice: int = 0

    # 0, 0, 0, 0, 0, 0, 0
    # 1, 1, 1, 1, 1, 1, 1


class QLearningSimulAgent:

    def __init__(self):

        self.loaded_states = []
        self.used_states_index = []
        self.learning_rate = 0.2
        self.discount_factor = 0.3

        pass

    def choose_move(self, player, board_model):

        self.used_states_index = []

        state_index = self.find_state_index(board_model)
        self.used_states_index.append(state_index)

        current_state = self.loaded_states[state_index]
        print(current_state)

        choice = 0

        if player == 'a':
            choice = random.choices([1, 2, 3, 4, 5, 6, 7], current_state.q_value_player_a)[0]
            self.loaded_states[state_index].player_a_choice = choice - 1
        elif player == 'b':
            choice = random.choices([1, 2, 3, 4, 5, 6, 7], current_state.q_value_player_b)[0]
            self.loaded_states[state_index].player_b_choice = choice - 1

        return choice

    def update_all_q_values(self, winner_player):

        prev_reward = 1

        for state_index in reversed(self.used_states_index):
            curr_state = self.loaded_states[state_index]
            self.loaded_states[state_index] = self.update_q_value(curr_state, winner_player, prev_reward)
            # prev_reward =

        for state in self.loaded_states:
            print(state)

    def update_q_value(self, state, winner_player, winner_reward):

        if winner_player == 'a':
            current_q_value_a = state.q_value_player_a[state.player_a_choice]
            current_q_value_b = state.q_value_player_a[state.player_b_choice]

            state.q_value_player_a[state.player_a_choice] += self.learning_rate * (winner_reward - current_q_value_a)
            state.q_value_player_b[state.player_b_choice] += self.learning_rate * (-winner_reward - current_q_value_b)
        elif winner_player == 'b':
            current_q_value_a = state.q_value_player_a[state.player_a_choice]
            current_q_value_b = state.q_value_player_a[state.player_b_choice]

            state.q_value_player_a[state.player_a_choice] += self.learning_rate * (-winner_reward - current_q_value_a)
            state.q_value_player_b[state.player_b_choice] += self.learning_rate * (winner_reward - current_q_value_b)

        if state.q_value_player_a[state.player_a_choice] < 0:
            state.q_value_player_a[state.player_a_choice] = 0

        if state.q_value_player_b[state.player_b_choice] < 0:
            state.q_value_player_b[state.player_b_choice] = 0

        return state

    def find_state_index(self, board_model):

        for index, state in enumerate(self.loaded_states):
            if board_model.house_a_values == state.house_a_values and \
                    board_model.house_b_values == state.house_b_values:
                return index

        house_a_prob = []
        house_b_prob = []

        for i in range(7):
            if i+1 in board_model.available_moves('a'):
                house_a_prob.append(1)
            else:
                house_a_prob.append(0)

            if i+1 in board_model.available_moves('b'):
                house_b_prob.append(1)
            else:
                house_b_prob.append(0)



        self.loaded_states.append(QState(board_model.house_a_values,
                                         board_model.house_b_values,
                                         house_a_prob,
                                         house_b_prob))

        return len(self.loaded_states) - 1

    def load_states(self):
        pass

    def save_states(self):
        pass

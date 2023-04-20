import copy
import random

from dataclasses import dataclass, field


from Congkak.CongkakBoardModel import BoardModel
from Congkak.Hand import Hand


@dataclass
class State:

    house_a_values: list[int]
    house_b_values: list[int]
    value_player_a: list[int]
    value_player_b: list[int]
    player_a_choice: int = 0
    player_b_choice: int = 0
    learning_rate: float = 0.1

    # 0, 0, 0, 0, 0, 0, 0
    # 1, 1, 1, 1, 1, 1, 1


class ReinforcementLearningSimulAgent:

    def __init__(self):

        self.loaded_states = []
        self.used_states_index = []
        # self.learning_rate = 0.01

        pass

    def choose_move(self, player, board_model):

        available_moves = board_model.available_moves(player)

        # self.learning_rate = min(self.learning_rate + 0.001, 0.1)

        state_index = self.find_state_index(board_model)

        if state_index not in self.used_states_index:
            self.used_states_index.append(state_index)

        current_state = self.loaded_states[state_index]

        # self.loaded_states[state_index].learning_rate = min(self.loaded_states[state_index].learning_rate - 0.001, 0.1)

        choice = 0

        if player == 'a':
            choice = random.choices([1, 2, 3, 4, 5, 6, 7], current_state.value_player_a)[0]
            # choice = random.choice(available_moves)
            self.loaded_states[state_index].player_a_choice = choice - 1
        elif player == 'b':
            choice = random.choices([1, 2, 3, 4, 5, 6, 7], current_state.value_player_b)[0]
            # choice = random.choice(available_moves)
            self.loaded_states[state_index].player_b_choice = choice - 1

        return choice

    def update_all_values(self, winner_player):

        for state_index in reversed(self.used_states_index):
            curr_state = self.loaded_states[state_index]
            self.loaded_states[state_index] = self.update_value(curr_state, winner_player)

    def clear_used_states(self):
        self.used_states_index = []
        self.used_states_index = []

    def update_value(self, state, winner_player):

        current_value_a = state.value_player_a[state.player_a_choice]
        current_value_b = state.value_player_b[state.player_b_choice]

        increase = state.learning_rate

        if winner_player == 'a':
            state.value_player_a[state.player_a_choice] = round(current_value_a + increase, 5)

        elif winner_player == 'b':
            state.value_player_b[state.player_b_choice] = round(current_value_b + increase, 5)

        if state.value_player_a[state.player_a_choice] < 0:
            state.value_player_a[state.player_a_choice] = 0

        if state.value_player_b[state.player_b_choice] < 0:
            state.value_player_b[state.player_b_choice] = 0

        state.learning_rate = max(increase - 0.001, 0.01)

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

        self.loaded_states.append(State(board_model.house_a_values,
                                        board_model.house_b_values,
                                        house_a_prob,
                                        house_b_prob))

        return len(self.loaded_states) - 1

    def print_all_states(self):
        print("RL: number of found states: " + str(len(self.loaded_states)) + " all states: ")
        print(self.state_to_string())
        # for state in self.loaded_states:
        #     print(state)

    def state_to_string(self):
        msg = "RL: number of found states: " + str(len(self.loaded_states)) + " all states: \n"
        for state in self.loaded_states:
            msg_x = ""
            msg_x += "house A state: "
            msg_x += str(state.house_a_values)
            msg_x += " house B state: "
            msg_x += str(state.house_b_values)
            msg_x += " player A value: "
            msg_x += str(state.value_player_a)
            msg_x += " player B value: "
            msg_x += str(state.value_player_b)

            msg += msg_x
            msg += "\n"

        return msg

    def load_states(self):
        pass

    def save_states(self):
        pass

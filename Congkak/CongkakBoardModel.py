import sys
import time

class Hand:
    player = 'n'
    hole_pos = 0
    counter_count = 0

    def __init__(self, player, hole_pos, counter_count):
        self.player = player
        self.hole_pos = hole_pos
        self.counter_count = counter_count

class BoardModel:

    # player A is top with storeroom on right.
    # player B is bottom with storeroom on left.
    storeroom_a_value = 0
    storeroom_b_value = 0

    # player A house 1 starts at left. For the sake of sanity, houses start at 1, not 0
    # player B house 1 starts at left.
    house_a_values = [0, 0, 0, 0, 0, 0, 0]
    house_b_values = [0, 0, 0, 0, 0, 0, 0]

    def __init__(self):
        self.house_a_values = [1, 7, 7, 7, 7, 7, 7]
        self.house_b_values = [1, 0, 0, 0, 0, 0, 0]

        self.storeroom_a_value = 0
        self.storeroom_b_value = 0

        # self.iterate_sowing(player='a', hole=6)


    def iterate_sowing(self, player, hole):

        CONTINUE_SOWING = 1
        STOP_SOWING = 2
        PROMPT_SOWING = 3

        status = CONTINUE_SOWING

        while status == CONTINUE_SOWING:

            new_hand_pos = self.sow_once(player = player, hole = hole)

            if new_hand_pos == 28 or new_hand_pos == 18:
                new_hand_pos -= 1

            if (new_hand_pos < 20 and self.house_a_values[new_hand_pos-11] == 1) or (new_hand_pos > 20 and self.house_b_values[new_hand_pos - 21] == 1):
                status = STOP_SOWING
                print("sowing stopped")
            elif new_hand_pos == 17 or new_hand_pos == 27:
                status = PROMPT_SOWING
                print("user needs to input hole")
            else:
                status = CONTINUE_SOWING
                hole = new_hand_pos % 10
                print("continuing starting with: " + str(hole))

    def sow_once(self, player, hole):

        hand_value = 0
        hand_pos = hole

        if player == 'a':

            hand_pos = 10 + hole

            hand_value = self.house_a_values[hole-1]
            self.house_a_values[hole-1] = 0

        elif player == 'b':

            hand_pos = 20 + hole

            hand_value = self.house_b_values[hole-1]
            self.house_b_values[hole-1] = 0

        player_hand = Hand(player=player, hole_pos=hand_pos, counter_count=hand_value)

        while player_hand.counter_count > 0:

            player_hand.hole_pos -= 1

            start = time.time()

            while time.time() - start < 1:
                print(time.time() - start)
                self.update_board()

            self.drop_counter(player_hand)

        return player_hand.hole_pos

    def drop_counter(self, hand):
        if hand.hole_pos == 10:
            if hand.player == 'a':
                self.storeroom_a_value += 1
                hand.counter_count -= 1
            hand.hole_pos = 28
        elif hand.hole_pos == 20:
            if hand.player == 'b':
                self.storeroom_b_value += 1
                hand.counter_count -= 1
            hand.hole_pos = 18
        elif hand.hole_pos < 20:
            self.house_a_values[hand.hole_pos - 11] += 1
            hand.counter_count -= 1
        elif hand.hole_pos > 20:
            self.house_b_values[hand.hole_pos - 21] += 1
            hand.counter_count -= 1

        return hand









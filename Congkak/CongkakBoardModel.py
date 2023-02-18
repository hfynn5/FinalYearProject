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
        self.house_a_values = [7, 7, 7, 7, 7, 7, 7]
        self.house_b_values = [7, 7, 7, 7, 7, 7, 7]

        self.storeroom_a_value = 0
        self.storeroom_b_value = 0

        # TODO: create hands for player A and B. Use this hand in all needed functions below

    # do repeated sowing
    # TODO: replace player and hole with hand
    def iterate_sowing(self, player, hole, sowing_speed):

        CONTINUE_SOWING = 1
        STOP_SOWING = 2
        PROMPT_SOWING = 3

        status = CONTINUE_SOWING

        while status == CONTINUE_SOWING:

            new_hand_pos = self.sow_once(player = player, hole = hole, sowing_speed=sowing_speed)

            time.sleep(sowing_speed)

            if new_hand_pos == 18 or new_hand_pos == 28:
                status = PROMPT_SOWING
                print("user needs to input hole")
            elif (new_hand_pos < 20 and (self.house_a_values[new_hand_pos-11] == 1 or self.house_a_values[new_hand_pos-11] == 0 )) or \
                    (new_hand_pos > 20 and (self.house_b_values[new_hand_pos - 21] == 1 or self.house_b_values[new_hand_pos - 21] == 0)):
                status = STOP_SOWING
                print("sowing stopped")
            else:
                status = CONTINUE_SOWING
                hole = new_hand_pos
                print("continuing starting with: " + str(hole))

    # sows once
    # TODO: replace player and hole with hand.
    def sow_once(self, player, hole, sowing_speed):

        hand_value = 0
        hand_pos = hole

        if hand_pos >= 10 and hand_pos < 20:
            hand_value = self.house_a_values[hole - 11]
            self.house_a_values[hole - 11] = 0
        elif hand_pos >= 20:
            hand_value = self.house_b_values[hole - 21]
            self.house_b_values[hole - 21] = 0

        player_hand = Hand(player=player, hole_pos=hand_pos, counter_count=hand_value)

        while player_hand.counter_count > 0:
            time.sleep(sowing_speed)
            player_hand.hole_pos -= 1
            self.drop_counter(player_hand)

        return player_hand.hole_pos

    # drops a counter a the position the hand is at
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

    # print holes
    def print_holes(self):
        print("house a: " + str(self.house_a_values))
        print("house b: " + str(self.house_b_values))
        print("store a: " + str(self.storeroom_a_value))
        print("store b: " + str(self.storeroom_b_value))








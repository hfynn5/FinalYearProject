import sys
import time
from Congkak.Hand import Hand

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

        self.player_a_hand = Hand(player='a', hole_pos=-1, counter_count=0)
        self.player_b_hand = Hand(player='b', hole_pos=-1, counter_count=0)
        self.current_hand = Hand(player='', hole_pos=-1, counter_count=0)

        self.sowing_speed = 0

    # TODO: add simultaneous sowing

    # do repeated sowing
    def iterate_sowing(self, player, hole):

        CONTINUE_SOWING = 1
        STOP_SOWING = 2
        PROMPT_SOWING = 3

        status = CONTINUE_SOWING

        self.current_hand = Hand(player=player, hole_pos=hole, counter_count=0)

        while status == CONTINUE_SOWING:

            self.current_hand = self.sow_once(self.current_hand)

            time.sleep(self.sowing_speed)

            if self.current_hand.hole_pos == 18 or self.current_hand.hole_pos == 28:
                status = PROMPT_SOWING
                self.player_a_hand = Hand(player='a', hole_pos=-1, counter_count=0)
                self.player_b_hand = Hand(player='b', hole_pos=-1, counter_count=0)
                print("user needs to input hole")
            elif (self.current_hand.hole_pos < 20 and
                  (self.house_a_values[self.current_hand.hole_pos-11] == 1 or
                   self.house_a_values[self.current_hand.hole_pos-11] == 0 )) or \
                    (self.current_hand.hole_pos > 20 and
                     (self.house_b_values[self.current_hand.hole_pos - 21] == 1 or
                      self.house_b_values[self.current_hand.hole_pos - 21] == 0)):
                status = STOP_SOWING
                self.player_a_hand = Hand(player='a', hole_pos=-1, counter_count=0)
                self.player_b_hand = Hand(player='b', hole_pos=-1, counter_count=0)
                print("sowing stopped")
            else:
                status = CONTINUE_SOWING
                # hole = self.current_hand.hole_pos
                print("continuing starting with: " + str(self.current_hand.hole_pos))

    # sows once
    def sow_once(self, hand):
        if 10 <= hand.hole_pos < 20:
            hand.counter_count = self.house_a_values[hand.hole_pos - 11]
            self.house_a_values[hand.hole_pos - 11] = 0
        elif hand.hole_pos >= 20:
            hand.counter_count = self.house_b_values[hand.hole_pos - 21]
            self.house_b_values[hand.hole_pos - 21] = 0

        while hand.counter_count > 0:

            time.sleep(self.sowing_speed)

            hand.hole_pos -= 1

            if hand.hole_pos == 10 and hand.player == 'b':
                hand.hole_pos = 27
            elif hand.hole_pos == 20 and hand.player == 'a':
                hand.hole_pos = 17

            hand = self.drop_counter(hand)

            if hand.player == 'a':
                self.player_a_hand = hand
            elif hand.player == 'b':
                self.player_b_hand = hand

        return hand

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

    def reset_hands(self):
        self.player_a_hand = Hand(player='a', hole_pos=-1, counter_count=0)
        self.player_b_hand = Hand(player='b', hole_pos=-1, counter_count=0)

    def update_player_hands(self):
        if self.current_hand.player == 'a':
            self.player_a_hand = self.current_hand
        elif self.current_hand.player == 'b':
            self.player_b_hand = self.current_hand

    # print holes
    def print_holes(self):
        print("house a: " + str(self.house_a_values))
        print("house b: " + str(self.house_b_values))
        print("store a: " + str(self.storeroom_a_value))
        print("store b: " + str(self.storeroom_b_value))








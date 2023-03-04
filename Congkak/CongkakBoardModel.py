import sys
import time
from Congkak.Hand import Hand

class BoardModel:

    CONTINUE_SOWING = 1
    STOP_SOWING_A = 21
    STOP_SOWING_B = 22
    PROMPT_SOWING_A = 31
    PROMPT_SOWING_B = 32
    TIKAM_A = 41
    TIKAM_B = 42
    ERROR = -1

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
        # self.current_hand = Hand(player='', hole_pos=-1, counter_count=0)

        self.must_loop_before_tikam = True

        self.turn_count = 0
        self.current_player_turn = ''

        self.sowing_speed = 0

    # do repeated sowing
    def iterate_sowing(self, current_hand):

        # self.current_hand = new_hand
        print(current_hand.hole_pos)

        if not current_hand.player == self.current_player_turn:
            self.turn_count += 1
            print("turn")

        self.current_player_turn = current_hand.player

        status = self.CONTINUE_SOWING

        self.update_player_hands_from_current_hand(current_hand)

        time.sleep(self.sowing_speed)

        while status == self.CONTINUE_SOWING:

            current_hand = self.sow_once(current_hand)

            self.update_player_hands_from_current_hand(current_hand)

            time.sleep(self.sowing_speed)

            status = self.check_hand_status(current_hand)

            if status == self.TIKAM_A:
                self.tikam(self.player_a_hand, True)
            elif status == self.TIKAM_B:
                self.tikam(self.player_b_hand, True)

        self.reset_hands()
        return status

    # sows once
    def sow_once(self, hand):

        hand = self.pick_up_all_counters(hand)

        if hand.counter_count == 0:
            return hand

        while hand.counter_count > 0:

            time.sleep(self.sowing_speed)

            hand.move_one_pos()

            hand = self.drop_counter(hand)

            if hand.player == 'a':
                self.player_a_hand = hand
            elif hand.player == 'b':
                self.player_b_hand = hand

        return hand

    # pick up all counters at the hand position and put into hand
    def pick_up_all_counters(self, hand):
        if 10 <= hand.hole_pos < 18:
            hand.counter_count = self.house_a_values[hand.hole_pos - 11]
            self.house_a_values[hand.hole_pos - 11] = 0
        elif 20 <= hand.hole_pos < 28:
            hand.counter_count = self.house_b_values[hand.hole_pos - 21]
            self.house_b_values[hand.hole_pos - 21] = 0
        else:
            print(hand)
            print("player at storeroom. cant pick up")
        return hand

    # drops a counter a the position the hand is at
    def drop_counter(self, hand):
        if hand.hole_pos == 10:
            if hand.player == 'a':
                self.storeroom_a_value += 1
                hand.drop_one_counter()
                hand.has_looped = True
            hand.hole_pos = 28
        elif hand.hole_pos == 20:
            if hand.player == 'b':
                self.storeroom_b_value += 1
                hand.drop_one_counter()
                hand.has_looped = True
            hand.hole_pos = 18
        elif hand.hole_pos < 20:
            self.house_a_values[hand.hole_pos - 11] += 1
            hand.drop_one_counter()
        elif hand.hole_pos > 20:
            self.house_b_values[hand.hole_pos - 21] += 1
            hand.drop_one_counter()

        return hand

    # check status of hand
    def check_hand_status(self, hand):

        status = self.CONTINUE_SOWING

        if hand.hole_pos == 28:
            status = self.PROMPT_SOWING_A
        elif hand.hole_pos == 18:
            status = self.PROMPT_SOWING_B
        elif (hand.hole_pos < 20 and
              (self.house_a_values[hand.hole_pos - 11] == 0)) or \
                (hand.hole_pos > 20 and
                 (self.house_b_values[hand.hole_pos - 21] == 0)):
            status = self.ERROR
        elif (hand.hole_pos < 20 and
              (self.house_a_values[hand.hole_pos - 11] == 1)):
            if hand.player == 'a':
                if hand.has_looped:
                    status = self.TIKAM_A
                else:
                    status = self.STOP_SOWING_A
            elif hand.player == 'b':
                status = self.STOP_SOWING_B
        elif (hand.hole_pos > 20 and
              (self.house_b_values[hand.hole_pos - 21] == 1)):

            if hand.player == 'a':
                status = self.STOP_SOWING_A
            elif hand.player == 'b':
                if hand.has_looped:
                    status = self.TIKAM_B
                else:
                    status = self.STOP_SOWING_B
        else:
            status = self.CONTINUE_SOWING

        return status

    # tikam the hand (will check if its possible to tikam or not
    def tikam(self, hand, timed):

        if timed:
            delay = self.sowing_speed
        else:
            delay = 0

        if hand.player == 'a' and hand.has_looped and hand.hole_pos < 20:
            self.player_a_hand = hand

            opposite_hole = 17 - self.player_a_hand.hole_pos
            current_hand_pos = self.player_a_hand.hole_pos

            self.house_a_values[current_hand_pos - 11] = 0
            self.player_a_hand.counter_count += 1

            time.sleep(delay)

            self.player_a_hand.hole_pos = 21 + opposite_hole

            time.sleep(delay)

            self.player_a_hand.counter_count += self.house_b_values[opposite_hole]
            self.house_b_values[opposite_hole] = 0

            time.sleep(delay)

            self.player_a_hand.hole_pos = 28

            time.sleep(delay)

            self.storeroom_a_value += self.player_a_hand.drop_all_counters()

            time.sleep(delay)
            pass
        elif hand.player == 'b' and hand.has_looped and hand.hole_pos > 20:
            self.player_b_hand = hand

            opposite_hole = 27 - self.player_b_hand.hole_pos
            current_hand_pos = self.player_b_hand.hole_pos

            self.house_b_values[current_hand_pos - 21] = 0
            self.player_b_hand.counter_count += 1

            time.sleep(delay)

            self.player_b_hand.hole_pos = 11 + opposite_hole

            time.sleep(delay)

            self.player_b_hand.counter_count += self.house_a_values[opposite_hole]
            self.house_a_values[opposite_hole] = 0

            time.sleep(delay)

            self.player_b_hand.hole_pos = 18

            time.sleep(delay)

            self.storeroom_b_value += self.player_b_hand.drop_all_counters()

            time.sleep(delay)
        else:
            print("cannot tikam")

    # reset hands to empty and no position
    def reset_hands(self):
        self.player_a_hand = Hand(player='a', hole_pos=-1, counter_count=0)
        self.player_b_hand = Hand(player='b', hole_pos=-1, counter_count=0)

    # # update the current hand to appropriate player hand
    # def update_player_hands(self):
    #     if self.current_hand.player == 'a':
    #         self.player_a_hand = self.current_hand
    #     elif self.current_hand.player == 'b':
    #         self.player_b_hand = self.current_hand

    def update_player_hands_from_current_hand(self, current_hand):
        if current_hand.player == 'a':
            self.player_a_hand = current_hand
        elif current_hand.player == 'b':
            self.player_b_hand = current_hand

    def update_player_hand_pos(self, player, pos):
        if player == 'a':
            self.player_a_hand.hole_pos = pos
        elif player == 'b':
            self.player_b_hand.hole_pos = pos

    # print holes
    def print_holes(self):
        print("house a: " + str(self.house_a_values))
        print("house b: " + str(self.house_b_values))
        print("store a: " + str(self.storeroom_a_value))
        print("store b: " + str(self.storeroom_b_value))











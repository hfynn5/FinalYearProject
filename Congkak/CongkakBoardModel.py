import sys
import time
from Congkak.Hand import Hand

class BoardModel:

    CONTINUE_SOWING = 1
    STOP_SOWING_A = 21
    STOP_SOWING_B = 22
    STOP_SOWING_BOTH = 23
    PROMPT_SOWING_A = 31
    PROMPT_SOWING_B = 32
    PROMPT_SOWING_BOTH = 33
    TIKAM_A = 41
    TIKAM_B = 42
    TIKAM_BOTH = 43
    WAIT = 5
    ERROR = -1

    SIMULTANEOUS_PHASE = 1
    SEQUENTIAL_PHASE = 2

    # # player A is top with storeroom on right.
    # # player B is bottom with storeroom on left.
    # storeroom_a_value = 0
    # storeroom_b_value = 0
    #
    # # player A house 1 starts at left. For the sake of sanity, houses start at 1, not 0
    # # player B house 1 starts at left.
    # house_a_values = [0, 0, 0, 0, 0, 0, 0]
    # house_b_values = [0, 0, 0, 0, 0, 0, 0]


    def __init__(self):
        self.house_a_values = [7, 7, 7, 7, 7, 7, 7]
        self.house_b_values = [7, 7, 7, 7, 7, 7, 7]

        self.storeroom_a_value = 0
        self.storeroom_b_value = 0

        self.player_a_hand = Hand(player='a', hole_pos=-1, counter_count=0)
        self.player_b_hand = Hand(player='b', hole_pos=-1, counter_count=0)
        # self.current_hand = Hand(player='', hole_pos=-1, counter_count=0)

        self.must_loop_before_tikam = True

        self.player_a_status = self.STOP_SOWING_A
        self.player_b_status = self.STOP_SOWING_B
        self.active_players = []
        self.last_active_player = ''

        self.game_phase = self.SIMULTANEOUS_PHASE

        self.turn_count = 0
        self.current_player_turn = ''

        self.sowing_speed = 0
        # self.player_a_slowed_sowing_multiplier = 2
        # self.player_b_slowed_sowing_multiplier = 2
        self.slowed_sowing_multiplier = 2

        self.player_a_sowing_slowed = False
        self.player_b_sowing_slowed = False

    # do repeated sowing
    def iterate_sowing(self, current_hand):

        if current_hand.player not in self.active_players:
            self.active_players.append(current_hand.player)

        if current_hand.player == 'a':
            self.player_a_status = self.CONTINUE_SOWING
            self.player_b_sowing_slowed = False
        elif current_hand.player == 'b':
            self.player_b_status = self.CONTINUE_SOWING
            self.player_a_sowing_slowed = False

        status = self.CONTINUE_SOWING

        if not current_hand.player == self.current_player_turn and self.game_phase == self.SEQUENTIAL_PHASE:
            self.turn_count += 1
            print("turn")
            self.current_player_turn = current_hand.player

        self.update_player_hands_from_current_hand(current_hand)

        self.wait_between_micromoves(current_hand.player)

        while status == self.CONTINUE_SOWING:

            current_hand = self.sow_once(current_hand)

            self.update_player_hands_from_current_hand(current_hand)

            self.wait_between_micromoves(current_hand.player)

            status = self.check_hand_status(current_hand)

        if status == self.TIKAM_A:
            self.tikam(self.player_a_hand)
            self.player_a_status = self.STOP_SOWING_A
            status = self.STOP_SOWING_A
        elif status == self.TIKAM_B:
            self.tikam(self.player_b_hand)
            self.player_b_status = self.STOP_SOWING_B
            status = self.STOP_SOWING_B

        if status == self.STOP_SOWING_A or status == self.STOP_SOWING_B:
            self.active_players.remove(current_hand.player)
            if len(self.active_players) == 0:
                self.last_active_player = current_hand.player

        self.reset_hands()
        return status

    # sows once
    def sow_once(self, hand):

        hand = self.pick_up_all_counters(hand)

        if hand.counter_count == 0:
            return hand

        while hand.counter_count > 0:

            self.wait_between_micromoves(hand.player)

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
            print("player " + hand.player + " at storeroom. cant pick up")
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

    # tikam the hand (will check if its possible to tikam or not
    def tikam(self, hand):

        if hand.player == 'a' and hand.has_looped and hand.hole_pos < 20:
            self.player_a_hand = hand

            opposite_hole = 17 - self.player_a_hand.hole_pos
            current_hand_pos = self.player_a_hand.hole_pos

            self.house_a_values[current_hand_pos - 11] = 0
            self.player_a_hand.counter_count += 1

            self.wait_between_micromoves(hand.player)

            self.player_a_hand.hole_pos = 21 + opposite_hole

            self.wait_between_micromoves(hand.player)

            self.player_a_hand.counter_count += self.house_b_values[opposite_hole]
            self.house_b_values[opposite_hole] = 0

            self.wait_between_micromoves(hand.player)

            self.player_a_hand.hole_pos = 28

            self.wait_between_micromoves(hand.player)

            self.storeroom_a_value += self.player_a_hand.drop_all_counters()

            self.wait_between_micromoves(hand.player)
            pass
        elif hand.player == 'b' and hand.has_looped and hand.hole_pos > 20:
            self.player_b_hand = hand

            opposite_hole = 27 - self.player_b_hand.hole_pos
            current_hand_pos = self.player_b_hand.hole_pos

            self.house_b_values[current_hand_pos - 21] = 0
            self.player_b_hand.counter_count += 1

            self.wait_between_micromoves(hand.player)

            self.player_b_hand.hole_pos = 11 + opposite_hole

            self.wait_between_micromoves(hand.player)

            self.player_b_hand.counter_count += self.house_a_values[opposite_hole]
            self.house_a_values[opposite_hole] = 0

            self.wait_between_micromoves(hand.player)

            self.player_b_hand.hole_pos = 18

            self.wait_between_micromoves(hand.player)

            self.storeroom_b_value += self.player_b_hand.drop_all_counters()

            self.wait_between_micromoves(hand.player)
        else:
            print("cannot tikam")

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

        if hand.player == 'a':
            self.player_a_status = status
        if hand.player == 'b':
            self.player_b_status = status

        return status

    # returns the action the game manager should do
    def action_to_take(self):
        action = self.ERROR
        if self.game_phase == self.SEQUENTIAL_PHASE:

            if self.player_a_status == self.PROMPT_SOWING_A:
                action = self.PROMPT_SOWING_A
            elif self.player_b_status == self.PROMPT_SOWING_B:
                action = self.PROMPT_SOWING_B
            elif self.player_a_status == self.STOP_SOWING_A and self.player_b_status == self.STOP_SOWING_B:
                if self.last_active_player == 'a':
                    action = self.PROMPT_SOWING_B
                elif self.last_active_player == 'b':
                    action = self.PROMPT_SOWING_A

        elif self.game_phase == self.SIMULTANEOUS_PHASE:

            if self.player_a_status == self.STOP_SOWING_A and self.player_b_status == self.STOP_SOWING_B:
                self.game_phase = self.SEQUENTIAL_PHASE
                if self.last_active_player == 'a':
                    action = self.PROMPT_SOWING_B
                elif self.last_active_player == 'b':
                    action = self.PROMPT_SOWING_A
            elif self.player_a_status == self.STOP_SOWING_A and not self.player_b_status == self.STOP_SOWING_B or \
                    self.player_b_status == self.STOP_SOWING_B and not self.player_a_status == self.STOP_SOWING_A:
                self.game_phase = self.SEQUENTIAL_PHASE
                action = self.WAIT
            elif self.player_a_status == self.PROMPT_SOWING_A and self.player_b_status == self.PROMPT_SOWING_B:
                action = self.PROMPT_SOWING_BOTH
            elif self.player_a_status == self.PROMPT_SOWING_A:
                action = self.PROMPT_SOWING_A
            elif self.player_b_status == self.PROMPT_SOWING_B:
                action = self.PROMPT_SOWING_B

        print("player a: " + str(self.player_a_status) + "player b: " + str(self.player_b_status))
        print("phase: " + str(self.game_phase))

        return action

    # reset hands to empty and no position
    def reset_hands(self):
        self.player_a_hand = Hand(player='a', hole_pos=-1, counter_count=0)
        self.player_b_hand = Hand(player='b', hole_pos=-1, counter_count=0)

    # update player hands given the current hand
    def update_player_hands_from_current_hand(self, current_hand):
        if current_hand.player == 'a':
            self.player_a_hand = current_hand
        elif current_hand.player == 'b':
            self.player_b_hand = current_hand

    # update player hand pos (10-28)
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

    # wait time
    def wait_between_micromoves(self, player):

        start_time = time.time()

        wait_length = self.sowing_speed

        if player == 'a' and self.player_a_sowing_slowed or player == 'b' and self.player_b_sowing_slowed:
            wait_length = self.sowing_speed * self.slowed_sowing_multiplier

        while time.time() - start_time < wait_length:
            if player == 'a' and self.player_a_sowing_slowed or player == 'b' and self.player_b_sowing_slowed:
                wait_length = self.sowing_speed * self.slowed_sowing_multiplier
            else:
                wait_length = self.sowing_speed
            pass

            time.sleep(0.01)



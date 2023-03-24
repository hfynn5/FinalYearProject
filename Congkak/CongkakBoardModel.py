import sys
import time
from Congkak.Hand import Hand


class BoardModel:
    CONTINUE_SOWING = "CONTINUE SOWING"
    CONTINUE_SOWING_A = "CONTINUE SOWING A"
    CONTINUE_SOWING_B = "CONTINUE SOWING B"
    STOP_SOWING_A = "STOP SOWING A"
    STOP_SOWING_B = "STOP SOWING B"
    STOP_SOWING_BOTH = "STOP SOWING BOTH"
    PROMPT_SOWING_A = "PROMPT SOWING A"
    PROMPT_SOWING_B = "PROMPT SOWING B"
    PROMPT_SOWING_BOTH = "PROMPT SOWING BOTH"
    TIKAM_A = "TIKAM A"
    TIKAM_B = "TIKAM B"
    TIKAM_BOTH = "TIKAM BOTH"
    WAIT = "WAIT"
    GAME_END = "GAME END"
    ERROR = "ERROR"

    SIMULTANEOUS_PHASE = 1
    SEQUENTIAL_PHASE = 2

    def __init__(self):
        # player A house 1 starts at left. For the sake of sanity, houses start at 1, not 0
        # player B house 1 starts at left.
        self.house_a_values = [7, 7, 7, 7, 7, 7, 7]
        self.house_b_values = [7, 7, 7, 7, 7, 7, 7]

        # player A is top with storeroom on right.
        # player B is bottom with storeroom on left.
        self.storeroom_a_value = 0
        self.storeroom_b_value = 0

        self.player_a_hand = Hand(player='a', hole_pos=-1, counter_count=0)
        self.player_b_hand = Hand(player='b', hole_pos=-1, counter_count=0)

        self.must_loop_before_tikam = True

        self.player_a_status = self.STOP_SOWING_A
        self.player_b_status = self.STOP_SOWING_B
        self.active_players = []
        self.last_active_player = ''

        self.game_phase = self.SIMULTANEOUS_PHASE

        self.sowing_speed = 0
        self.slowed_sowing_multiplier = 10  # if more than 10, slowing is infinite

        self.player_a_sowing_slowed = False
        self.player_b_sowing_slowed = False

        self.no_of_micromoves_made = 0
        self.no_of_micromoves_made_player_a = 0
        self.no_of_micromoves_made_player_b = 0

        self.ping = False

        self.moves_made = []

        self.running = True

    # do repeated sowing. has waiting
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

        self.update_player_hands_from_current_hand(current_hand)

        self.wait_micromove()

        while status == self.CONTINUE_SOWING:
            current_hand = self.sow_once(current_hand)

            self.update_player_hands_from_current_hand(current_hand)

            self.wait_micromove()

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
            if current_hand.player in self.active_players:
                self.active_players.remove(current_hand.player)
                if len(self.active_players) == 0:
                    self.last_active_player = current_hand.player

        self.reset_hand(current_hand.player)
        return status

    # sows once. has waiting
    def sow_once(self, hand):

        hand = self.pick_up_all_counters(hand)

        if hand.counter_count == 0:
            return hand

        while hand.counter_count > 0:

            self.wait_micromove()

            hand.move_one_pos()
            hand = self.drop_counter(hand)

            if hand.player == 'a':
                self.player_a_hand = hand
            elif hand.player == 'b':
                self.player_b_hand = hand

        return hand

    # do repeated simultaneous sowing
    def iterated_sowing_simultaneous(self, hand_a, hand_b):

        if 'a' not in self.active_players:
            self.active_players.append('a')

        if 'b' not in self.active_players:
            self.active_players.append('b')

        self.player_a_status = self.CONTINUE_SOWING
        self.player_b_status = self.CONTINUE_SOWING

        # status_a = self.CONTINUE_SOWING
        # status_b = self.CONTINUE_SOWING

        self.player_a_hand = hand_a
        self.player_b_hand = hand_b

        self.wait_micromove()

        while self.player_a_status == self.CONTINUE_SOWING and self.player_b_status == self.CONTINUE_SOWING:
            hand_a, hand_b = self.sow_once_simultaneous(hand_a, hand_b)

            self.player_a_hand = hand_a
            self.player_b_hand = hand_b

            self.wait_micromove()

            self.player_a_status = self.check_hand_status(hand_a)
            self.player_b_status = self.check_hand_status(hand_b)

        if self.player_a_status == self.STOP_SOWING_A:
            self.reset_hand('a')
            self.active_players.remove('a')

        if self.player_b_status == self.STOP_SOWING_B:
            self.reset_hand('b')
            self.active_players.remove('b')

        if self.player_a_status == self.PROMPT_SOWING_A:
            self.reset_hand('a')

        if self.player_b_status == self.PROMPT_SOWING_B:
            self.reset_hand('b')

        pass

    def sow_once_simultaneous(self, hand_a, hand_b):

        # TODO: this process will take time. picking up counters is technically a micromove
        #  therefore if one hand picks, the other must move. fix this.
        if hand_a.counter_count <= 0:
            hand_a = self.pick_up_all_counters(hand_a)
        if hand_b.counter_count <= 0:
            hand_b = self.pick_up_all_counters(hand_b)

        if hand_a.counter_count == 0 or hand_b.counter_count == 0:
            return hand_a, hand_b

        while hand_a.counter_count > 0 and hand_b.counter_count > 0:
            self.wait_micromove()

            hand_a.move_one_pos()
            hand_b.move_one_pos()

            hand_a = self.drop_counter(hand_a)
            hand_b = self.drop_counter(hand_b)

            self.player_a_hand = hand_a
            self.player_b_hand = hand_b

        return hand_a, hand_b

    # pick up all counters at the hand position and put into hand.
    def pick_up_all_counters(self, hand):
        if 10 <= hand.hole_pos < 18:
            hand.counter_count = self.house_a_values[hand.hole_pos - 11]
            self.house_a_values[hand.hole_pos - 11] = 0
        elif 20 <= hand.hole_pos < 28:
            hand.counter_count = self.house_b_values[hand.hole_pos - 21]
            self.house_b_values[hand.hole_pos - 21] = 0
        else:
            print(hand.hole_pos)
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

    # tikam the hand (will check if its possible to tikam or not). has waiting
    def tikam(self, hand):

        # print("tikaming")
        # # self.print_all_data()

        if hand.player == 'a' and hand.has_looped and hand.hole_pos < 20:
            self.player_a_hand = hand

            self.player_a_status = self.STOP_SOWING_A

            opposite_hole = 17 - self.player_a_hand.hole_pos
            current_hand_pos = self.player_a_hand.hole_pos

            self.house_a_values[current_hand_pos - 11] = 0
            self.player_a_hand.counter_count += 1

            self.wait_micromove()

            self.player_a_hand.hole_pos = 21 + opposite_hole

            self.wait_micromove()

            self.player_a_hand.counter_count += self.house_b_values[opposite_hole]
            self.house_b_values[opposite_hole] = 0

            self.wait_micromove()

            self.player_a_hand.hole_pos = 28

            self.wait_micromove()

            self.storeroom_a_value += self.player_a_hand.drop_all_counters()

            self.wait_micromove()

            self.reset_hand('a')

            self.player_a_status = self.STOP_SOWING_A

            self.active_players.remove('a')
            if len(self.active_players) == 0:
                self.last_active_player = 'a'

        elif hand.player == 'b' and hand.has_looped and hand.hole_pos > 20:
            self.player_b_hand = hand

            self.player_b_status = self.STOP_SOWING_B

            opposite_hole = 27 - self.player_b_hand.hole_pos
            current_hand_pos = self.player_b_hand.hole_pos

            self.house_b_values[current_hand_pos - 21] = 0
            self.player_b_hand.counter_count += 1

            self.wait_micromove()

            self.player_b_hand.hole_pos = 11 + opposite_hole

            self.wait_micromove()

            self.player_b_hand.counter_count += self.house_a_values[opposite_hole]
            self.house_a_values[opposite_hole] = 0

            self.wait_micromove()

            self.player_b_hand.hole_pos = 18

            self.wait_micromove()

            self.storeroom_b_value += self.player_b_hand.drop_all_counters()

            self.wait_micromove()

            self.reset_hand('b')

            self.player_b_status = self.STOP_SOWING_B

            self.active_players.remove('b')
            if len(self.active_players) == 0:
                self.last_active_player = 'b'

        else:
            print("cannot tikam")

        # print("tikamed")

    # check status of hand
    def check_hand_status(self, hand):

        status = self.CONTINUE_SOWING

        if hand.hole_pos == 28 and hand.counter_count == 0:
            status = self.PROMPT_SOWING_A
        elif hand.hole_pos == 18 and hand.counter_count == 0:
            status = self.PROMPT_SOWING_B

        elif (10 < hand.hole_pos < 18 and
              (self.house_a_values[hand.hole_pos - 11] == 1) and
              hand.counter_count == 0):
            if hand.player == 'a':
                if hand.has_looped:
                    status = self.TIKAM_A
                else:
                    status = self.STOP_SOWING_A
            elif hand.player == 'b':
                status = self.STOP_SOWING_B

        elif (20 < hand.hole_pos < 28 and
              (self.house_b_values[hand.hole_pos - 21] == 1) and
              hand.counter_count == 0):
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

        if not self.running:
            return self.WAIT

        if self.game_phase == self.SEQUENTIAL_PHASE:

            if sum(self.house_a_values) == 0 and sum(self.house_b_values) == 0:
                action = self.GAME_END

            elif sum(self.house_a_values) == 0:
                action = self.PROMPT_SOWING_B
                if self.ping: print("all of a houses empty. prompt player b")
            elif sum(self.house_b_values) == 0:
                action = self.PROMPT_SOWING_A
                if self.ping: print("all of b houses empty. prompt player a")

            elif self.player_a_status == self.PROMPT_SOWING_A:
                action = self.PROMPT_SOWING_A
                if self.ping: print("prompt player a 2")
            elif self.player_b_status == self.PROMPT_SOWING_B:
                action = self.PROMPT_SOWING_B
                if self.ping: print("prompt player b 2")

            elif self.player_a_status == self.STOP_SOWING_A and self.player_b_status == self.STOP_SOWING_B:
                if self.last_active_player == 'a':
                    action = self.PROMPT_SOWING_B
                    if self.ping: print("prompt player b 3")
                elif self.last_active_player == 'b':
                    action = self.PROMPT_SOWING_A
                    if self.ping: print("prompt player a 3")

            elif self.player_a_status == self.CONTINUE_SOWING and (self.player_b_status == self.STOP_SOWING_B or
                                                                   self.player_b_status == self.TIKAM_B):
                action = self.WAIT
                pass
            elif self.player_b_status == self.CONTINUE_SOWING and (self.player_a_status == self.STOP_SOWING_A or
                                                                   self.player_a_status == self.TIKAM_A):
                action = self.WAIT
            elif self.player_a_status == self.TIKAM_A and self.player_b_status == self.TIKAM_B:
                if self.ping: print(
                    "both tikam. prompting both. honestly, this should never be printed so you fucked up")
                action = self.WAIT
                pass
            else:
                print("seq action error. status a: " + str(self.player_a_status) + ". status b: " +
                      str(self.player_b_status) + ". active players: " + str(self.active_players))

        elif self.game_phase == self.SIMULTANEOUS_PHASE:

            # keep
            if self.player_a_status == self.PROMPT_SOWING_A and self.player_b_status == self.PROMPT_SOWING_B:
                if self.ping: print("both are prompted")
                action = self.PROMPT_SOWING_BOTH

            # keep
            elif self.player_a_status == self.STOP_SOWING_A and self.player_b_status == self.STOP_SOWING_B:
                if self.ping: print("both stopped at the same time. prompting both")
                action = self.PROMPT_SOWING_BOTH

            # probably keep
            elif self.player_a_status == self.TIKAM_A and self.player_b_status == self.TIKAM_B:
                if self.ping: print(
                    "both tikam. prompting both. honestly, this should never be printed so you fucked up")
                action = self.PROMPT_SOWING_BOTH

            elif self.player_a_status == self.STOP_SOWING_A and self.player_b_status == self.CONTINUE_SOWING:
                if self.ping: print("player a has stopped. player b has not. continue sowing b")
                action = self.CONTINUE_SOWING_B
                self.game_phase = self.SEQUENTIAL_PHASE
            elif self.player_b_status == self.STOP_SOWING_B and self.player_a_status == self.CONTINUE_SOWING:
                if self.ping: print("player b has stopped. player a has not. continue sowing a")
                action = self.CONTINUE_SOWING_A
                self.game_phase = self.SEQUENTIAL_PHASE

            elif self.player_a_status == self.TIKAM_A and self.player_b_status == self.CONTINUE_SOWING:
                if self.ping: print("player a has tikam. player b has not. continue sowing b")
                action = self.CONTINUE_SOWING_B
                self.game_phase = self.SEQUENTIAL_PHASE
            elif self.player_b_status == self.TIKAM_B and self.player_a_status == self.CONTINUE_SOWING:
                if self.ping: print("player b has tikam. player a has not. continue sowing a")
                action = self.CONTINUE_SOWING_A
                self.game_phase = self.SEQUENTIAL_PHASE

            elif self.player_a_status == self.PROMPT_SOWING_A:
                if self.player_b_status == self.STOP_SOWING_B:
                    self.game_phase = self.SEQUENTIAL_PHASE
                if self.ping: print("prompt player a")
                action = self.PROMPT_SOWING_A

            elif self.player_b_status == self.PROMPT_SOWING_B:
                if self.player_a_status == self.STOP_SOWING_A:
                    self.game_phase = self.SEQUENTIAL_PHASE
                if self.ping: print("prompt player b")
                action = self.PROMPT_SOWING_B
            elif self.player_a_status == self.CONTINUE_SOWING and self.player_b_status == self.CONTINUE_SOWING:
                action = self.WAIT
            else:
                print("simul action error. status a: " + str(self.player_a_status) + ". status b: " + str(
                    self.player_b_status))

        else:
            print("super weird bug. its neither seq nor simul")
            print("error. status a: " + str(self.player_a_status) + ". status b: " + str(
                self.player_b_status) + ". phase: " + str(self.game_phase))

        return action

    # reset hands to empty and no position
    # TODO: find vanishing counter.
    # (17, 22)
    # (11, '')
    def reset_hand(self, player):

        if player == 'a':
            self.player_a_hand = Hand(player='a', hole_pos=-1, counter_count=0)
        elif player == 'b':
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

    def reset_game(self):
        self.reset_hand('a')
        self.reset_hand('b')

        self.house_a_values = [7, 7, 7, 7, 7, 7, 7]
        self.house_b_values = [7, 7, 7, 7, 7, 7, 7]

        self.storeroom_a_value = 0
        self.storeroom_b_value = 0

        # self.player_a_status = self.STOP_SOWING_A
        # self.player_b_status = self.STOP_SOWING_B
        # self.active_players = []
        # self.last_active_player = ''
        #
        # self.game_phase = self.SIMULTANEOUS_PHASE
        #
        # self.no_of_micromoves_made = 0
        # self.no_of_micromoves_made_player_a = 0
        # self.no_of_micromoves_made_player_b = 0

    def append_move(self, player_a_move, player_b_move):
        if not (type(player_a_move) == int) or 1 <= player_a_move <= 7:
            player_a_move = ''
        if not (type(player_b_move) == int) or 1 <= player_b_move <= 7:
            player_b_move = ''

        move_tuple = (player_a_move, player_b_move)

        self.moves_made.append(move_tuple)

    def available_moves(self, player):
        available_move = []

        if player == 'a':
            for i, hole in enumerate(self.house_a_values):
                if hole > 0:
                    available_move.append(i + 1)
        elif player == 'b':
            for i, hole in enumerate(self.house_b_values):
                if hole > 0:
                    available_move.append(i + 1)

        return available_move

    def do_holes_have_counter(self, player):

        truth_list = []

        if player == 'a':
            for hole in self.house_a_values:
                if hole > 0:
                    truth_list.append(True)
                else:
                    truth_list.append(False)
        elif player == 'b':
            for hole in self.house_b_values:
                if hole > 0:
                    truth_list.append(True)
                else:
                    truth_list.append(False)

        return truth_list

    def wait_micromove(self):

        start_time = time.time()

        while self.running and time.time() - start_time < self.sowing_speed:
            # time.sleep(0.00001)
            pass

        if not self.running:
            raise Exception("Running the game is disabled.")

        # self.print_all_data()

    # print holes
    def print_all_data(self):
        print("house a: " + str(self.house_a_values))
        print("house b: " + str(self.house_b_values))
        print("store a: " + str(self.storeroom_a_value))
        print("store b: " + str(self.storeroom_b_value))
        self.player_a_hand.print_data()
        self.player_b_hand.print_data()

        total = sum(self.house_a_values) + sum(self.house_b_values) + self.storeroom_a_value + \
                self.storeroom_b_value + self.player_a_hand.counter_count + self.player_b_hand.counter_count

        print("total: " + str(total))

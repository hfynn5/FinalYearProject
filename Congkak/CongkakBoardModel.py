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

        self.ping = False
        self.debug = False

        self.moves_made = []

        self.running = True

    def iterate_progress_player(self, hand=None, player=None):

        self.game_phase = self.SEQUENTIAL_PHASE

        if hand is None:
            if player == 'a':
                hand = self.player_a_hand
            elif player == 'b':
                hand = self.player_b_hand
            else:
                print("invalid hand and player")
                return

        if hand.player not in self.active_players:
            self.active_players.append(hand.player)

        self.update_player_hands_from_current_hand(hand)

        while not hand.current_state == Hand.IDLE_STATE and not hand.current_state == Hand.PROMPTING_STATE:
            self.wait_micromove()
            hand = self.progress_hand(hand)
            self.update_player_hands_from_current_hand(hand)

        if hand.current_state == Hand.IDLE_STATE:
            self.active_players.remove(hand.player)
            self.last_active_player = hand.player
        elif hand.current_state == Hand.PROMPTING_STATE:
            self.last_active_player = hand.opponent()
            self.reset_hand(hand.player)

        action = self.get_next_action()

        self.update_player_hands_from_current_hand(hand)

        return action

    def iterate_progress_both_players(self, hand_a=None, hand_b=None):

        self.player_a_hand = hand_a
        self.player_b_hand = hand_b

        if self.player_a_hand.player not in self.active_players:
            self.active_players.append(self.player_a_hand.player)

        if self.player_b_hand.player not in self.active_players:
            self.active_players.append(self.player_b_hand.player)

        while not self.player_a_hand.current_state == Hand.IDLE_STATE and \
                not self.player_a_hand.current_state == Hand.PROMPTING_STATE and \
                not self.player_b_hand.current_state == Hand.IDLE_STATE and \
                not self.player_b_hand.current_state == Hand.PROMPTING_STATE:
            self.wait_micromove()
            self.player_a_hand = self.progress_hand(self.player_a_hand)
            self.player_b_hand = self.progress_hand(self.player_b_hand)
            # self.print_all_data()

            pass

        if self.player_a_hand.current_state == Hand.IDLE_STATE and self.player_b_hand.current_state == Hand.IDLE_STATE:
            self.active_players.remove(self.player_a_hand.player)
            self.active_players.remove(self.player_b_hand.player)
            self.last_active_player = ''
            self.reset_hand('a')
            self.reset_hand('b')
        elif self.player_a_hand.current_state == Hand.PROMPTING_STATE and \
                self.player_b_hand.current_state == Hand.PROMPTING_STATE:
            self.last_active_player = ''
            self.reset_hand('a')
            self.reset_hand('b')

        elif self.player_a_hand.current_state == Hand.IDLE_STATE and \
                self.player_b_hand.current_state == Hand.PROMPTING_STATE:
            self.active_players.remove(self.player_a_hand.player)
            self.last_active_player = 'a'
            self.reset_hand('a')
            self.reset_hand('b')
        elif self.player_b_hand.current_state == Hand.IDLE_STATE and \
                self.player_a_hand.current_state == Hand.PROMPTING_STATE:
            self.active_players.remove(self.player_b_hand.player)
            self.last_active_player = 'b'
            self.reset_hand('a')
            self.reset_hand('b')

        elif self.player_a_hand.current_state == Hand.IDLE_STATE:
            self.active_players.remove(self.player_a_hand.player)
            self.last_active_player = 'a'
            self.reset_hand('a')
            self.iterate_progress_player(hand=self.player_b_hand)
        elif self.player_b_hand.current_state == Hand.IDLE_STATE:
            self.active_players.remove(self.player_b_hand.player)
            self.last_active_player = 'b'
            self.reset_hand('b')
            self.iterate_progress_player(hand=self.player_a_hand)

        action = self.get_next_action()

        return action

    # progress the hand one micromove
    def progress_hand(self, hand):

        match hand.current_state:
            case Hand.IDLE_STATE:
                pass
            case Hand.SOWING_STATE:
                hand = self.sow_once(hand)
                pass
            case Hand.PICKUP_STATE:
                hand = self.pick_up_all_counters(hand)
                pass
            case Hand.PROMPTING_STATE:
                pass
            case Hand.TIKAM_STATE_1:
                hand = self.tikam_step_1(hand)
                pass
            case Hand.TIKAM_STATE_2:
                hand = self.tikam_step_2(hand)
                pass
            case Hand.TIKAM_STATE_3:
                hand = self.tikam_step_3(hand)
                pass

        self.update_hand_status(hand)

        return hand

    # picks up all counters at the hand position
    def pick_up_all_counters(self, hand):

        if hand.hole_pos == 10 or hand.hole_pos == 20:
            print(hand.hole_pos)
            print("player " + hand.player + " at storeroom. cant pick up")
        else:
            hand.counter_count += self.get_value_at_position(hand.hole_pos)
            self.set_value_at_position(hand.hole_pos, 0)

        return hand

    # drops a counter at the hand position
    def hand_drop_one_counter(self, hand):

        hand.remove_one_counter()
        self.increment_value_at_position(hand.hole_pos)

        return hand

    # drops all counters at the hand position
    def hand_drop_all_counters(self, hand):

        self.set_value_at_position(hand.hole_pos, hand.remove_all_counters())

        return hand

    def sow_once(self, hand):
        hand.move_one_pos()
        hand = self.hand_drop_one_counter(hand)
        return hand

    # picks up the one counter
    def tikam_step_1(self, hand):
        hand = self.pick_up_all_counters(hand)
        return hand

    # moves to opposite end and picks up all counters there
    def tikam_step_2(self, hand):
        hand.move_to_opposite_hole()
        hand = self.pick_up_all_counters(hand)
        return hand

    # moves to storeroom and drops all counters there
    def tikam_step_3(self, hand):
        hand.move_to_storeroom()
        hand = self.hand_drop_all_counters(hand)
        return hand

    # gets the number of counters at a position
    def get_value_at_position(self, pos):
        value = -1

        if pos == 10:
            value = self.storeroom_a_value
        elif pos == 20:
            value = self.storeroom_b_value
        elif 10 < pos < 18:
            value = self.house_a_values[pos - 11]
        elif 20 < pos < 28:
            value = self.house_b_values[pos - 21]
        else:
            print("invalid pos: " + str(pos))

        return value

    def increment_value_at_position(self, pos):
        if pos == 10:
            self.storeroom_a_value += 1
        elif pos == 20:
            self.storeroom_b_value += 1
        elif 10 < pos < 18:
            self.house_a_values[pos - 11] += 1
        elif 20 < pos < 28:
            self.house_b_values[pos - 21] += 1
        else:
            print("invalid pos: " + str(pos))

    # sets the number of counters at a position
    def set_value_at_position(self, pos, value):
        if pos == 10:
            self.storeroom_a_value = value
        elif pos == 20:
            self.storeroom_b_value = value
        elif 10 < pos < 18:
            self.house_a_values[pos - 11] = value
        elif 20 < pos < 28:
            self.house_b_values[pos - 21] = value
        else:
            print("invalid pos: " + str(pos))

    # updates the hand status based on all the data available
    def update_hand_status(self, hand):

        match hand.current_state:
            case Hand.IDLE_STATE:
                pass
            case Hand.SOWING_STATE:

                if hand.counter_count <= 0:

                    if hand.is_on_storeroom():
                        hand.current_state = Hand.PROMPTING_STATE

                    elif self.get_value_at_position(hand.hole_pos) == 1:
                        if hand.is_on_house_side():
                            hand.current_state = Hand.TIKAM_STATE_1
                        else:
                            hand.current_state = Hand.IDLE_STATE
                    elif self.get_value_at_position(hand.hole_pos) == 0:
                        if self.ping: print("ended at a hole with no counters. peculiar.")
                        hand.current_state = Hand.IDLE_STATE
                    else:
                        hand.current_state = Hand.PICKUP_STATE
                else:
                    hand.current_state = Hand.SOWING_STATE

                pass
            case Hand.PICKUP_STATE:

                if hand.counter_count > 0:
                    hand.current_state = Hand.SOWING_STATE
                else:
                    if self.ping: print("hand try to pickup but hand have no counter. weird")
                    hand.current_state = Hand.IDLE_STATE

                pass
            case Hand.PROMPTING_STATE:
                print("prompting action...")
                pass
            case Hand.TIKAM_STATE_1:
                hand.current_state = Hand.TIKAM_STATE_2
                pass
            case Hand.TIKAM_STATE_2:
                hand.current_state = Hand.TIKAM_STATE_3
                pass
            case Hand.TIKAM_STATE_3:
                hand.current_state = Hand.IDLE_STATE
                pass

        return hand

    # gets the next action that should be done
    def get_next_action(self):

        action = self.ERROR

        if sum(self.house_a_values) == 0 and sum(self.house_b_values) == 0:
            action = self.GAME_END

        if sum(self.house_a_values) == 0:
            action = self.PROMPT_SOWING_B
            if self.ping: print("all of a houses empty. prompt player b")
        elif sum(self.house_b_values) == 0:
            action = self.PROMPT_SOWING_A
            if self.ping: print("all of b houses empty. prompt player a")

        elif self.last_active_player == 'a':
            action = self.PROMPT_SOWING_B
        elif self.last_active_player == 'b':
            action = self.PROMPT_SOWING_A
        elif self.last_active_player == '':
            action = self.PROMPT_SOWING_BOTH

        return action

    def reset_hand(self, player):

        if player == 'a':
            self.player_a_hand = Hand(player='a', hole_pos=-1, counter_count=0)
            self.player_a_hand.is_tikaming = False
        elif player == 'b':
            self.player_b_hand = Hand(player='b', hole_pos=-1, counter_count=0)
            self.player_b_hand.is_tikaming = False

    # update player hands given the current hand
    def update_player_hands_from_current_hand(self, current_hand):
        if current_hand.player == 'a':
            self.player_a_hand = current_hand
            return self.player_a_hand
        elif current_hand.player == 'b':
            self.player_b_hand = current_hand
            return self.player_b_hand
        return None

    # update player hand pos (10-27)
    def update_player_hand_pos(self, player, pos):
        if player == 'a':
            self.player_a_hand.hole_pos = pos
        elif player == 'b':
            self.player_b_hand.hole_pos = pos

    # reset game to initial mode
    def reset_game(self):

        self.house_a_values = [7, 7, 7, 7, 7, 7, 7]
        self.house_b_values = [7, 7, 7, 7, 7, 7, 7]

        self.storeroom_a_value = 0
        self.storeroom_b_value = 0

        self.reset_hand('a')
        self.reset_hand('b')

        self.player_a_status = self.STOP_SOWING_A
        self.player_b_status = self.STOP_SOWING_B
        self.active_players = []
        self.last_active_player = ''

        self.game_phase = self.SIMULTANEOUS_PHASE

        self.moves_made = []

        self.running = True

    # append a move to the list
    def append_move(self, player_a_move, player_b_move):
        if not (type(player_a_move) == int) or 1 <= player_a_move <= 7:
            player_a_move = 0
        if not (type(player_b_move) == int) or 1 <= player_b_move <= 7:
            player_b_move = 0

        move_tuple = (player_a_move, player_b_move)

        self.moves_made.append(move_tuple)

    # check the available moves a player can do
    def available_moves(self, player):
        available_move = []

        if player == 'a':
            for i, hole in enumerate(self.house_a_values):
                if hole > 0 and not (self.player_b_hand.hole_pos == i+11 and self.player_b_hand.counter_count == 0):
                    available_move.append(i + 1)
        elif player == 'b':
            for i, hole in enumerate(self.house_b_values):
                if hole > 0 and not (self.player_a_hand.hole_pos == i+21 and self.player_a_hand.counter_count == 0):
                    available_move.append(i + 1)

        return available_move

    # check if player side have counter
    def does_player_hole_have_counter(self, player):

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

    # wait a micromove if game is running
    def wait_micromove(self):

        start_time = time.time()

        while self.running and time.time() - start_time < self.sowing_speed:
            pass

        if not self.running:
            raise Exception("Running the game is disabled.")
            self.print_all_data()

    # print holes
    def print_all_data(self):
        print("house a: " + str(self.house_a_values))
        print("house b: " + str(self.house_b_values))
        print("store a: " + str(self.storeroom_a_value))
        print("store b: " + str(self.storeroom_b_value))
        self.player_a_hand.print_data()
        self.player_b_hand.print_data()

        # total = sum(self.house_a_values) + sum(self.house_b_values) + self.storeroom_a_value + \
        #         self.storeroom_b_value + self.player_a_hand.counter_count + self.player_b_hand.counter_count
        #
        # print("total: " + str(total))

        print("moves made so far: " + str(self.moves_made))


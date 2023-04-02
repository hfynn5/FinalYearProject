class Hand:

    ERROR_STATE = -1
    IDLE_STATE = 0
    SOWING_STATE = 1
    PICKUP_STATE = 2
    PROMPTING_STATE = 3
    TIKAM_STATE_1 = 4
    TIKAM_STATE_2 = 5
    TIKAM_STATE_3 = 6

    def __init__(self, player, hole_pos, counter_count):
        self.player = player
        self.hole_pos = hole_pos
        # 20 = storeroom B
        # 10 = storeroom A
        self.counter_count = counter_count

        self.current_state = self.IDLE_STATE

        self.has_looped = False

    def remove_one_counter(self):
        self.counter_count -= 1
        return 1

    def remove_all_counters(self):
        old = self.counter_count
        self.counter_count = 0
        return old

    def move_one_pos(self):
        self.hole_pos -= 1

        if (self.hole_pos == 10 and self.player == 'b') or self.hole_pos == 9:
            self.has_looped = True
            self.hole_pos = 27
        elif (self.hole_pos == 20 and self.player == 'a') or self.hole_pos == 19:
            self.has_looped = True
            self.hole_pos = 17

    def move_to_opposite_hole(self):

        opposite = 0

        if 10 < self.hole_pos < 18:
            opposite = 17 - self.hole_pos + 21
        elif 20 < self.hole_pos < 28:
            opposite = 27 - self.hole_pos + 11

        self.hole_pos = opposite

    def move_to_storeroom(self):
        if self.player == 'a':
            self.hole_pos = 10
        elif self.player == 'b':
            self.hole_pos = 20

    def move_n_pos(self, n):
        for x in n:
            self.move_one_pos()

    def is_on_house_side(self):
        if 10 < self.hole_pos < 18 and self.player == 'a':
            return True
        elif 20 < self.hole_pos < 28 and self.player == 'b':
            return True
        else:
            return False

    def is_on_storeroom(self):
        if self.hole_pos == 10 and self.player == 'a':
            return True
        elif self.hole_pos == 20 and self.player == 'b':
            return True
        else:
            return False

    def opponent(self):
        if self.player == 'a':
            return 'b'
        elif self.player == 'b':
            return 'a'
        else:
            return ''

    def reset_hand(self):
        self.current_state = self.IDLE_STATE
        self.hole_pos = -1
        self.counter_count = 0
        self.has_looped = False


    def print_data(self):
        print("hand: player: " + self.player +
              " counter count: " + str(self.counter_count) +
              " pos: " + str(self.hole_pos) +
              " state: " + str(self.current_state)
              )

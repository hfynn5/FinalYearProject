class Hand:
    player = 'n'
    hole_pos = 0
    counter_count = 0

    def __init__(self, player, hole_pos, counter_count):
        self.player = player
        self.hole_pos = hole_pos
        # 18 = storeroom B
        # 28 = storeroom A
        self.counter_count = counter_count
        self.has_looped = False
        self.is_running = False

    def drop_one_counter(self):
        self.counter_count -= 1
        return 1

    def drop_all_counters(self):
        old = self.counter_count
        self.counter_count = 0
        return old

    def move_one_pos(self):
        self.hole_pos -= 1

        if self.hole_pos == 10 and self.player == 'b':
            self.hole_pos = 27
        elif self.hole_pos == 20 and self.player == 'a':
            self.hole_pos = 17

    def move_n_pos(self, n):
        for x in n:
            self.move_one_pos()

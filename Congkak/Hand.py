class Hand:
    player = 'n'
    hole_pos = 0
    counter_count = 0

    def __init__(self, player, hole_pos, counter_count):
        self.player = player
        self.hole_pos = hole_pos
        self.counter_count = counter_count

    def drop_one_counter(self):
        self.counter_count -= 1
        return 1

    def drop_all_counters(self):
        old = self.counter_count
        self.counter_count = 0
        return old

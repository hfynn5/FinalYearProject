from graphics import *


class BoardGraphic:

    def __init__(self):

        self.house_a_positions = []
        self.house_b_positions = []
        self.storeroom_a_position = Point(0, 0)
        self.storeroom_b_position = Point(0, 0)

        self.win = GraphWin("Congkak", 800, 600)
        self.init_draw_board()

    def init_draw_board(self):
        storeroom_diameter = 45

        storeroom_b_x_pos = 100

        storeroom_y_pos = 150

        house_a_y_pos = 100
        house_b_y_pos = 200

        storeroom_house_offset = 90
        house_x_pos_init = storeroom_b_x_pos + storeroom_house_offset
        house_x_pos_offset = 70

        house_diameter = 25

        self.storeroom_b_position = Point(storeroom_b_x_pos, storeroom_y_pos)

        storeroom_b = Circle(self.storeroom_b_position, storeroom_diameter)

        storeroom_b.draw(self.win)

        house_x_pos = house_x_pos_init

        house_a_7 = Circle(Point(house_x_pos, house_a_y_pos), house_diameter)
        self.house_a_positions.append(Point(house_x_pos, house_a_y_pos))
        house_x_pos += house_x_pos_offset
        house_a_6 = Circle(Point(house_x_pos, house_a_y_pos), house_diameter)
        self.house_a_positions.append(Point(house_x_pos, house_a_y_pos))
        house_x_pos += house_x_pos_offset
        house_a_5 = Circle(Point(house_x_pos, house_a_y_pos), house_diameter)
        self.house_a_positions.append(Point(house_x_pos, house_a_y_pos))
        house_x_pos += house_x_pos_offset
        house_a_4 = Circle(Point(house_x_pos, house_a_y_pos), house_diameter)
        self.house_a_positions.append(Point(house_x_pos, house_a_y_pos))
        house_x_pos += house_x_pos_offset
        house_a_3 = Circle(Point(house_x_pos, house_a_y_pos), house_diameter)
        self.house_a_positions.append(Point(house_x_pos, house_a_y_pos))
        house_x_pos += house_x_pos_offset
        house_a_2 = Circle(Point(house_x_pos, house_a_y_pos), house_diameter)
        self.house_a_positions.append(Point(house_x_pos, house_a_y_pos))
        house_x_pos += house_x_pos_offset
        house_a_1 = Circle(Point(house_x_pos, house_a_y_pos), house_diameter)
        self.house_a_positions.append(Point(house_x_pos, house_a_y_pos))

        house_a_1.draw(self.win)
        house_a_2.draw(self.win)
        house_a_3.draw(self.win)
        house_a_4.draw(self.win)
        house_a_5.draw(self.win)
        house_a_6.draw(self.win)
        house_a_7.draw(self.win)

        storeroom_a_x_pos = house_x_pos + storeroom_house_offset

        storeroom_a = Circle(Point(storeroom_a_x_pos, storeroom_y_pos), storeroom_diameter)
        storeroom_a.draw(self.win)

        self.storeroom_a_position = Point(storeroom_a_x_pos, storeroom_y_pos)

        house_b_7 = Circle(Point(house_x_pos, house_b_y_pos), house_diameter)
        self.house_b_positions.append(Point(house_x_pos, house_b_y_pos))
        house_x_pos -= house_x_pos_offset
        house_b_6 = Circle(Point(house_x_pos, house_b_y_pos), house_diameter)
        self.house_b_positions.append(Point(house_x_pos, house_b_y_pos))
        house_x_pos -= house_x_pos_offset
        house_b_5 = Circle(Point(house_x_pos, house_b_y_pos), house_diameter)
        self.house_b_positions.append(Point(house_x_pos, house_b_y_pos))
        house_x_pos -= house_x_pos_offset
        house_b_4 = Circle(Point(house_x_pos, house_b_y_pos), house_diameter)
        self.house_b_positions.append(Point(house_x_pos, house_b_y_pos))
        house_x_pos -= house_x_pos_offset
        house_b_3 = Circle(Point(house_x_pos, house_b_y_pos), house_diameter)
        self.house_b_positions.append(Point(house_x_pos, house_b_y_pos))
        house_x_pos -= house_x_pos_offset
        house_b_2 = Circle(Point(house_x_pos, house_b_y_pos), house_diameter)
        self.house_b_positions.append(Point(house_x_pos, house_b_y_pos))
        house_x_pos -= house_x_pos_offset
        house_b_1 = Circle(Point(house_x_pos, house_b_y_pos), house_diameter)
        self.house_b_positions.append(Point(house_x_pos, house_b_y_pos))

        self.house_b_positions.reverse()

        house_b_1.draw(self.win)
        house_b_2.draw(self.win)
        house_b_3.draw(self.win)
        house_b_4.draw(self.win)
        house_b_5.draw(self.win)
        house_b_6.draw(self.win)
        house_b_7.draw(self.win)

    def update_values(self, house_a_values, house_b_values, storeroom_a_value, storeroom_b_value):

        for x in range(len(self.house_a_positions)):
            label = Text(self.house_a_positions[x], house_a_values[x])
            label.draw(self.win)

        for x in range(len(self.house_b_positions)):
            label = Text(self.house_b_positions[x], house_b_values[x])
            label.draw(self.win)

        label = Text(self.storeroom_a_position, storeroom_a_value)
        label.draw(self.win)

        label = Text(self.storeroom_b_position, storeroom_b_value)
        label.draw(self.win)
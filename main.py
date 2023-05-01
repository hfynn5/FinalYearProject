# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import Congkak.GameManager as CongkakGame
import Congkak.CongkakBoardModel as BoardModel
import sys
import traceback
import winsound

sys.setrecursionlimit(4000)

try:
    congkak = CongkakGame.GameManager()
except BoardModel.GameDisabledError:
    # traceback.print_exc()

    print("Game was disabled. ")

except SystemExit:
    print("Program has closed")

except:
    print("Unknown error encountered.")

    traceback.print_exc()

    print("if error code is '0xC0000374', it is recommended to run the game with the graphics disabled and the move speed set to maximum.")

finally:
    while True:
        pass
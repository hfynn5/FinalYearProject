# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import Congkak.GameManager as CongkakGame
import sys
import traceback
import winsound

sys.setrecursionlimit(4000)

try:
    congkak = CongkakGame.GameManager()
except:
    traceback.print_exc()

    # while True:
    #     winsound.Beep(987, 200)
    #     winsound.Beep(1396, 200)
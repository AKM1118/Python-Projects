import numpy as np
from numpy import random

class GameCreate:
    def __init__(self, size):
        self.size = size
    def createField(self):
        field = np.zeros((self.size, self.size), dtype=int)
        return field
    def showField(self,field):
        for i in range(50):
            print("")
        print(" --- --- --- ")
        for y in field:
            line = str("| ")
            for x in y:
                if x == 0:
                    line += " "
                else:
                    if x == 1:
                        line += "O"
                    else:
                        line += "X"
                line += " | "
            print(line)
            print(" --- --- --- ")

class PlayerClass:
    # XorO = True for X
    # XorO = False for O
    def __init__(self, player, XorO,gameWorld):
        self.player = player
        self.XorO = XorO
        self.gameWorld = gameWorld
    def makeMove(self, move, field):
        y = (move - 1) // 3
        x = (move - 1) % 3
        if field[y][x] == 0 and self.XorO:
            field[y][x] = 1
        elif field[y][x] == 0:
            field[y][x] = 2
        else:
            self.gameWorld.showField(field)
            print("Wrong move, kiddo, space taken!")
            self.makeMove(int(input("make your move from 1 to 9 =")), field)
        return field
    def winCheck(self, field):
        print("debug winCheck XorO ",self.XorO)
        if self.XorO:
            dot = 2
        else:
            dot = 1
        print("debug dot ",dot)
        # Horizontal check
        for y in field:
            win = 0
            for x in y:
                if x == dot:
                    win += 1
                if win == self.gameWorld.size:
                    return True
        print("debug HC ",win)
        # Vertical check
        for x in range(len(field[0])):
            win = 0
            for y in range(len(field[0])):
                if field[y][x] == dot:
                    win += 1
                if win == self.gameWorld.size:
                    return True
        print("debug VC ", win)
        # Diagonal check
        win = 0
        for x in range(len(field[0])):
            if field[x][x] == dot:
                win += 1
            if win == self.gameWorld.size:
                return True
        print("debug DC ", win)
        # Reverse Diagonal check
        win = 0
        for x in range(len(field[0])):
            if field[2 - x][x] == dot:
                win += 1
            if win == self.gameWorld.size:
                return True
        print("debug RDC ", win)

def mainGame():
    size = int(input("Please select the size of your square: "))
    gameWorld = GameCreate(size)
    field = gameWorld.createField()
    AIenab = input("Would you like to play against an AI? Y/N ")
    if AIenab == "Y":
        PieceSelect = input("Do you want to play as X or O? X/O ")
        if PieceSelect == "X":
            playerX = PlayerClass(True, True, field)
            playerO = PlayerClass(False, False, field)
        else:
            playerX = PlayerClass(False, True, field)
            playerO = PlayerClass(True, False, field)
    else:
        playerX = PlayerClass(True, True, field)
        playerO = PlayerClass(True, False, field)

    gameWorld.showField(field)
    while True:
        field = playerX.makeMove(int(input("make your move from 1 to 9 = ")), field)
        gameWorld.showField(field)
        if playerX.winCheck(field) == True:
            print("suck a dick")
            break
        field = playerO.makeMove(int(input("make your move from 1 to 9 = ")), field)
        gameWorld.showField(field)
        if playerO.winCheck(field) == True:
            print("suck a pussy")
            break

mainGame()


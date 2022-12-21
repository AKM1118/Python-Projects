import numpy as np
from numpy import random

def showField(field):
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

def makeMove(move,field,player=True):
    y = (move - 1) // 3
    x = (move - 1) % 3
    if field[y][x] == 0 and player:
        field[y][x] = 1
    elif field[y][x] == 0:
        field[y][x] = 2
    else:
        showField(field)
        print("Wrong move, kiddo, space taken!")
        makeMove(int(input("make you move from 1 to 9 =")), field)

    return field
def winCheck(field,player=True):
    if player:
        dot = 1
    else:
        dot = 2
    # Horizontal check
    for y in field:
        win = 0
        for x in y:
            if x == dot:
                win += 1
            if win == 3:
                return True
    # Vertical check
    for x in range(len(field[0])):
        win = 0
        for y in range(len(field[0])):
            if field[y][x] == dot:
                win += 1
            if win == 3:
                return True
    # Diagonal check
    win = 0
    for x in range(len(field[0])):
        if field[x][x] == dot:
            win += 1
        if win == 3:
            return True
    # Reverse Diagonal check
    win = 0
    for x in range(len(field[0])):
        if field[2-x][x] == dot:
            win += 1
        if win == 3:
            return True

def main():
    player = True
    field = np.zeros((3, 3), dtype=int)
    showField(field)
    while True:
        field = makeMove(int(input("make you move from 1 to 9 =")), field, player=player)
        if player == True:
            player = False
        else:
            player = True
        showField(field)
        if winCheck(field) == True:
            if player==True:
                print("you win!")
            else:
                print("you lose!")
            break

main()


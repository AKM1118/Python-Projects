import numpy as np


# A function to draw a field with the desired size
def showField(field):
    for i in range(50):
        print("")
    print(" ---" * len(field), " ")
    for y in field:
        line = str("| ")
        for x in y:
            if x == 0:
                line += " "
            else:
                if x == 1:
                    line += "X"
                else:
                    line += "O"
            line += " | "
        print(line)
        print(" ---" * len(field), " ")


class GameCreate:
    def __init__(self, size):
        self.size = size

    def createField(self):
        field = np.zeros((self.size, self.size), dtype=int)
        # for AI debug
        field = np.array([[1,0,2],[1,0,1],[2,2,0]], dtype=int)
        #
        return field


class PlayerClass:
    # XorO = True for X
    # XorO = False for O
    def __init__(self, player, XorO):
        self.player = player
        self.XorO = XorO

    def makeMove(self, field):
        if self.player == False:
            self.__moveAI(field)
            return field
        move = int(input("make your move from 1 to 9 = "))
        y = (move - 1) // 3
        x = (move - 1) % 3
        if field[y][x] == 0 and self.XorO:
            field[y][x] = 1
        elif field[y][x] == 0:
            field[y][x] = 2
        else:
            showField(field)
            print("Wrong move, kiddo, space taken!")
            self.makeMove(field)
        return field

    def __moveAI(self, field):
        if True:
            _, move = self.__minMaxAI(field, self.XorO)
        else:
            move = np.random.randint(1, 10, size=None, dtype=int)
        y = (move - 1) // 3
        x = (move - 1) % 3
        if field[y][x] == 0 and self.XorO:
            field[y][x] = 1
        elif field[y][x] == 0:
            field[y][x] = 2
        else:
            self.__moveAI(field)
        return field

    def __minMaxAI(self, field, XorO):
        # need to finish the minmax algo, probably make it separate from the movement
        move = 0
        score = 0
        old_field = field.copy()
        index_list = [1,2,3,4,5,6,7,8,9]
        for pos in range(9):
            y = (pos) // 3
            x = (pos) % 3
            if old_field[y][x] != 0:
                index_list.remove(pos+1)

        print(index_list)
        for index in index_list:
            if self.winCheck(self, old_field, XorO) == True:
                score += 1
            elif self.winCheck(self, old_field, not XorO) == True:
                score -= 1
            elif len(index_list) == 0:
                score = 0
            self.__minMaxAI(self, old_field, XorO)
        return score, move

        print("kek")

    def winCheck(self, field, XorO):
        if XorO:
            dot = 1
        else:
            dot = 2
        # Horizontal check
        for y in field:
            win = 0
            for x in y:
                if x == dot:
                    win += 1
                if win == len(field):
                    return True
        # Vertical check
        for x in range(len(field[0])):
            win = 0
            for y in range(len(field[0])):
                if field[y][x] == dot:
                    win += 1
                if win == len(field):
                    return True
        # Diagonal check
        win = 0
        for x in range(len(field[0])):
            if field[x][x] == dot:
                win += 1
            if win == len(field):
                return True
        # Reverse Diagonal check
        win = 0
        for x in range(len(field[0])):
            if field[2 - x][x] == dot:
                win += 1
            if win == len(field):
                return True


def mainGame():
    size = int(input("Please select the size of your square: "))
    gameWorld = GameCreate(size)
    field = gameWorld.createField()
    if input("Would you like to play against an AI? Y/N ") == "Y":
        if input("Do you want to play as X or O? X/O ") == "X":
            playerX = PlayerClass(True, True)
            playerO = PlayerClass(False, False)
        else:
            playerX = PlayerClass(False, True)
            playerO = PlayerClass(True, False)
    else:
        playerX = PlayerClass(True, True)
        playerO = PlayerClass(True, False)

    showField(field)
    while True:
        field = playerX.makeMove(field)
        showField(field)
        if playerX.winCheck(field,playerX.XorO) == True:
            print("player X wins")
            break
        blank = 0
        for y in field:
            for x in y:
                if x == 0:
                    blank += 1
        if blank == 0:
            print("it's a draw")
            break
        field = playerO.makeMove(field)
        showField(field)
        if playerO.winCheck(field,playerO.XorO) == True:
            print("player O wins")
            break


mainGame()

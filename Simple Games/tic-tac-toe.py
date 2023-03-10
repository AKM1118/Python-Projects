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
        #field = np.array([[1, 0, 2], [1, 0, 1], [2, 2, 0]], dtype=int)
        #
        return field


class PlayerClass:
    # XorO = True for X
    # XorO = False for O
    def __init__(self, player, XorO):
        self.player = player
        self.XorO = XorO

    def makeMove(self, field, moves_left):
        if self.player == False:
            self.__moveAI__(field, moves_left=moves_left)
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

    def __moveAI__(self, field, moves_left=int):
        # Get the moves_left from the main game to avoid recursion overflow
        score, move = self.__minMaxAI__(field, moves_left, self.XorO, alpha=-10, beta=10)
        print(f"Current move is {move}, score {score}, {moves_left} moves left, {self.XorO}")
        if move == -1:
            XorO = not self.XorO
            _, move = self.__minMaxAI__(field, moves_left, XorO, alpha=-10, beta=10)
            print(f"Current move is {move}, {moves_left} moves left, {XorO}")
        if move == -1:
            move = np.random.randint(1, 10, size=None, dtype=int)
        y = (move - 1) // 3
        x = (move - 1) % 3
        if field[y][x] == 0 and self.XorO:
            field[y][x] = 1
        elif field[y][x] == 0:
            field[y][x] = 2
        else:
            self.__moveAI__(field, moves_left)
        return field

    def __minMaxAI__(self, field, depth=int, maxiPlayer=bool, alpha=int, beta=int):
        # The algo works but during game testing it rarely calculate optimal moves
        # Need to figure out the issue behind AI not using the algo since algo works fine
        if depth == 0 or self.winCheck(field, not maxiPlayer) is True:
            maxi = not maxiPlayer
            if self.winCheck(field, maxi) is True and maxi is True:
                return 1, -1
            elif self.winCheck(field, maxi) is True and maxi is False:
                return -1, -1
            else:
                return 0, -1
        count = 1
        free_index = []
        for pos_y in field:
            for pos_x in pos_y:
                if pos_x == 0:
                    free_index.append(count)
                count += 1

        if maxiPlayer:
            maxVAL = 0
            maxPos = -1
            for pos in free_index:
                field_copy = field.copy()
                x = (pos - 1) % 3
                y = (pos - 1) // 3
                field_copy[y][x] = 2
                cur_val, _ = self.__minMaxAI__(field_copy, depth - 1, False, alpha, beta)
                alpha = max(alpha, cur_val)
                if beta <= alpha:
                    break
                if maxVAL < cur_val:
                    maxPos = pos
                    maxVAL = cur_val
                #print(f"maxVal for move {pos} is {maxVAL}")
            return maxVAL, maxPos
        else:
            miniVAL = 0
            minPos = -1
            for pos in free_index:
                field_copy = field.copy()
                x = (pos - 1) % 3
                y = (pos - 1) // 3
                field_copy[y][x] = 1
                cur_val, _ = self.__minMaxAI__(field_copy, depth - 1, True, alpha, beta)
                beta = min(beta, cur_val)
                if beta <= alpha:
                    break
                if miniVAL > cur_val:
                    minPos = pos
                    miniVAL = cur_val
                #print(f"miniVal for move {pos} is {miniVAL}")
            return miniVAL, minPos

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
    # Make universal input so that Y and y is both accepted and other letters do not throw an exception
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
    moves_left = 9
    while True:
        field = playerX.makeMove(field, moves_left)
        showField(field)
        if playerX.winCheck(field,playerX.XorO) == True:
            print("player X wins")
            break
        moves_left -= 1
        if moves_left <= 0:
            print("it's a draw")
            break
        field = playerO.makeMove(field, moves_left)
        showField(field)
        if playerO.winCheck(field,playerO.XorO) == True:
            print("player O wins")
            break
        moves_left -= 1
        if moves_left <= 0:
            print("it's a draw")
            break

mainGame()

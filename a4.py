

# a4.py

# How to play it: place your X or O on a empty tile`
# Legal moves: any empty tile
# Win: you reach 3 in a row before they do
# Loss: they reach 3 in a row before you do
# Draw: none of you reach 3 in a row when all 9 tiles is filled

# 1) make a list of legal moves
# 2) for each moves in moveList
#   do x number of random play out

# 3) choose the move that result in the greatet number of win

# Random play out:
#   play the game by choosing random moves
#   play till it wins, lose or draw
#   record the result

import random


class ticTacToe:
    def __init__(self):
        self.activePlayer = 1
        self.gameBoard = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.AI = 1

    # row 1 = index 0-2, row2 = index 3-5, row 3 = index 6-8
    # 0 1 2
    # 3 4 5
    # 6 7 8

    def getAI(self):
        return self.AI

    def setAI(self, first):
        if first == True:
            return self.AI
        else:
            self.AI = 2
            return self.AI

    def copyGameState(self):
        copyGame = ticTacToe()
        copyGame.activePlayer = self.activePlayer
        copyGame.gameBoard = self.gameBoard[:]
        copyGame.AI = self.AI
        return copyGame

    def getGameBoard(self):
        return self.gameBoard

    def currentPlayer(self):
        return self.activePlayer

    def switchPlayer(self):
        if (self.activePlayer == 2):
            self.activePlayer = 1
        else:
            self.activePlayer = 2
        return self.activePlayer

    def doMove(self, index, player):
        self.gameBoard[index] = player
        return self.gameBoard

    # Game ends when someone wins (in which there is gonna be left over 0, or there is no more 0)
    # so you should first check if smoeone win the game first

    def inGame(self):
        inGame = False
        if self.winLoseDraw() == -1:
            inGame = True
        return inGame

    def zeroCheck(self, numArr):
        noZero = True
        for x in numArr:
            if self.gameBoard[x] == 0:
                noZero = False
        return noZero

    def winLoseDraw(self):
            # 0 = draw, 1 = player 1 wins, 2 = player 2 wins
        winFlag = -1
        # win state is 0 3 6, 1 4 7, 2 5 8, 0 1 2 , 3 4 5, 6 7 8, 0 4 8, 2 4 6

        if self.gameBoard[0] == self.gameBoard[3] and self.gameBoard[0] == self.gameBoard[6] and self.zeroCheck([0, 3, 6]):
            if self.gameBoard[0] == 1:
                winFlag = 1
            else:
                winFlag = 2
        elif self.gameBoard[1] == self.gameBoard[4] and self.gameBoard[1] == self.gameBoard[7] and self.zeroCheck([1, 4, 7]):
            if self.gameBoard[1] == 1:
                winFlag = 1
            else:
                winFlag = 2
        elif self.gameBoard[2] == self.gameBoard[5] and self.gameBoard[2] == self.gameBoard[8] and self.zeroCheck([2, 5, 8]):
            if self.gameBoard[2] == 1:
                winFlag = 1
            else:
                winFlag = 2
        elif self.gameBoard[0] == self.gameBoard[1] and self.gameBoard[0] == self.gameBoard[2] and self.zeroCheck([0, 1, 2]):
            if self.gameBoard[0] == 1:
                winFlag = 1
            else:
                winFlag = 2
        elif self.gameBoard[3] == self.gameBoard[4] and self.gameBoard[3] == self.gameBoard[5] and self.zeroCheck([3, 4, 5]):
            if self.gameBoard[3] == 1:
                winFlag = 1
            else:
                winFlag = 2
        elif self.gameBoard[6] == self.gameBoard[7] and self.gameBoard[6] == self.gameBoard[8] and self.zeroCheck([6, 7, 8]):
            if self.gameBoard[6] == 1:
                winFlag = 1
            else:
                winFlag = 2
        elif self.gameBoard[0] == self.gameBoard[4] and self.gameBoard[0] == self.gameBoard[8] and self.zeroCheck([0, 4, 8]):
            if self.gameBoard[0] == 1:
                winFlag = 1
            else:
                winFlag = 2
        elif self.gameBoard[2] == self.gameBoard[4] and self.gameBoard[2] == self.gameBoard[6] and self.zeroCheck([2, 4, 6]):
            if self.gameBoard[2] == 1:
                winFlag = 1
            else:
                winFlag = 2
        elif 0 not in self.gameBoard:
            winFlag = 0

        else:
            winFlag = -1

        return winFlag
    
    def displayEndGame(self):
        display = ['_ ', '_ ', '_ ', '_ ', '_ ', '_ ', '_ ', '_ ', '_ ']
        displayString = ''
        for i in range(9):
            if self.gameBoard[i] == 1:
                display[i] = 'X '
            if self.gameBoard[i] == 2:
                display[i] = 'O '
            if i == 2 or i == 5:
                displayString += (display[i] + '\n')
            else:
                displayString += display[i]

        print(displayString)
        print('\nGame Over!\n')
        # if(self.winLoseDraw == 0):
        #     print('It was a draw!')
        # elif(self.winLoseDraw == 1):
        #     print('Player 1 wins!')
        # else:
        #     print('Player 2 wins!')

    def inputHelp(self):
        print('\nHere is the number for the corresponding tile:\n')
        print('0 1 2 \n3 4 5 \n6 7 8\n')

    def display(self):
        # display init
        display = ['_ ', '_ ', '_ ', '_ ', '_ ', '_ ', '_ ', '_ ', '_ ']
        displayString = ''
        for i in range(9):
            if self.gameBoard[i] == 1:
                display[i] = 'X '
            if self.gameBoard[i] == 2:
                display[i] = 'O '
            if i == 2 or i == 5:
                displayString += (display[i] + '\n')
            else:
                displayString += display[i]

        print(displayString)
        self.inputHelp()

    def legalMoves(self):
        legalIndex = []
        for i in range(9):
            if self.gameBoard[i] == 0:
                legalIndex.append(i)
        return legalIndex


class monteCarloTreeSearch:
    def __init__(self, game, randPlayOutNum):
        self.game = game
        self.board = self.game.getGameBoard()
        self.state = self.game.inGame()
        self.randPlayOutNum = randPlayOutNum

    def makeMove(self):
        legalMoves = self.game.legalMoves()
        # print('list of legal moves: ', legalMoves)
        # print('gameboard: ', self.game.getGameBoard())
        moveWinCounts = {}
        for m in legalMoves:  # for each legal moves
            moveWinCounts[m] = 0
        for m in legalMoves:
            for i in range(self.randPlayOutNum):  # do a set number of random play out
                # and store the result when each random playout is over
                moveWinCounts[m] += self.randomPlayOut(m)
        movechoice = legalMoves[0]
        choiceWinCount = moveWinCounts[movechoice]
        for win in moveWinCounts:
            if moveWinCounts[win] >= choiceWinCount:
                movechoice = win
                choiceWinCount = moveWinCounts[win]
        self.game.doMove(int(movechoice), self.game.activePlayer)
        # print('list of legal moves (after): ', self.game.legalMoves())
        # print('moveWinCounts = :', moveWinCounts)
        # print('movechoice:', movechoice)


# The idea is as follows. When it’s the computers turn to make a move, it makes a list of all legals moves. Then for each of these moves it does some number of random playouts. A random playout is when the computer simulates playing the game — using randomly chosen moves — until it is over, i.e. a win, loss, or draw is reached. It records the result (a win, loss, or draw), and then does some more random playouts. It does random playouts for every possible move, and when they’re done it choses the move that resulted in the greatest number of wins.

    def randomPlayOut(self, move):
        copyCurrentGame = self.game.copyGameState()
        copyCurrentGame.doMove(
            move, copyCurrentGame.activePlayer)  # make the move
        copyCurrentGame.switchPlayer()  # switch player
        while copyCurrentGame.inGame() == True:
            legalMoves = copyCurrentGame.legalMoves()
            randMove = random.randint(0, 8)
            while(randMove not in legalMoves):
                randMove = random.randint(0, 8)
            copyCurrentGame.doMove(randMove, copyCurrentGame.activePlayer)
            copyCurrentGame.switchPlayer()
            copyCurrentGame.state = copyCurrentGame.inGame()
        if copyCurrentGame.getAI() == 1:
            if copyCurrentGame.winLoseDraw() == 2:
                return -5
            elif copyCurrentGame.winLoseDraw() == 1:
                return 2
            else:
                return 1
        else:
            if copyCurrentGame.winLoseDraw() == 2:
                return 2
            elif copyCurrentGame.winLoseDraw() == 1:
                return -5
            else:
                return 1


def play_a_new_game():
    game = ticTacToe()
    aiMonte = monteCarloTreeSearch(game, 10000)
    gameState = game.inGame()
    playerMove = ''
    firstOrSecond = input('Do you want to go first? (type Y or N): ')
    if (firstOrSecond.upper() == 'N'):
        aiMonte.makeMove()
        game.switchPlayer()
        game.display()
        playerMove = input('Choose your next move... ')
    else:
        game.setAI(False)
        game.display()
        playerMove = input('Choose your next move... ')
    while gameState == True:
        game.doMove(int(playerMove), game.activePlayer)
        game.display()
        game.switchPlayer()
        aiMonte.makeMove()
        gameState = game.inGame()
        if gameState == True:
            game.switchPlayer()
            game.display()
            playerMove = input('Choose your next move... ')
            gameCheck = game.copyGameState()
            gameCheck.doMove(int(playerMove), gameCheck.activePlayer)
            gameState = gameCheck.inGame()

    game.doMove(int(playerMove), game.activePlayer)    
    print('\n')        
    game.displayEndGame()



if __name__ == '__main__':
  play_a_new_game()


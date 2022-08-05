# GAME SETUP

print('How many columns?')
numCols = int(input())
print('How many rows?')
numRows = int(input())
playerName = []
print('Enter PLAYER ONE name')
playerName.append(input())
print('Enter PLAYER TWO name')
playerName.append(input())

# VARIABLES

# specifies the blank character for the board
blank = ' . '

# 2D array giving the state of the board, beginning with a blank token in every entry
board = [ [blank]*numRows for i in range(numCols)]

# 1D array giving the highest occupied row in each column
highest = [-1 for i in range(numCols)]

# how many turns have been completed; turn%2 will indicate whose turn it is, player 1 (0) or player 2 (1)
turn = 0

# logs the column choices of official plays
playLog = []

# binary that specifies when the game is over
isGameOver = False

# sets tokens for each player
playerToken = ['[O]', '[X]']

# FUNCTIONS — GAME PLAY

# prints the current state of the board
def printBoard():
	print('\n')
	print('\n')
	for i in range(numRows):
		for j in range (numCols):
			print(board[j][numRows-i-1] + ' ', end = '')
		print('\n')
	for i in range(numCols):
		print(' ' + str(i+1) + '  ', end = '')
	print('\n')

# prompts next player for column choice and repeats until valid input is given; the value returned is adjusted to zero-index
# this currently has a carve-out for 0 to trigger the computer player
# change it back by switching <=0 to just <0 and removing the if (column == 0) block
def columnSelection():
	column = -1
	while (column <= 0 or column > numCols or not isColumnFree(column-1)):
		print(playerName[turn%2] + ' (' + playerToken[turn%2] + '), select a column')
		column = int(input())
		if (column == 0):
			return concrete()
	return (column-1)

# checks whether the top entry of a column is free
def isColumnFree(column):
	if (board[column][numRows-1] == blank):
		return True
	else:
		return False

# updates board AND highest column AND playLog
def updateBoard(player, column):
	for i in range(numRows):
		if (board[column][i] == blank):
			board[column][i] = playerToken[player]
			highest[column] += 1
			playLog.append([column, highest[column]])
			break

# checks whether the current player has just won after the most recent move has been logged
def checkWin():
	# identify (x,y) coordinates of the most recently placed token
	t = len(playLog) - 1
	x = playLog[t][0]
	y = playLog[t][1]
	if (checkWinVert(x,y) or checkWinHor(x,y) or checkWinDiagSWNE(x,y) or checkWinDiagNWSE(x,y)):
		return True
	else:
		return False

def checkWinVert(x,y):
	if (y > 2):
		p1 = board[x][y-3]
		p2 = board[x][y-2]
		p3 = board[x][y-1]
		p4 = board[x][y]
		if (p1 == p2 and p2 == p3 and p3 == p4):
			# print('VERTICAL WIN')
			return True
		else:
			return False
	return False

def checkWinHor(x,y):
	if (numCols > 3):
		# make x1 on the board
		xmin = 0
		# make x1 not too far from x
		xmin = max(xmin, x-3)
		# make x4 on the board
		xmax = numCols - 3
		# make x4 not too far from x
		xmax = min(xmax, x+1)
		for i in range(xmin, xmax):
			p1 = board[i][y]
			p2 = board[i+1][y]
			p3 = board[i+2][y]
			p4 = board[i+3][y]
			if (p1 == p2 and p2 == p3 and p3 == p4):
				# print('HORIZONTAL WIN WITH x1 = ' + str(x1))
				return True
	return False

def checkWinDiagSWNE(x,y):
	if (numCols > 3):
		# make x1 on the board
		xmin = 0
		# make x1 not too far from x
		xmin = max(xmin, x-3)
		# make y1 on the board
		xmin = max(xmin, x-y)
		# make x4 on the board
		xmax = numCols - 3
		# make x4 not too far from x
		xmax = min(xmax, x+1)
		# make y4 on the board
		xmax = min(xmax, numRows+x-y-3)
		for x1 in range(xmin, xmax):
			y1 = y - (x - x1)
			p1 = board[x1][y1]
			p2 = board[x1+1][y1+1]
			p3 = board[x1+2][y1+2]
			p4 = board[x1+3][y1+3]
			if (p1 == p2 and p2 == p3 and p3 == p4):
				# print('SW-NE WIN WITH x1 = ' + str(x1))
				return True
	return False

def checkWinDiagNWSE(x,y):
	if (numCols > 3):
		# make x1 on the board
		xmin = 0
		# make x1 not too far from x
		xmin = max(xmin, x-3)
		# make y1 on the board
		xmin = max(xmin, x+y-numRows+1)
		# make x4 on the board
		xmax = numCols - 3
		# make x4 not too far from x
		xmax = min(xmax, x+1)
		# make y4 on the board
		xmax = min(xmax, x+y-2)
		for x1 in range(xmin, xmax):
			y1 = y + (x - x1)
			p1 = board[x1][y1]
			p2 = board[x1+1][y1-1]
			p3 = board[x1+2][y1-2]
			p4 = board[x1+3][y1-3]
			if (p1 == p2 and p2 == p3 and p3 == p4):
				# print('SW-NE WIN WITH x1 = ' + str(x1))
				return True
	return False

# FUNCTIONS — HYPOTHETICALS AND STRATEGY

# specify which columns are open to take a token
def OpenMoves():
	moves = []
	for i in range(numCols):
		if (isColumnFree(i)):
			moves.append(i)
	return moves

# undo n moves, updating board, highest, and playLog
def undoMoves(n):
	for i in range(n):
		k = len(playLog)
		x = playLog[k-1][0]
		y = playLog[k-1][1]
		board[x][y] = blank
		highest[x] -= 1
		playLog.pop()
	return

# STRATEGY FUNCTIONS

def concrete():
	turnsRemaining = numCols * numRows - turn
	moves = OpenMoves()
	if (turnsRemaining > 0):
		theMove = moves[0]
	else:
		print('Uh oh, there shouldnt be any turns remaining')
	if (len(moves) == 1):
		print('There is only one column to choose')
		return theMove
	player = turn%2
	if (isWinningPossible(player)):
		print('We are going for the win')
		return movesToWin(player)[0]
	if (turnsRemaining > 1):
		if (isLosingInevitable(player)):
			print('There are no ways to avoid loss')
			return theMove
		if (isLosingPossible(player)):
			print('Losing is possible but we can avoid losing')
			for i in movesToLose(player):
				moves.remove(i)
			theMove = moves[0]
	if (turnsRemaining > 2):
		if (isTrappingPossible(player)):
			print('It looks like a trap is possible')
			for i in movesToTrap(player):
				for j in moves:
					if (i == j):
						print('We are going for the trap')
						return i
			print('It looks like all the traps were false hopes')
	if (turnsRemaining > 3):
		if (isGettingTrappedInevitable(player)):
			print('There are no ways to avoid a trap')
			return theMove
		if (isGettingTrappedPossible(player)):
			print('Getting trapped is possible but avoidable')
			for i in movesToGetTrapped(player):
				moves.remove(i)
			theMove = moves[0]
	return theMove

# CONCERNING T = 0 (could the game end on this (our) turn, i.e. can we win in one move)

def isWinningPossible(player):
	print('... determining if ' + playerName[player] + ' can win ...')
	for i in OpenMoves():
		updateBoard(player, i)
		if (checkWin()):
			undoMoves(1)
			return True
		else:
			undoMoves(1)

def movesToWin(player):
	print('... determining what moves give ' + playerName[player] + ' a win ...')	
	moves = []
	for i in OpenMoves():
		updateBoard(player, i)
		if (checkWin()):
			undoMoves(1)
			moves.append(i)
		else:
			undoMoves(1)
	return moves

# CONCERNING T = 1 (could the game end on their next turn)

def isLosingPossible(player):
	print('... determining if ' + playerName[player] + ' can lose ...')	
	for i in OpenMoves():
		updateBoard(player, i)
		if (isWinningPossible(1-player)):
			undoMoves(1)
			return True
		else:
			undoMoves(1)
	return False

def isLosingInevitable(player):
	print('... determining if ' + playerName[player] + ' can avoid losing ...')	
	for i in OpenMoves():
		updateBoard(player, i)
		if (not isWinningPossible(1-player)):
			undoMoves(1)
			return False
		else:
			undoMoves(1)
	return True

def movesToLose(player):
	print('... determining what moves give ' + playerName[player] + ' a loss ...')	
	moves = []
	for i in OpenMoves():
		updateBoard(player, i)
		if (isWinningPossible(1-player)):
			moves.append(i)
			undoMoves(1)
		else:
			undoMoves(1)
	return moves

# CONCERNING T = 2 (can we trap them and win on our next move)

def isTrappingPossible(player):
	for i in OpenMoves():
		updateBoard(player, i)
		if (isLosingInevitable(1-player)):
			undoMoves(1)
			return True
		else:
			undoMoves(1)
	return False

def movesToTrap(player):
	moves = []
	for i in OpenMoves():
		updateBoard(player, i)
		if (isLosingInevitable(1-player)):
			moves.append(i)
			undoMoves(1)
		else:
			undoMoves(1)
	return moves

# CONCERNING T = 3 (can they trap us)

def isGettingTrappedPossible(player):
	for i in OpenMoves():
		updateBoard(player, i)
		if isTrappingPossible(1-player):
			undoMoves(1)
			return True
		else:
			undoMoves(1)
	return False

def isGettingTrappedInevitable(player):
	for i in OpenMoves():
		updateBoard(player, i)
		if (not isTrappingPossible(1-player)):
			undoMoves(1)
			return False
		else:
			undoMoves(1)
	return True

def movesToGetTrapped(player):
	moves = []
	for i in OpenMoves():
		updateBoard(player, i)
		if (isTrappingPossible(1-player)):
			moves.append(i)
			undoMoves(1)
		else:
			undoMoves(1)
	return moves

# CONCERNING T = 4 (can we win two moves from now)

def isTrapping2xPossible(player):
	for i in OpenMoves():
		updateBoard(player, i)
		if (isGettingTrappedInevitable(1-player)):
			undoMoves(1)
			return True
		else:
			undoMoves(1)
	return False

def movesToTrap2x(player):
	moves = []
	for i in OpenMoves():
		updateBoard(player, i)
		if (isGettingTrappedInevitable(1-player)):
			moves.append(i)
			undoMoves(1)
		else:
			undoMoves(1)
	return moves

# CONCERNING T = 5 (can they trap us and win three moves from now)

def isGettingTrapped2xPossible(player):
	for i in OpenMoves():
		updateBoard(player, i)
		if isTrapping2xPossible(1-player):
			undoMoves(1)
			return True
		else:
			undoMoves(1)
	return False

def isGettingTrapped2xInevitable(player):
	for i in OpenMoves():
		updateBoard(player, i)
		if (not isTrapping2xPossible(1-player)):
			undoMoves(1)
			return False
		else:
			undoMoves(1)
	return True

def movesToGetTrapped2x(player):
	moves = []
	for i in OpenMoves():
		updateBoard(player, i)
		if (isTrapping2xPossible(1-player)):
			moves.append(i)
			undoMoves(1)
		else:
			undoMoves(1)
	return moves
	
# CONCERNING T = 6 (can we win three moves from now)

def isTrapping3xPossible(player):
	for i in OpenMoves():
		updateBoard(player, i)
		if (isGettingTrapped2xInevitable(1-player)):
			undoMoves(1)
			return True
		else:
			undoMoves(1)
	return False

def movesToTrap3x(player):
	moves = []
	for i in OpenMoves():
		updateBoard(player, i)
		if (isGettingTrapped2xInevitable(1-player)):
			moves.append(i)
			undoMoves(1)
		else:
			undoMoves(1)
	return moves

# GAME PLAY
printBoard()
while (not isGameOver):
	if (playerName[turn%2] == 'HAL'):
		updateBoard(turn%2, concrete())
	else:
		updateBoard(turn%2, columnSelection())

	printBoard()

	# at this point, a move has been locked in and all the variables have been updated, but "turn" has not been increased
	if (checkWin()):
		print(playerName[turn%2] + ' has won!')
		isGameOver = True
	if (turn == numCols * numRows - 1):
		print('The game is a tie.')
		isGameOver = True
	else:
		turn = turn + 1
for i in range(8):
	print()

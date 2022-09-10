# ---------
# VARIABLES
# ---------

# establish game defaults
numCols = 7
numRows = 6
playerName = []
blank = ' . '
board = [ [blank]*numRows for i in range(numCols)]
highest = [-1 for i in range(numCols)]
turn = 0
playLog = []
isGameOver = 0
playerToken = [' O ', ' X ']

# ---------------------
# FUNCTIONS — GAME PLAY
# ---------------------

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
def columnSelection():
	column = -1
	while (column < 0 or column > numCols or not isColumnFree(column-1)):
		print(playerName[turn%2] + ' (' + playerToken[turn%2] + '), select a column')
		column = int(input())
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

# ----------------------
# FUNCTIONS — CORE LOGIC
# ----------------------

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

# the check functions gather data about how many 3s, 2s, and 1s are created for one player or blocked for another
def checkCounts(player):
	t = len(playLog) - 1
	x = playLog[t][0]
	y = playLog[t][1]
	counts = [[0, 0, 0, 0], [0, 0, 0, 0]]
	checkV = checkCountsVert(player, x, y)
	checkH = checkCountsHor(player, x, y)
	checkD1 = checkCountsDiagSWNE(player, x, y)
	checkD2 = checkCountsDiagNWSE(player, x, y)
	for i in range(2):
		for j in range(4):
			counts[i][j] = checkV[i][j] + checkH[i][j] + checkD1[i][j] + checkD2[i][j]
	return counts

def checkCountsVert(player, x,y):
	our4s = 0
	our3s = 0
	our2s = 0
	our1s = 0
	their3s = 0
	their2s = 0
	their1s = 0

	if (numRows > 3):
		# make y1 on the board
		ymin = 0
		# make y1 not too far from y
		ymin = max(ymin, y-3)
		# make y4 on the board
		ymax = numRows - 3
		#make y4 not too far from y
		ymax = min(ymax, y+1)
		for y1 in range(ymin, ymax):
			ourTokens = 0
			theirTokens = 0
			p1 = board[x][y1]
			p2 = board[x][y1+1]
			p3 = board[x][y1+2]
			p4 = board[x][y1+3]
			p = []
			p.append(p1)
			p.append(p2)
			p.append(p3)
			p.append(p4)
			for i in range(4):
				if (p[i] == playerToken[player]):
					ourTokens +=1
				if (p[i] == playerToken[1-player]):
					theirTokens +=1
			if (theirTokens == 0):
				if (ourTokens == 4):
					our4s +=1
					break
				if (ourTokens == 3):
					our3s +=1
					break
				if (ourTokens == 2):
					our2s +=1
					break
				if (ourTokens == 1):
					our1s +=1
			if (theirTokens != 0 and ourTokens == 1):
				if (theirTokens == 3):
					their3s +=1
					break
				if (theirTokens == 2):
					their2s +=1
					break
				if (theirTokens ==  1):
					their1s +=1
	return [[our4s, our3s, our2s, our1s], [0, their3s, their2s, their1s]]

def checkCountsHor(player, x,y):
	our4s = 0
	our3s = 0
	our2s = 0
	our1s = 0
	their3s = 0
	their2s = 0
	their1s = 0
	if (numCols > 3):
		# make x1 on the board
		xmin = 0
		# make x1 not too far from x
		xmin = max(xmin, x-3)
		# make x4 on the board
		xmax = numCols - 3
		# make x4 not too far from x
		xmax = min(xmax, x+1)
		for x1 in range(xmin, xmax):
			ourTokens = 0
			theirTokens = 0
			p1 = board[x1][y]
			p2 = board[x1+1][y]
			p3 = board[x1+2][y]
			p4 = board[x1+3][y]
			p = []
			p.append(p1)
			p.append(p2)
			p.append(p3)
			p.append(p4)
			for i in range(4):
				if (p[i] == playerToken[player]):
					ourTokens +=1
				if (p[i] == playerToken[1-player]):
					theirTokens +=1
			if (theirTokens == 0):
				if (ourTokens == 4):
					our4s +=1
				if (ourTokens == 3):
					our3s +=1
				if (ourTokens == 2):
					our2s +=1
				if (ourTokens == 1):
					our1s +=1
			if (theirTokens != 0 and ourTokens == 1):
				if (theirTokens == 3):
					their3s +=1
				if (theirTokens == 2):
					their2s +=1
				if (theirTokens ==  1):
					their1s +=1
	return [[our4s, our3s, our2s, our1s], [0, their3s, their2s, their1s]]

def checkCountsDiagSWNE(player, x,y):
	our4s = 0
	our3s = 0
	our2s = 0
	our1s = 0
	their3s = 0
	their2s = 0
	their1s = 0
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
			ourTokens = 0
			theirTokens = 0
			p1 = board[x1][y1]
			p2 = board[x1+1][y1+1]
			p3 = board[x1+2][y1+2]
			p4 = board[x1+3][y1+3]
			p = []
			p.append(p1)
			p.append(p2)
			p.append(p3)
			p.append(p4)
			for i in range(4):
				if (p[i] == playerToken[player]):
					ourTokens +=1
				if (p[i] == playerToken[1-player]):
					theirTokens +=1
			if (theirTokens == 0):
				if (ourTokens == 4):
					our4s +=1
				if (ourTokens == 3):
					our3s +=1
				if (ourTokens == 2):
					our2s +=1
				if (ourTokens == 1):
					our1s +=1
			if (theirTokens != 0 and ourTokens == 1):
				if (theirTokens == 3):
					their3s +=1
				if (theirTokens == 2):
					their2s +=1
				if (theirTokens ==  1):
					their1s +=1
	return [[our4s, our3s, our2s, our1s], [0, their3s, their2s, their1s]]

def checkCountsDiagNWSE(player, x,y):
	our4s = 0
	our3s = 0
	our2s = 0
	our1s = 0
	their3s = 0
	their2s = 0
	their1s = 0
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
			ourTokens = 0
			theirTokens = 0
			p1 = board[x1][y1]
			p2 = board[x1+1][y1-1]
			p3 = board[x1+2][y1-2]
			p4 = board[x1+3][y1-3]
			p = []
			p.append(p1)
			p.append(p2)
			p.append(p3)
			p.append(p4)
			for i in range(4):
				if (p[i] == playerToken[player]):
					ourTokens +=1
				if (p[i] == playerToken[1-player]):
					theirTokens +=1
			if (theirTokens == 0):
				if (ourTokens == 4):
					our4s +=1
				if (ourTokens == 3):
					our3s +=1
				if (ourTokens == 2):
					our2s +=1
				if (ourTokens == 1):
					our1s +=1
			if (theirTokens != 0 and ourTokens == 1):
				if (theirTokens == 3):
					their3s +=1
				if (theirTokens == 2):
					their2s +=1
				if (theirTokens ==  1):
					their1s +=1
	return [[our4s, our3s, our2s, our1s], [0, their3s, their2s, their1s]]

# ------------
# BOT PROFILES
# ------------

# HAL bots:
# Each HALx will consider x moves ahead; e.g. HAL0 only considers its first move but ignores whether the opponent will have opportunities to win.
# HALx bots default to center-most column choices

def HAL0():
	turnsRemaining = numCols * numRows - turn
	if (turnsRemaining == 0):
		print('Uh oh, there shouldnt be any turns remaining')
	moves = OpenMoves()
	if (len(moves) == 1):
		return moves[0]
	player = turn%2
	if (isWinningPossible(player, moves)):
		return movesToWin(player, moves)[0]
	return choiceMiddleOut(moves)

# Pyle is just HAL1 (with middle-out default)
def Pyle():
	turnsRemaining = numCols * numRows - turn
	if (turnsRemaining == 0):
		print('Uh oh, there shouldnt be any turns remaining')
	moves = OpenMoves()
	if (len(moves) == 1):
		return moves[0]
	player = turn%2
	if (isWinningPossible(player, moves)):
		return movesToWin(player, moves)[0]
	if (turnsRemaining > 1):
		if (isLosingInevitable(player, moves)):
			return moves[0]
		if (isLosingPossible(player, moves)):
			for i in movesToLose(player, moves):
				moves.remove(i)
				if (len(moves) == 0):
					print('Uh oh, all moves have been ruled out')
	return choiceMiddleOut(moves)

# Mandrake is just HAL2 (with middle-out default)
def Mandrake():
	turnsRemaining = numCols * numRows - turn
	if (turnsRemaining == 0):
		print('Uh oh, there shouldnt be any turns remaining')
	moves = OpenMoves()
	if (len(moves) == 1):
		return moves[0]
	player = turn%2
	if (isWinningPossible(player, moves)):
		return movesToWin(player, moves)[0]
	if (turnsRemaining > 1):
		if (isLosingInevitable(player, moves)):
			return moves[0]
		if (isLosingPossible(player, moves)):
			for i in movesToLose(player, moves):
				moves.remove(i)
				if (len(moves) == 0):
					print('Uh oh, all moves have been ruled out')
	if (turnsRemaining > 2):
		if (isTrappingPossible(player, moves)):
			for i in movesToTrap(player, moves):
				for j in moves:
					if (i == j):
						return i
	return choiceMiddleOut(moves)

def HAL3():
	turnsRemaining = numCols * numRows - turn
	if (turnsRemaining == 0):
		print('Uh oh, there shouldnt be any turns remaining')
	moves = OpenMoves()
	if (len(moves) == 1):
		return moves[0]
	player = turn%2
	if (isWinningPossible(player, moves)):
		return movesToWin(player, moves)[0]
	if (turnsRemaining > 1):
		if (isLosingInevitable(player, moves)):
			return moves[0]
		if (isLosingPossible(player, moves)):
			for i in movesToLose(player, moves):
				moves.remove(i)
				if (len(moves) == 0):
					print('Uh oh, all moves have been ruled out')
	if (turnsRemaining > 2):
		if (isTrappingPossible(player, moves)):
			for i in movesToTrap(player, moves):
				for j in moves:
					if (i == j):
						return i
	if (turnsRemaining > 3):
		if (isGettingTrappedInevitable(player, moves)):
			return moves[0]
		if (isGettingTrappedPossible(player, moves)):
			for i in movesToGetTrapped(player, moves):
				moves.remove(i)
				if (len(moves) == 0):
					print('Uh oh, all moves have been ruled out')
	return choiceMiddleOut(moves)

def HAL4():
	turnsRemaining = numCols * numRows - turn
	if (turnsRemaining == 0):
		print('Uh oh, there shouldnt be any turns remaining')
	moves = OpenMoves()
	if (len(moves) == 1):
		return moves[0]
	player = turn%2
	if (isWinningPossible(player, moves)):
		return movesToWin(player, moves)[0]
	if (turnsRemaining > 1):
		if (isLosingInevitable(player, moves)):
			return moves[0]
		if (isLosingPossible(player, moves)):
			for i in movesToLose(player, moves):
				moves.remove(i)
				if (len(moves) == 0):
					print('Uh oh, all moves have been ruled out')
	if (turnsRemaining > 2):
		if (isTrappingPossible(player, moves)):
			for i in movesToTrap(player, moves):
				for j in moves:
					if (i == j):
						return i
	if (turnsRemaining > 3):
		if (isGettingTrappedInevitable(player, moves)):
			return moves[0]
		if (isGettingTrappedPossible(player, moves)):
			for i in movesToGetTrapped(player, moves):
				moves.remove(i)
				if (len(moves) == 0):
					print('Uh oh, all moves have been ruled out')
	if (turnsRemaining > 4):
		if (isTrapping2xPossible(player, moves)):
			for i in movesToTrap2x(player, moves):
				for j in moves:
					if (i == j):
						return i
	return choiceMiddleOut(moves)

def HAL5():
	turnsRemaining = numCols * numRows - turn
	if (turnsRemaining == 0):
		print('Uh oh, there shouldnt be any turns remaining')
	moves = OpenMoves()
	if (len(moves) == 1):
		return moves[0]
	player = turn%2
	if (isWinningPossible(player, moves)):
		return movesToWin(player, moves)[0]
	if (turnsRemaining > 1):
		if (isLosingInevitable(player, moves)):
			return moves[0]
		if (isLosingPossible(player, moves)):
			for i in movesToLose(player, moves):
				moves.remove(i)
				if (len(moves) == 0):
					print('Uh oh, all moves have been ruled out')
	if (turnsRemaining > 2):
		if (isTrappingPossible(player, moves)):
			for i in movesToTrap(player, moves):
				for j in moves:
					if (i == j):
						return i
	if (turnsRemaining > 3):
		if (isGettingTrappedInevitable(player, moves)):
			return moves[0]
		if (isGettingTrappedPossible(player, moves)):
			for i in movesToGetTrapped(player, moves):
				moves.remove(i)
				if (len(moves) == 0):
					print('Uh oh, all moves have been ruled out')
	if (turnsRemaining > 4):
		if (isTrapping2xPossible(player, moves)):
			for i in movesToTrap2x(player, moves):
				for j in moves:
					if (i == j):
						return i
	if (turnsRemaining > 5):
		if (isGettingTrapped2xInevitable(player, moves)):
			return moves[0]
		if (isGettingTrapped2xPossible(player, moves)):
			for i in movesToGetTrapped2x(player, moves):
				moves.remove(i)
				if (len(moves) == 0):
					print('Uh oh, all moves have been ruled out')
	return choiceMiddleOut(moves)

def HAL6():
	turnsRemaining = numCols * numRows - turn
	if (turnsRemaining == 0):
		print('Uh oh, there shouldnt be any turns remaining')
	moves = OpenMoves()
	if (len(moves) == 1):
		return moves[0]
	player = turn%2
	if (isWinningPossible(player, moves)):
		return movesToWin(player, moves)[0]
	if (turnsRemaining > 1):
		if (isLosingInevitable(player, moves)):
			return moves[0]
		if (isLosingPossible(player, moves)):
			for i in movesToLose(player, moves):
				moves.remove(i)
				if (len(moves) == 0):
					print('Uh oh, all moves have been ruled out')
	if (turnsRemaining > 2):
		if (isTrappingPossible(player, moves)):
			for i in movesToTrap(player, moves):
				for j in moves:
					if (i == j):
						return i
	if (turnsRemaining > 3):
		if (isGettingTrappedInevitable(player, moves)):
			return moves[0]
		if (isGettingTrappedPossible(player, moves)):
			for i in movesToGetTrapped(player, moves):
				moves.remove(i)
				if (len(moves) == 0):
					print('Uh oh, all moves have been ruled out')
	if (turnsRemaining > 4):
		if (isTrapping2xPossible(player, moves)):
			for i in movesToTrap2x(player, moves):
				for j in moves:
					if (i == j):
						return i
	if (turnsRemaining > 5):
		if (isGettingTrapped2xInevitable(player, moves)):
			return moves[0]
		if (isGettingTrapped2xPossible(player, moves)):
			for i in movesToGetTrapped2x(player, moves):
				moves.remove(i)
				if (len(moves) == 0):
					print('Uh oh, all moves have been ruled out')
	if (turnsRemaining > 6):
		if (isTrapping3xPossible(player, moves)):
			for i in movesToTrap3x(player, moves):
				for j in moves:
					if (i == j):
						return i
	return choiceMiddleOut(moves)

# HAL is HAL6 (with choiceNeutral default)
def HAL():
	turnsRemaining = numCols * numRows - turn
	if (turnsRemaining == 0):
		print('Uh oh, there shouldnt be any turns remaining')
	moves = OpenMoves()
	if (len(moves) == 1):
		return moves[0]
	player = turn%2
	if (isWinningPossible(player, moves)):
		return movesToWin(player, moves)[0]
	if (turnsRemaining > 1):
		if (isLosingInevitable(player, moves)):
			return moves[0]
		if (isLosingPossible(player, moves)):
			for i in movesToLose(player, moves):
				moves.remove(i)
				if (len(moves) == 0):
					print('Uh oh, all moves have been ruled out')
	if (turnsRemaining > 2):
		if (isTrappingPossible(player, moves)):
			for i in movesToTrap(player, moves):
				for j in moves:
					if (i == j):
						return i
	if (turnsRemaining > 3):
		if (isGettingTrappedInevitable(player, moves)):
			return moves[0]
		if (isGettingTrappedPossible(player, moves)):
			for i in movesToGetTrapped(player, moves):
				moves.remove(i)
				if (len(moves) == 0):
					print('Uh oh, all moves have been ruled out')
	if (turnsRemaining > 4):
		if (isTrapping2xPossible(player, moves)):
			for i in movesToTrap2x(player, moves):
				for j in moves:
					if (i == j):
						return i
	if (turnsRemaining > 5):
		if (isGettingTrapped2xInevitable(player, moves)):
			return moves[0]
		if (isGettingTrapped2xPossible(player, moves)):
			for i in movesToGetTrapped2x(player, moves):
				moves.remove(i)
				if (len(moves) == 0):
					print('Uh oh, all moves have been ruled out')
	if (turnsRemaining > 6):
		if (isTrapping3xPossible(player, moves)):
			for i in movesToTrap3x(player, moves):
				for j in moves:
					if (i == j):
						return i
	return choiceNeutral(player, moves)

# Alex looks for wins and traps but ignores opponent's options and favors columns that improve his board
def Alex():
	turnsRemaining = numCols * numRows - turn
	if (turnsRemaining == 0):
		print('Uh oh, there shouldnt be any turns remaining')
	moves = OpenMoves()
	if (len(moves) == 1):
		return moves[0]
	player = turn%2
	if (isWinningPossible(player, moves)):
		return movesToWin(player, moves)[0]
	if (turnsRemaining > 2):
		if (isTrappingPossible(player, moves)):
			for i in movesToTrap(player, moves):
				for j in moves:
					if (i == j):
						return i
	if (turnsRemaining > 4):
		if (isTrapping2xPossible(player, moves)):
			for i in movesToTrap2x(player, moves):
				for j in moves:
					if (i == j):
						return i
	if (turnsRemaining > 6):
		if (isTrapping3xPossible(player, moves)):
			for i in movesToTrap3x(player, moves):
				for j in moves:
					if (i == j):
						return i
	return choiceOffense(player, moves)

# Dax attempts to thwart the opponent's wins and traps and favors columns that block the opponent
def Dax():
	turnsRemaining = numCols * numRows - turn
	if (turnsRemaining == 0):
		print('Uh oh, there shouldnt be any turns remaining')
	moves = OpenMoves()
	if (len(moves) == 1):
		return moves[0]
	player = turn%2
	if (turnsRemaining > 1):
		if (isLosingInevitable(player, moves)):
			return moves[0]
		if (isLosingPossible(player, moves)):
			for i in movesToLose(player, moves):
				moves.remove(i)
				if (len(moves) == 0):
					print('Uh oh, all moves have been ruled out')
	if (turnsRemaining > 3):
		if (isGettingTrappedInevitable(player, moves)):
			return moves[0]
		if (isGettingTrappedPossible(player, moves)):
			for i in movesToGetTrapped(player, moves):
				moves.remove(i)
				if (len(moves) == 0):
					print('Uh oh, all moves have been ruled out')
	if (turnsRemaining > 5):
		if (isGettingTrapped2xInevitable(player, moves)):
			return moves[0]
		if (isGettingTrapped2xPossible(player, moves)):
			for i in movesToGetTrapped2x(player, moves):
				moves.remove(i)
				if (len(moves) == 0):
					print('Uh oh, all moves have been ruled out')
	return choiceDefense(player, moves)

# ---------------------------------
# FUNCTIONS — ABSOLUTIST STRATEGIES
# ---------------------------------

# CONCERNING T = 0 (could the game end on this (our) turn, i.e. can we win in one move)

def isWinningPossible(player, moves):
	# can P1 choose 1 move that wins
	for i in moves:
		updateBoard(player, i)
		if (checkWin()):
			undoMoves(1)
			return True
		else:
			undoMoves(1)
	return False

def movesToWin(player, moves):
	movesToWin = []
	for i in moves:
		updateBoard(player, i)
		if (checkWin()):
			undoMoves(1)
			movesToWin.append(i)
		else:
			undoMoves(1)
	return movesToWin

# CONCERNING T = 1 (could the game end on their next turn)

def isLosingPossible(player, moves):
	for i in moves:
		updateBoard(player, i)
		if (isWinningPossible(1-player, OpenMoves())):
			undoMoves(1)
			return True
		else:
			undoMoves(1)
	return False

def isLosingInevitable(player, moves):
	if (isWinningPossible(player, OpenMoves())):
		return False
	for i in moves:
		updateBoard(player, i)
		if (not isWinningPossible(1-player, OpenMoves())):
			undoMoves(1)
			return False
		else:
			undoMoves(1)
	return True

def movesToLose(player, moves):
	movesToLose = []
	for i in moves:
		updateBoard(player, i)
		if (isWinningPossible(1-player, OpenMoves())):
			movesToLose.append(i)
			undoMoves(1)
		else:
			undoMoves(1)
	return movesToLose

# CONCERNING T = 2 (can we trap them and win on our next move)

def isTrappingPossible(player, moves):
	for i in moves:
		updateBoard(player, i)
		if (isLosingInevitable(1-player, OpenMoves())):
			undoMoves(1)
			return True
		else:
			undoMoves(1)
	return False

def movesToTrap(player, moves):
	movesToTrap = []
	for i in moves:
		updateBoard(player, i)
		if (isLosingInevitable(1-player, OpenMoves())):
			movesToTrap.append(i)
			undoMoves(1)
		else:
			undoMoves(1)
	return movesToTrap

# CONCERNING T = 3 (can they trap us)

def isGettingTrappedPossible(player, moves):
	for i in moves:
		updateBoard(player, i)
		if isTrappingPossible(1-player, OpenMoves()):
			undoMoves(1)
			return True
		else:
			undoMoves(1)
	return False

def isGettingTrappedInevitable(player, moves):
	if (isWinningPossible(player, OpenMoves())):
		return False
	for i in moves:
		updateBoard(player, i)
		if (not isTrappingPossible(1-player, OpenMoves())):
			undoMoves(1)
			return False
		else:
			undoMoves(1)
	return True

def movesToGetTrapped(player, moves):
	movesToGetTrapped = []
	for i in moves:
		updateBoard(player, i)
		if (isTrappingPossible(1-player, OpenMoves())):
			movesToGetTrapped.append(i)
			undoMoves(1)
		else:
			undoMoves(1)
	return movesToGetTrapped

# CONCERNING T = 4 (can we win two moves from now)

def isTrapping2xPossible(player, moves):
	for i in moves:
		updateBoard(player, i)
		if (isGettingTrappedInevitable(1-player, OpenMoves())):
			undoMoves(1)
			return True
		else:
			undoMoves(1)
	return False

def movesToTrap2x(player, moves):
	movesToTrap2x = []
	for i in moves:
		updateBoard(player, i)
		if (isGettingTrappedInevitable(1-player, OpenMoves())):
			movesToTrap2x.append(i)
			undoMoves(1)
		else:
			undoMoves(1)
	return movesToTrap2x

# CONCERNING T = 5 (can they trap us and win three moves from now)

def isGettingTrapped2xPossible(player, moves):
	for i in moves:
		updateBoard(player, i)
		if isTrapping2xPossible(1-player, OpenMoves()):
			undoMoves(1)
			return True
		else:
			undoMoves(1)
	return False

def isGettingTrapped2xInevitable(player, moves):
	if (isWinningPossible(player, OpenMoves())):
		return False
	for i in moves:
		updateBoard(player, i)
		if (not isTrapping2xPossible(1-player, OpenMoves())):
			undoMoves(1)
			return False
		else:
			undoMoves(1)
	return True

def movesToGetTrapped2x(player, moves):
	movesToGetTrapped2x = []
	for i in moves:
		updateBoard(player, i)
		if (isTrapping2xPossible(1-player, OpenMoves())):
			movesToGetTrapped2x.append(i)
			undoMoves(1)
		else:
			undoMoves(1)
	return movesToGetTrapped2x
	
# CONCERNING T = 6 (can we win three moves from now)

def isTrapping3xPossible(player, moves):
	for i in moves:
		updateBoard(player, i)
		if (isGettingTrapped2xInevitable(1-player, OpenMoves())):
			undoMoves(1)
			return True
		else:
			undoMoves(1)
	return False

def movesToTrap3x(player, moves):
	movesToTrap3x = []
	for i in moves:
		updateBoard(player, i)
		if (isGettingTrapped2xInevitable(1-player, OpenMoves())):
			movesToTrap3x.append(i)
			undoMoves(1)
		else:
			undoMoves(1)
	return movesToTrap3x

# ------------------------------------
# FUNCTIONS — PROBABILISTIC STRATEGIES
# ------------------------------------

# chooses the middle-most available move
def choiceMiddleOut(moves):
	if (numCols%2 == 1):
		mid = int((numCols-1)/2)
		for i in moves:
			if (i == mid):
				return mid
	else:
		mid = int(numCols/2)
	for i in range(mid):
		p1 = mid-i-1
		if (numCols%2 == 1):
			p2 = mid+i+1
		else:
			p2 = mid+i
		for j in moves:
			if (j == p1):
				return p1
			if (j == p2):
				return p2
	return moves[0]

# chooses a random available move
def choiceRandom(moves):
	mod = len(moves)
	index = turnsRemaining*turn + 19 + moves[0] + highest[numCols-1]
	return moves[index%mod]

# chooses the best move available according to the advantages it affords in CREATING AND BLOCKING 4s, 3s, 2s, and 1s
def choiceNeutral(player, moves):
	theMove = moves[0]
	maxValue = -99999
	temp = 0
	for i in range(len(moves)):
		updateBoard(player, moves[i])

		counts = checkCounts(player)
		count = 0
		count += counts[0][0] * (1000000000000)
		count += counts[1][1] * (10000000000)
		count += counts[0][1] * (100000000)
		count += counts[1][2] * (1000000)
		count += counts[0][2] * (10000)
		count += counts[1][3] * (100)
		count += counts[0][3]

		temp = count
		undoMoves(1)
		if (temp > maxValue):
			maxValue = temp
			theMove = moves[i]
	return theMove

# chooses the best move available according to the advantages it affords in CREATING 4s, 3s, 2s, and 1s
def choiceOffense(player, moves):
	theMove = moves[0]
	maxValue = -99999
	temp = 0
	for i in range(len(moves)):
		updateBoard(player, moves[i])

		counts = checkCounts(player)
		count = 0
		count += counts[0][0] * (1000000000000)
		count += counts[0][1] * (100000000)
		count += counts[0][2] * (10000)
		count += counts[0][3]

		temp = count
		undoMoves(1)
		if (temp > maxValue):
			maxValue = temp
			theMove = moves[i]
	return theMove

# chooses the best move available according to the advantages it affords in BLOCKING 4s, 3s, 2s, and 1s
def choiceDefense(player, moves):
	theMove = moves[0]
	maxValue = -99999
	temp = 0
	for i in range(len(moves)):
		updateBoard(player, moves[i])

		counts = checkCounts(player)
		count = 0
		count += counts[1][1] * (10000000000)
		count += counts[1][2] * (1000000)
		count += counts[1][3] * (100)

		temp = count
		undoMoves(1)
		if (temp > maxValue):
			maxValue = temp
			theMove = moves[i]
	return theMove

# --------------
# GAME EXECUTION
# --------------

# choose player names or computer profiles
for i in range(8):
	print()
print('     ****************')
print('     * CONNECT FOUR *')
print('     ****************')
for i in range(8):
	print()
print('Each player may play manually or name a bot to play your moves')
print('')
print('Bot profiles:')
print('  Alex:      considers offense only')
print('  Dax:       considers defense only')
print('  Pyle:      thinks 1 move ahead')
print('  Mandrake:  thinks 2 moves ahead')
print('  HAL:       thinks 6 moves ahead')
for i in range(4):
	print()
print('Enter PLAYER ONE name')
playerName.append(input())
print('Enter PLAYER TWO name')
playerName.append(input())
printBoard()
while (isGameOver == 0):
	print('Move: ' + str(turn + 1))
	print(playerName[turn%2] + ', it is your turn.')
	if (playerName[turn%2] == 'Alex'):
		updateBoard(turn%2, Alex())
	elif (playerName[turn%2] == 'Dax'):
		updateBoard(turn%2, Dax())
	elif (playerName[turn%2] == 'Pyle'):
		updateBoard(turn%2, Pyle())
	elif (playerName[turn%2] == 'Mandrake'):
		updateBoard(turn%2, Mandrake())
	elif (playerName[turn%2] == 'HAL'):
		updateBoard(turn%2, HAL())
	else:
		updateBoard(turn%2, columnSelection())
	printBoard()
	# at this point, a move has been locked in and all the variables have been updated, but "turn" has not been increased
	if (checkWin()):
		print(playerName[turn%2] + ' has won!')
		isGameOver = 1
	if (turn == numCols * numRows - 1):
		print('The game is a tie.')
		isGameOver = 1
	else:
		turn = turn + 1
for i in range(8):
	print()

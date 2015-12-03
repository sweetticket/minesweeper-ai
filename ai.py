import random
import re
import time
from string import ascii_lowercase
import math
from game_constants import *

BF_LIMIT = 8

def getrandomcell(grid):
    gridsize = len(grid)
    a = random.randint(0, gridsize - 1)
    b = random.randint(0, gridsize - 1)
    return (a, b)

def firstMove(currgrid):
	gridsize = len(currgrid)
	moves = [(0, 0), (0, gridsize-1), (gridsize-1, 0), (gridsize-1, gridsize-1)]
	return [{'cell': random.choice(moves), 'flag': False, 'message': ""}]


""" Counts the number of flags around a given position.
	row i, col j """
def countFlagsAround(currgrid, flags, i, j):
	mines = 0
	gridsize = len(currgrid)
	# see if we're on the edge of the board
	oU = False
	oD = False
	oL = False
	oR = False

	if i == 0:
		oU = True
	if j == 0:
		oL = True
	if i == gridsize-1:
		oD = True
	if j == gridsize-1:
		oR = True

	if not oU and (i-1, j) in flags:
		mines += 1
	if not oL and (i, j-1) in flags:
		mines += 1
	if not oD and (i+1, j-1) in flags:
		mines += 1
	if not oR and (i-1, j+1) in flags:
		mines += 1
	if not oU and not oL and (i-1, j-1) in flags:
		mines += 1
	if not oU and not oR and (i-1, j+1) in flags:
		mines += 1
	if not oD and not oL and (i+1, j-1) in flags:
		mines += 1
	if not oD and not oR and (i+1, j+1) in flags:
		mines += 1
	return mines

""" Counts the number of unopened squares around a given position. """
def getUnopenedAround(currgrid, i, j):
	freeSquares = []
	if currgrid[i-1][j] == ' ':
		freeSquares.append((i-1, j))
	if currgrid[i+1][j] == ' ':
		freeSquares.append((i+1, j))
	if currgrid[i][j-1] == ' ':
		freeSquares.append((i, j-1))
	if currgrid[i][j+1] == ' ':
		freeSquares.append((i, j+1))
	if currgrid[i+1][j+1] == ' ':
		freeSquares.append((i+1, j+1))
	if currgrid[i-1][j-1] == ' ':
		freeSquares.append((i-1, j-1))
	return freeSquares

""" A boundry square is an unopened square with opened squares near it. """
def isBoundary(currgrid, i, j):
	gridsize = len(grid)
	if grid[i][j] != ' ':
		return False

	oU = False
	oD = False
	oL = False
	oR = False

	if i == 0:
		oU = True
	if j == 0:
		oL = True
	if i == gridsize-1:
		oD = True
	if j == gridsize-1:
		oR = True

	if not oU and grid[i-1][j] != ' ':
		return True
	if not oL and grid[i][j-1] != ' ':
		return True
	if not oD and grid[i+1][j] != ' ':
		return True
	if not oR and grid[i][j+1] != ' ':
		return True

	if not oU and not oL and grid[i-1][j-1] != ' ':
		return True
	if not oU and not oR and grid[i-1][j+1] != ' ':
		return True
	if not oD and grid[i+1][j-1] != ' ':
		return True
	if not oD and grid[i+1][j+1] != ' ':
		return True

""" Attempt to deduce squares that we know have mines
  	More specifically if number of squares around it = its number. """
def attemptFlagMine(currgrid):
	for i in range(len(currgrid)):
		for j in range(len(currgrid)):
			if isinstance(currgrid[i][j], int) and currgrid[i][j] >= 1:
				unopened = getUnopenedAround(currgrid, i, j)
				if currgrid[i][j] == len(unopened):
					for ii in range(len(currgrid)):
						for jj in range(len(currgrid)):
							if math.abs(ii-i) <= 1 and math.abs(jj-j) <= 1:
								if currgrid[ii][jj] == ' ':
									return [{'cell': (ii, jj), 'flag': True, 'message': ""}]
	return False

""" Attempt to deduce a spot that should be free and click it
  	More specifically:
  	Find a square where the number of flags around it is the same as it
  	Then click every empty square around it. """
def attemptMove(currgrid, flags):
	for i in range(len(currgrid)):
		for j in range(len(currgrid)):
			if isinstance(currgrid[i][j], int) and currgrid[i][j] >= 1:
				curNum = currgrid[i][j]
				minesAround = countFlagsAround(currgrid, flags, i, j)
				unopenedAround = getUnopenedAround(currgrid, i, j)
				if curNum == minesAround and len(unopenedAround) > minesAround:
					success = True
					if len(unopenedAround) - minesAround > 1:
						moves = []
						for cell in unopenedAround:
							moves.append({'cell': cell, 'flag': False, 'message': ""})
							return moves
	return guessRandomly(currgrid)
	# tankSolver()

def guessRandomly(currgrid):
	print "guessing"
	while True:
		(rowno, colno) = getrandomcell(currgrid)
		if currgrid[rowno][colno] == ' ':
			return [{'cell': (rowno, colno), 'flag': False, 'message': ""}]

def getBorderTiles(currgrid, flags):
	borderTiles = []
	# Determine all border tiles
	for i in range(len(currgrid)):
    	for j in range(len(currgrid)):
    		if isBoundary(currgrid, i, j) and (i, j) not in flags:
        		borderTiles.append((i, j))
 	return borderTiles

 def getAllUnopenedTiles(currgrid):
 	allUnopenedTiles = []
 	for i in range(len(currgrid)):
    	for j in range(len(currgrid)):
      		if currgrid[i][j] == ' ':
        		allUnopenedTiles.append((i, j))

def tileSearch(currgrid, (ci, cj), (ti, tj)):
  for i in range(len(currgrid)):
    for j in range(len(currgrid)):
      if isInstance(currgrid[i][j], int) and currgrid[i][j] > 0:
        if math.abs(ci-i) <= 1 and math.abs(cj-j) <= 1 and math.abs(ti-i) <= 1 and math.abs(tj-j) <= 1:
          return True
  return False

def tankSegregate(borderTiles):
	allRegions = [] # array of arrays
	covered = []

	while True:
		queue = Queue.Queue()
		finishedRegion = []

		# Find a suitable starting point
		for firstT in borderTiles:
			if firstT not in covered:
				queue.put(firstT)
				break
		if queue.empty():
			break

		while not queue.empty():
			(ci, cj) = queue.get()
			finishedRegion.append((ci, cj))
			covered.append((ci, cj))

			# Find all connecting tiles
			for (ti, tj) in borderTiles:
				isConnected = False
				if (ti, tj) not in finishedRegion:
					isConnected = tilesearch(currgrid, (ci, cj), (ti, tj))
					if isConnected and (ti, tj) not in queue:
						queue.put((ti, tj))
		allRegions.append(finishedRegion)

	return allRegions

def getKnownEmptyTiles(currgrid):
	knownEmpty = []
	for i in range(len(currgrid)):
      for j in range(len(currgrid)):
        if isInstance(tank_board[i][j], int) and tank_board[i][j] >= 0:
          knownEmpty.append((i, j))
    return knownEmpty

def tankRecurse(currgrid, borderTiles, k, knownEmpty, knownMines, tank_board):
	flagCount = 0
	for i in range(len(tank_board)):
		for j in range(len(tank_board)):
			# Count flags for endgame cases
			if (i, j) in knownMines:
				flagCount += 1
			num = tank_board[i][j]

			if isInstance(num, int):			
				surround = 0 # number of surrounding tiles
				if (i == 0 and j == 0) or (i == len(tank_board)-1 and j == len(tank_board)-1):
					surround = 3
				else if i == 0 or j == 0 or i == len(tank_board)-1 or j == len(tank_board)-1:
					surround = 5
				else:
					surround = 8
				numFlags = countFlagsAround(tank_board, knownMines, i, j)
				numFree = len(getUnopenedAround(tank_board, i, j))

				# Scenario 1: too many mines
				if numFlags > num:
					return (tank_solutions, knownMines, knownEmpty)

				# Scenario 2: too many empty
				if surround - numFree < num:
					return (tank_solutions, knownMines, knownEmpty)

	if flagCount > numberofmines:
		return (tank_solutions, knownMines, knownEmpty)

	if k == len(borderTiles):
		if not borderOptimization and flagCount < numberofmines:
			return (tank_solutions, knownMines, knownEmpty)
		
		solution = [] # array of possible mine locations
		for i in range(len(borderTiles)):
			(si, sj) = borderTiles[i]
			if (si, sj) in knownMines:
				solution.append((si, sj))
		tank_solutions.append(solution)
		return (tank_solutions, knownMines, knownEmpty)

	(qi, qj) = borderTiles[k]

	# Recurse two positions: mine and no mine
	knownMines.append((qi, qj))
	(tank_solutions, knownMines, knownEmpty) = tankRecurse(currgrid, borderTiles, k+1, knownEmpty, knownMines, tank_board)
	knownMines.remove((qi, qj))

	knownEmpty.append((qi, qj))
	(tank_solutions, knownMines, knownEmpty) = tankRecurse(currgrid, borderTiles, k+1, knownEmpty, knownMines, tank_board)
	knownEmpty.remove((qi, qj))

def tankSolver(currgrid, flags):
	borderTiles = getBorderTiles(currgrid, flags)
	allUnopenedTiles = getAllUnopenedTiles(currgrid)
	
	# Count how many squares outside the knowable range
	numOutSquares = len(allUnopenedTiles) - len(borderTiles)
	if numOutSquares > BF_LIMIT:
		borderOptimization = True
	else:
		borderTiles = allUnopenedTiles

	# Something went wrong
	if len(borderTiles) == 0:
		print "Error: len(borderTiles) == 0"
		return []

	# Run the segregation routine before recursing one by one
 	# Don't bother if it's endgame as doing so might make it miss some cases
 	segregated = [] # array of arrays
 	if not borderOptimization:
 		segregated.append(borderTiles)
 	else:
 		segregated = tankSolver(borderTiles)

 	prob_best = 0
 	prob_besttile = -1
 	prob_best_s = -1

 	for s in range(len(segregated)):
 		tank_solutions = []
 		tank_board = currgrid[:]
 		knownMines = flags[:]
 		knownEmpty = getKnownEmptyTiles(tank_board)

 		# Compute solutions
 		(tank_solutions, knownMines, knownEmpty)  = tankRecurse(currgrid, segregated[s], 0, knownEmpty, knownMines, tank_board)

 		# In case something went wrong
 		if len(tank_solutions) == 0:
 			print "Error: len(tank_solutions) == 0"
 			return []

 		# Check for solved squares
 		for i in range(len(segregated[s])):
 			allMine = True
 			allEmpty = True
 			for sln in tank_solutions:
 				if segregated[s][i] in sln:
 					allEmpty = False
 				if segregated[s][i] not in sln:
 					allMine = False

 			(qi, qj) = segregated[s][i]
 			if allMine:
 				return [{'cell': (qi, qj), 'flag': True, 'message': ""}]
 			if allEmpty:
 				return [{'cell': (qi, qj), 'flag': False, 'message': ""}]

 			# Calculate probabilities, in case we need it
 			maxEmpty = -100000
 			iEmpty = -1

 			for i in range(len(segregated[s])):
 				nEmpty = 0
 				for sln in tank_solutions:
 					if segregated[s][i] not in sln:
 						nEmpty += 1
 					if nEmpty > maxEmpty:
 						maxEmpty = nEmpty
 						iEmpty = i
 				probability = float(maxEmpty) / len(tank_solutions)
 				if probability > prob_best:
 					prob_besttile = iEmpty
 					prob_best_s = s

 			# todo: bruteforce... extend BF_LIMIT
 			cell = segregated[prob_best_s][prob_besttile]
 			return [{'cell': cell, 'flag': False, 'message': ""}]


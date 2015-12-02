import random
import re
import time
from string import ascii_lowercase
import math

def getrandomcell(grid):
    gridsize = len(grid)
    a = random.randint(0, gridsize - 1)
    b = random.randint(0, gridsize - 1)
    return (a, b)


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
	while True:
		(rowno, colno) = getrandomcell(currgrid)
		if currgrid[rowno][colno] == ' ':
			return [{'cell': (rowno, colno), 'flag': False, 'message': ""}]

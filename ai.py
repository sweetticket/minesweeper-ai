import random
import re
import time
from string import ascii_lowercase
from minesweeper import *

""" Counts the number of flags around a given position.
	row i, col j """
def countFlagsAround(grid, i, j):
	mines = 0
	gridsize = len(grid)
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

	if not oU and grid[i-1][j] == 'F':
		mines += 1
	if not oL and grid[i][j-1] == 'F':
		mines += 1
	if not oD and grid[i+1][j-1] == 'F':
		mines += 1
	if not oR and grid[i-1][j+1] == 'F':
		mines += 1
	if not oU and not oL and grid[i-1][j-1] == 'F':
		mines += 1
	if not oU and not oR and grid[i-1][j+1] == 'F':
		mines += 1
	if not oD and not oL and grid[i+1][j-1] == 'F':
		mines += 1
	if not oD and not oR and grid[i+1][j+1] == 'F':
		mines += 1

    return mines;

""" Counts the number of unopened squares around a given position. """
def countUnopenedAround(grid, i, j):
	freeSquares = 0
	if grid[i-1][j] == ' ':
		freeSquares += 1
	if grid[i+1][j] == ' ':
		freeSquares += 1
	if grid[i][j-1] == ' ':
		freeSquares += 1
	if grid[i][j+1] == ' ':
		freeSquares += 1
	if grid[i+1][j+1] == ' ':
		freeSquares += 1
	if grid[i-1][j-1] == ' ':
		freeSquares += 1

    return freeSquares

""" A boundry square is an unopened square with opened squares near it. """
def isBoundary(grid, i, j):
	gridsize = len(grid)
	if grid[i][j] != ' ' return False

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
def attemptToFlagMine(grid, rowno, colno):
	pass

""" Attempt to deduce a spot that should be free and click it
  	More specifically:
  	Find a square where the number of flags around it is the same as it
  	Then click every empty square around it. """
def attemptMove(grid):
	pass

def guessRandomly(grid):
	pass

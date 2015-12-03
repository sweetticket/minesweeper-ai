import Queue

""" TANK solver: slow and heavyweight backtrack solver designed to
 solve any conceivable position! """

BF_LIMIT = 8 # ???
tank_board = None
knownMine = None
knownEmpty = None
tank_solutions = [] # array of arrays of bools
#  Should be true -- if false, we're bruteforcing the endgame
borderOptimization = False


def tileSearch(currgrid, ci, cj, ti, tj):
  for i in range(len(currgrid)):
    for j in range(len(currgrid)):
      if isInstance(currgrid[i][j], int) and currgrid[i][j] > 0:
        if math.abs(ci-i) <= 1 and math.abs(cj-j) <= 1 and math.abs(ti-i) <= 1 and math.abs(tj-j) <= 1:
          return True
  return False

def tankSolver(currgrid, flags):
  borderTiles = []
  allEmptyTiles = []

  # Endgame case: if there are few enough tiles, don't bother with border tiles.
  borderOptimization = False
  for i in range(len(currgrid)):
    for j in range(len(currgrid)):
      if currgrid[i][j] == ' ':
        allEmptyTiles.append((i, j))

  # Determine all border tiles
  for i in range(len(currgrid)):
    for j in range(len(currgrid)):
      if isBoundary(currgrid, i, j) and (i, j) not in flags:
        borderTiles.append((i, j))
  
  # Count how many squares outside the knowable range
  numOutSquares = len(allEmptyTiles) - len(borderTiles)
  if numOutSquares > BF_LIMIT:
    borderOptimization = True
  else:
    borderTiles = allEmptyTiles

  # Something went wrong
  if len(borderTiles) == 0:
    return False

  # Run the segregation routine before recursing one by one
  # Don't bother if it's endgame as doing so might make it miss some cases
  segregated = [] # array of arrays
  if not borderOptimization:
    segregated.append(borderTiles)
  else:
    segregated = tankSegregate(borderTiles)

  totalMultCases = 1
  success = False
  prob_best = 0
  prob_besttile = -1
  prob_best_s = -1

  for s in range(len(segregated)):
    # Copy everything into temporary constructs
    tank_solutions = [] # array of arrays of bools
    tank_board = currgrid[:]
    knownMine = flags[:]

    knownEmpty = [[False]*len(currgrid)]*len(currgrid)
    for i in range(len(currgrid)):
      for j in range(len(currgrid)):
        if isInstance(tank_board[i][j], int) and tank_board[i][j] >= 0:
          knownEmpty[i][j] = True

    # Compute solutions -- here's the time consuming step
    tankRecurse(currgrid, segregated.get(s), 0)

    # Something screwed up
    if tank_solutions.size() == 0:
      return

    # Check for solved squares
    for i in range(len(segregated.get(s))):
      allMine = True
      allEmpty = True
      for sln in tank_solutions:
        if sln[i]:
          allEmpty = False
        else:
          allMine = False

      (qi, qj) = segregated.get(s).get(i)

      # Muahaha
      if allMine:
        respond_to_move({'cell': (qi, qj), 'flag': True, 'message': ""})
      if allEmpty:
        respond_to_move({'cell': (qi, qj), 'flag': False, 'message': ""})

    totalMultCases = totalMultCases * len(tank_solutions)

    # Calculate probabilities, in case we need it
    if not success:
      break
    
    maxEmpty = -10000
    iEmpty = -1

    for i in range(len(segregated.get(s))):
      nEmpty = 0
      for sln in tank_solutions:
        if not sln[i]:
          nEmpty += 1
        if nEmpty > maxEmpty:
          maxEmpty = nEmpty
          iEmpty = i

      probability = float(maxEmpty) / len(tank_solutions)
      if probability > prob_best:
        prob_besttile = iEmpty
        prob_best_s = s

  # But wait! If there's any hope, bruteforce harder (by a factor of 32x)!
  if BF_LIMIT == 8 and numOutSquares > 8 and numOutSquares <= 13:
    print "Extending bruteforce horizon..."
    BF_LIMIT = 13
    tankSolver(currgrid, flags)
    LF_LIMIT = 8
    return []

  if success:
    return []

  # Take a guess
  cell = segregated.get(prob_best_s).get(prob_besttile)
  return [{'cell': cell, 'flag': False, 'message': ""}]

""" Segregation routine: if two regions are independent then consider
them as separate regions. """
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
      finishedRegion.append((ci,cj))
      covered.append((ci, cj))

      # Find all connecting tiles
      for (ti, tj) in borderTiles:
        isConnected = False
        if tiles not in finishedRegion:
          break

        if math.abs(ci-ti) > 2 or math.abs(cj-tj) > 2:
          isConnected = False
        else:
          # Perform a search on all the tiles
          isConnected = tilesearch(currgrid, ci, cj, ti, tj)
        
        if isConnected:
          break

        if tile not in queue:
          queue.put(tile)
    
    allRegions.append(finishedRegion)

  return allRegions


""" Recurse from depth k (0 is root)
Assumes the tank variables are already set; puts solutions in
the static arraylist. """
def tankRecurse(currgrid, borderTiles, k):
  # Return if at this point, it's already inconsistent
  flagCount = 0
  for i in range(len(currgrid)):
    for j in range(len(currgrid)):
      # Count flags for endgame cases
      if (i, j) in knownMine:
        flagCount += 1

      num = tank_board[i][j]
      if num == ' ':
        break

      # Total bordering squares
      surround = 0
      if (i == 0 and j == 0) or (i == len(currgrid)-1 and j == len(currgrid)-1):
        surround = 3
      else if i == 0 or j == 0 or i == len(currgrid)-1 or j == len(currgrid)-1:
        surround = 5
      else:
        surround = 8

      numFlags = countFlagsAround(tank_board, knownMine, i, j)
      numFree = len(getUnopenedAround(tank_board, i, j)) # use knownEmpty instead of tank_board?

      # Scenario 1: too many mines
      if numFlags > num:
        return

      # Scenario 2: too many empty
      if surround - numFree < num:
        return

  if flagCount > TOT_MINES:
    return

  # solution found!
  if k == len(borderTiles):
    # we don't have the exact min count, so no
    if not borderOptimization and flagCount < TOT_MINES:
      return

    solution = [] # array of bools, length len(borderTiles)
    for i in range(len(borderTiles)):
      (si, sj) = borderTiles[i]
      solution[i] = knownMine[si][sj]
    tank_solutions.append(solution)
    return

  (qi, qj) = borderTiles[k]

  # Recurse two positions: mine and no mine
  knownMine[qi][qj] = True
  tankRecurse(borderTiles, k+1)
  knownMine[qi][qj] = False

  knownEmpty[qi][qj] = True
  tankRecurse(borderTiles, k+1)
  knownEmpty[qi][qj] = False
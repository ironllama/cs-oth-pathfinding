poles = [[] * 3] * 3
discs = [v for v in range(6, 0, -1)]  # Smallest at end (or top)
# print(poles, discs)

poles[0] = list(discs);  # Copy of list.
# print(poles, discs)

# End state we're looking for.
end = [[], [], [6, 5, 4, 3, 2, 1]]

stack = [] # Contains path and backtracking
discovered = []

def continueWith(newState):
    # found = False
    # for checkme in discovered:
    #     if checkme.poles == newState.poles:
    #         if newState.numMoves < checkme.numMoves:
    #             checkme.numMoves = newState.numMoves
    #             return True
    #         found = True

    # if not found:
    #     discovered.append(newState)
    #     return True

    # return False

    # Taking advantage of the __eq__ override.
    discIdx = discovered.index(newState) if newState in discovered else -1
    if discIdx != -1 and newState.numMoves <= discovered[discIdx].numMoves:
        discovered[discIdx].numMoves = newState.numMoves
        return True
    elif discIdx == -1:
        discovered.append(newState)
        return True
    else:
        return False

# Data structure to conveniently store path and num moves.
class PlayState:
    def __init__(self, poles, numMoves):
        self.poles = poles
        self.numMoves = numMoves

    def __eq__(self, other):
        return self.poles == other.poles

count = 0
stack.append(PlayState(poles, 0))  # Starting state.

lowestNumMoves = float('inf')

while (len(stack) > 0):
    # BFS!
    count += 1
    if count % 100000 == 0: print("LOOP:", count, len(stack))
    # print("LOOP:", count, len(stack))
    # curr = stack.pop()
    curr = stack.pop(0)

    if curr.poles == end and curr.numMoves < lowestNumMoves:
        # print("FINISHED:", stack.length, curr.numMoves)
        lowestNumMoves = curr.numMoves
        break

    if curr.numMoves > lowestNumMoves: continue  # Don't pursue longer paths than min found so far.

    if continueWith(curr):
        # Find "neighbors" or next game state we can go to.
        for i, sourcePole in enumerate(curr.poles):  # For each pole.
            if len(sourcePole) > 0:  # If there's something on the pole.
                topDisc = sourcePole[-1]
                # for k in range(len(curr.poles)):  // Makes use of the k awkward, later.
                for k in range(len(curr.poles) - 1, -1, -1):
                    otherPole = curr.poles[k]

                    # Try moving it to other poles.
                    # if i == k: continue  # Don't check the same pole.
                    if sourcePole == otherPole: continue  # Don't check the same pole.

                    # We're going to check for possible valid moves, without regard
                    # to strategy. If the target pole is empty or has a larger disc
                    # on top, then it is a valid move.
                    goodMove = False
                    otherTopDisc = None
                    if len(otherPole) > 0:  # Check if pole has discs already.
                        otherTopDisc = otherPole[-1]
                        if otherTopDisc > topDisc: goodMove = True  # If existing disc is larger.
                    else:
                        goodMove = True  # If not, then it's a viable move.
                    # print("COMPARE:", sourcePole, topDisc, otherPole, otherTopDisc, goodMove)

                    if goodMove:
                        # Remember to duplicate the state deeply, as it's an object composed of objects.
                        # newState = list(curr.poles)  # Shallow!
                        newState = [[inner for inner in outer] for outer in curr.poles]

                        newState[i].pop();  # Remove from source pole.
                        newState[k].append(topDisc);  # Put on target pole.
                        stack.append(PlayState(newState, curr.numMoves + 1)); # New play state to check.

print("FINISHED: LOOPS:", count, "STACK LEN:", len(stack), "ANS:", lowestNumMoves);
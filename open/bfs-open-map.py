from tkinter import *
from random import randint

playAreaBorder = 3  # Window edges.
cellBorderWidth = 1

cellSideSize = 10

delaySolveSteps = 100  # Millisecond delay per walking step.

playareaSideHeightInCells = 20  # Num of cells.
playareaSideWidthInCells = 60  # Num of cells.
playareaSideHeight = (cellSideSize * playareaSideHeightInCells) + cellBorderWidth  # The right and bottom borders of the cell need to be added.
playareaSideWidth = (cellSideSize * playareaSideWidthInCells) + cellBorderWidth

# allDirs = ((0, 1), (1, 0), (-1, 0), (0, -1))  # (X, Y)  in S, E, W, N order
# allDirs = ((0, -1), (1, 0), (0, 1), (-1, 0))  # (X, Y) in N, E, S, W order
allDirs = ((0, -1), (-1, 0), (0, 1), (1, 0))  # (X, Y) in N, W, S, E order

standardColor = "lawn green"
pathColor = "green"
nextColor = "dark green"
wallColor = "black"

startColor = "white"
finishColor = "red"

tk = Tk()
canvas = Canvas(tk, bg="white", width=playareaSideWidth, height=playareaSideHeight)
canvas.pack()

start = None
finish = None

class Cell:
    def __init__(self, x, y):
        self.pos = (x, y)
        self.visited = False
        self.wall = False  # Am I a wall square?
        self.prev = None  # For backtracking the path.

        self.square = None

    def show(self, inColor):
        fillColor = inColor
        if self.wall:
            fillColor = wallColor
        elif self == start:
            fillColor = startColor
        elif self == finish:
            fillColor = finishColor

        # canvas.create_rectangle(topLeftX, topLeftY, topLeftX + 1, topLeftY + 1, fill="red", width=0)

        # Instead of recreating a square, changing the background color of an existing square.
        if self.square is not None:
            canvas.itemconfig(self.square, fill=fillColor)
        else:
            topLeftX = (self.pos[0] * cellSideSize) + playAreaBorder
            topLeftY = (self.pos[1] * cellSideSize) + playAreaBorder
            self.square = canvas.create_rectangle(topLeftX, topLeftY, topLeftX + cellSideSize, topLeftY + cellSideSize, fill=fillColor, width=cellBorderWidth)


playareaState = []

# Draw the playarea!
def colorPlayArea(inColor):
    for row in playareaState:
        for col in row:
            col.show(inColor)

for row in range(playareaSideHeightInCells):
    newRow = []
    playareaState.append(newRow)
    for col in range(playareaSideWidthInCells):
        newRow.append(Cell(col, row))
colorPlayArea(standardColor)
# tk.mainloop()

startRanX = randint(0, playareaSideWidthInCells / 5)
startRanY = randint(0, playareaSideHeightInCells / 5)
start = playareaState[startRanY][startRanX]
start.show(startColor)
finishRanX = playareaSideWidthInCells - randint(0, playareaSideWidthInCells / 5)
finishRanY = playareaSideHeightInCells - randint(0, playareaSideHeightInCells / 5)
finish = playareaState[finishRanY][finishRanX]
finish.show(finishColor)
tk.update()

nextPaths = [start]

done = False  # To help stop early.
loopNum = 0
while len(nextPaths) > 0:
    loopNum += 1
    curr = nextPaths.pop(0)
    print("NEXT:", loopNum, len(nextPaths))

    curr.visited = True

    if done: break  # Stop other branches when one branch found the finish.

    if curr == finish:
        done = True
        print("DONE!")

        # Reset colors.
        colorPlayArea(standardColor)

        # Show new path
        curr.show(pathColor)
        while(curr.prev is not None):
            curr = curr.prev
            curr.show(pathColor)
        tk.update()

        break # End early if found early.

    # Get neighbors.
    for newDir in allDirs:
        newPos = tuple(map(sum, zip(curr.pos, newDir)))  # (a, b) + (x, y) = (a+x, b+y)
        if newPos[1] >= 0 and newPos[1] < len(playareaState) and newPos[0] >= 0 and newPos[0] < len(playareaState[0]):
            newCell = playareaState[newPos[1]][newPos[0]]
            if not newCell.wall and not newCell.visited and newCell not in nextPaths:
                # print("NEIGHBOR:", newCell, newCell.pos)
                newCell.prev = curr

                curr.show(pathColor)
                newCell.show(nextColor)
                tk.update()

                # time.sleep(delaySolveSteps / 1000)
                nextPaths.append(newCell)
                # tk.after(delaySolveSteps, goBFSSolve)

tk.mainloop()
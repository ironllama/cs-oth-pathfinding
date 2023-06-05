from tkinter import *
from dataclasses import dataclass
from random import randrange
import time

playAreaBorder = 3

cellWallSize = 3
cellSideSize = cellWallSize * 4

playareaSideSizeInCells = 20  # Num of cells.
playareaSideSize = cellSideSize * playareaSideSizeInCells

delayCreateSteps = 10  # Millisecond delay per walking step.
delaySolveSteps = 100  # Millisecond delay per walking step.
delaySolveTypesSec = 5

colorNotPath = "cornflower blue"
colorPath = "peach puff"
colorWall = "black"

colorWalkStart = "yellow"
colorWalkNext = "green"
colorWalkPath = "lime green"

    # const allDirs = ["N", "S", "W", "E"]
allDirs = ((0, -1), (0, 1), (-1, 0), (1, 0))  # (X, Y)

captionAreaHeight = 50


tk = Tk()
canvas = Canvas(tk, bg="white", width=playareaSideSize, height=playareaSideSize + captionAreaHeight)
canvas.pack()


# @dataclass  # For free __init__(). In hindsight, with only 2 viable parameters, this was kinda useless.
class Cell:
    # pos: tuple  # (x, y)
    # visited: bool = False
    # walls: str = "list(a) for a in allDirs"  # Should be a list, but given random value to satisfy dataclass linter.
    # prev: StopIteration = "Nada"  # Should be None or Cell, but given random value to satisfy dataclass linter.

    def __init__(self, x, y):
        self.pos = (x, y)
        self.visited = False
        self.walls = [list(a) for a in allDirs]
        self.prev = None

    def show(self):
        self.highlight(colorPath if self.visited else colorNotPath)

    def highlight(self, inColor):
        cornerTLX = self.pos[0] * cellSideSize + cellWallSize  # The last + cellWallSize is to offset the left and top borders from the Canvas top and left borders.
        cornerTLY = self.pos[1] * cellSideSize + cellWallSize
        canvas.create_rectangle(cornerTLX, cornerTLY, cornerTLX + cellSideSize, cornerTLY + cellSideSize, fill=inColor, width=0)
        self.drawBorders()

    # Since TKinter can not selectively remove outline or border on one side of a rectangle, we draw them manually.
    def drawBorders(self):
        # Start with the whole cell...
        topLeftX = self.pos[0] * cellSideSize + cellWallSize
        topLeftY = self.pos[1] * cellSideSize + cellWallSize
        bottomWidth = cellSideSize
        bottomHeight = cellSideSize

        # Corners!
        cornerTLX = topLeftX
        cornerTLY = topLeftY
        canvas.create_rectangle(cornerTLX, cornerTLY, cornerTLX + cellWallSize, cornerTLY + cellWallSize, fill=colorWall, width=0)  # Top Left

        cornerTLX = topLeftX + cellSideSize - cellWallSize
        canvas.create_rectangle(cornerTLX, cornerTLY, cornerTLX + cellWallSize, cornerTLY + cellWallSize, fill=colorWall, width=0)  # Top Right

        cornerTLY = topLeftY + cellSideSize - cellWallSize
        canvas.create_rectangle(cornerTLX, cornerTLY, cornerTLX + cellWallSize, cornerTLY + cellWallSize, fill=colorWall, width=0)  # Bottom Right

        cornerTLX = topLeftX
        canvas.create_rectangle(cornerTLX, cornerTLY, cornerTLX + cellWallSize, cornerTLY + cellWallSize, fill=colorWall, width=0)  # Bottom Left

        # And now the walls.
        for side in self.walls or []:
            # Start with the whole cell...
            sideTopLeftX = topLeftX
            sideTopLeftY = topLeftY
            sideBottomWidth = bottomWidth
            sideBottomHeight = bottomHeight

            # Then limit the borders.
            if side[0] == 0:
                if side[1] > 0: sideTopLeftY = sideTopLeftY + cellSideSize - cellWallSize  # South
                sideBottomHeight = cellWallSize
            else:
                if side[0] > 0: sideTopLeftX = sideTopLeftX + cellSideSize - cellWallSize  # East
                sideBottomWidth = cellWallSize

            canvas.create_rectangle(sideTopLeftX, sideTopLeftY, sideTopLeftX + sideBottomWidth, sideTopLeftY + sideBottomHeight, fill=colorWall, width=0)



# Draw the playarea!
def drawPlayArea():
    for row in playareaState:
        for col in row:
            col.show()

playareaState = []
for row in range(playareaSideSizeInCells):
    newRow = []
    playareaState.append(newRow)
    for col in range(playareaSideSizeInCells):
        newCell = Cell(col, row)
        # newCell.walls = [list(a) for a in allDirs]  # For when using dataclass.
        # newCell.prev = None
        newRow.append(newCell)
# drawPlayArea()
# tk.mainloop()

canvas.create_rectangle(playAreaBorder, playAreaBorder, playareaSideSize + playAreaBorder, playareaSideSize + playAreaBorder, fill=colorNotPath, width=playAreaBorder, outline="black")  # playareaBackground
text = canvas.create_text(playareaSideSize / 2, playareaSideSize + (captionAreaHeight / 2), text="Creating Maze w/ DFS", fill="black", font=('Helvetica 15 bold'))
# canvas.pack()


def goDFSCreate(curr):
    tk.update()
    # print("NEW CURR:", curr.pos)
    curr.visited = True

    # Get neighbors.
    newCell = None
    newDir = ""
    potentialNeighbors = [list(a) for a in allDirs]
    while not newCell and len(potentialNeighbors) > 0:  # The ! here tests both newCell? and visited. Meh.
        newDir = potentialNeighbors.pop(randrange(len(potentialNeighbors)))
        newPos = tuple(map(sum, zip(curr.pos, newDir)))  # (a, b) + (x, y) = (a+x, b+y)
        if newPos[1] >= 0 and newPos[1] < len(playareaState) and newPos[0] >= 0 and newPos[0] < len(playareaState[0]):
            newCell = playareaState[newPos[1]][newPos[0]]
            if newCell.visited: newCell = None
    # print("NEIGHBOR:", newCell, newCell.pos)

    if newCell is not None:
        curr.walls.remove(newDir)  # Break down the wall.
        curr.highlight(colorPath)  # Redraw with fixed walls.

        newCell.prev = curr
        oppositeNewDir = [v * -1 for v in newDir]  # Beware of -0, since we're doing comparisons in filter.
        newCell.walls.remove(oppositeNewDir)  # Break down the wall.
        newCell.highlight(colorWalkNext)

        time.sleep(delayCreateSteps / 1000)
        goDFSCreate(newCell)
        # tk.after(delayCreateSteps, goDFSCreate, newCell)  # Better than the sleep, but seems to run async.
    else:  # No mo' neighbors.
        if curr.pos[0] == 0 and curr.pos[1] == 0:
            print("DONE!")
            # tk.mainloop()  # this blocks and stop the program!
            tk.update()

            # drawPlayArea()
            # break  # Enable for non-recursive.
        else:
            curr.highlight(colorPath)
            curr.prev.highlight(colorWalkNext)

            time.sleep(delayCreateSteps / 1000)
            goDFSCreate(curr.prev)
            # tk.after(delayCreateSteps, goDFSCreate, curr.prev)  # Better than the sleep, but seems to run async.

goDFSCreate(playareaState[0][0])


time.sleep(delaySolveTypesSec)
print("SOLVING DFS")
canvas.itemconfig(text, text="Solving w/ DFS")

# Reset the visited var to reuse in solve.
for row in playareaState:
    for col in row:
        col.visited = False
        col.prev = None
drawPlayArea()
tk.update()

target = playareaState[len(playareaState) - 1][len(playareaState) - 1]
# print("TARGET:", target)

def goDFSSolve(curr):
    tk.update()
    curr.visited = True

    # Get neighbors.
    newCell = None
    newDir = ""
    potentialNeighbors = [a for a in allDirs if list(a) not in curr.walls]
    while not newCell and len(potentialNeighbors) > 0:  # The ! here tests both newCell? and visited. Meh.
        newDir = potentialNeighbors.pop(randrange(len(potentialNeighbors)))
        newPos = tuple(map(sum, zip(curr.pos, newDir)))  # (a, b) + (x, y) = (a+x, b+y)
        if newPos[1] >= 0 and newPos[1] < len(playareaState) and newPos[0] >= 0 and newPos[0] < len(playareaState[0]):
            newCell = playareaState[newPos[1]][newPos[0]]
            if newCell.visited: newCell = None
    # print("NEIGHBOR:", newCell, newCell.pos)

    if newCell is not None:
        newCell.prev = curr

        curr.highlight(colorWalkPath)
        newCell.highlight(colorWalkNext)

        time.sleep(delaySolveSteps / 1000)
        goDFSSolve(newCell)
        # tk.after(delaySolveSteps, goDFSSolve, newCell)
    else:  # No mo' neighbors.
        # if curr.pos[0] == 0 and curr.pos[1] == 0:
        if curr.pos == target.pos:
            print("DONE!")
            tk.update()
        else:
            curr.highlight(colorPath)
            curr.prev.highlight(colorWalkNext)

            time.sleep(delaySolveSteps / 1000)
            goDFSSolve(curr.prev)
            # tk.after(delaySolveSteps, goDFSSolve, curr.prev)

goDFSSolve(playareaState[0][0])


time.sleep(delaySolveTypesSec)
print("SOLVING DFS ALT")
canvas.itemconfig(text, text="Solving w/ DFS alternate.")

# Reset the visited var to reuse in solve.
for row in playareaState:
    for col in row:
        col.visited = False
        col.prev = None
drawPlayArea()
tk.update()

def goDFSAltSolve(curr):
    tk.update()
    curr.visited = True

    if curr.pos == target.pos:
        print("DONE!")

        # Rest colors.
        for row in playareaState:
            for col in row:
                col.visited = True
        drawPlayArea()

        # Show new path
        curr.highlight(colorWalkPath)
        while(curr.prev is not None):
            curr = curr.prev
            curr.highlight(colorWalkPath)

        tk.update()

        return True  # End early if found early.

    # Get neighbors.
    newCell = None
    newDir = ""
    potentialNeighbors = [a for a in allDirs if list(a) not in curr.walls]

    for newDir in potentialNeighbors:
    # while not newCell and len(potentialNeighbors) > 0:  # The ! here tests both newCell? and visited. Meh.
        # newDir = potentialNeighbors.pop(randrange(len(potentialNeighbors)))
        newPos = tuple(map(sum, zip(curr.pos, newDir)))  # (a, b) + (x, y) = (a+x, b+y)
        if newPos[1] >= 0 and newPos[1] < len(playareaState) and newPos[0] >= 0 and newPos[0] < len(playareaState[0]):
            newCell = playareaState[newPos[1]][newPos[0]]
            # if newCell.visited: newCell = None
            if not newCell.visited:
                # print("NEIGHBOR:", newCell, newCell.pos)
                # if newCell is not None:
                newCell.prev = curr

                curr.highlight(colorWalkPath)
                newCell.highlight(colorWalkNext)

                time.sleep(delaySolveSteps / 1000)
                done = goDFSAltSolve(newCell)
                if done: return True  # End early if found early.
        # tk.after(delaySolveSteps, goBFSSolve, newCell)
    # else:  # No mo' neighbors.
    #     # if curr.pos[0] == 0 and curr.pos[1] == 0:
    #     if curr == target:
    #         print("DONE!")
    #         tk.update()
    #     else:
    #         curr.highlight(colorPath)
    #         curr.prev.highlight(colorWalkNext)

    #         time.sleep(delaySolveSteps / 1000)
    #         goBFSSolve(curr.prev)
    #         # tk.after(delaySolveSteps, goBFSSolve, curr.prev)

goDFSAltSolve(playareaState[0][0])


time.sleep(delaySolveTypesSec)
print("SOLVING BFS")
canvas.itemconfig(text, text="Solving w/ BFS")

# Reset the visited var to reuse in solve.
for row in playareaState:
    for col in row:
        col.visited = False
        col.prev = None
drawPlayArea()
tk.update()

done = False  # To help stop early.

def goBFSSolve(curr):
    global done

    tk.update()
    curr.visited = True

    if done: return

    if curr.pos == target.pos:
        done = True
        print("DONE!")

        # Rest colors.
        for row in playareaState:
            for col in row:
                col.visited = True
        drawPlayArea()

        # Show new path
        curr.highlight(colorWalkPath)
        while(curr.prev is not None):
            curr = curr.prev
            curr.highlight(colorWalkPath)

        tk.update()

        return # End early if found early.

    # Get neighbors.
    newCell = None
    newDir = ""
    potentialNeighbors = [a for a in allDirs if list(a) not in curr.walls]

    for newDir in potentialNeighbors:
        newPos = tuple(map(sum, zip(curr.pos, newDir)))  # (a, b) + (x, y) = (a+x, b+y)
        if newPos[1] >= 0 and newPos[1] < len(playareaState) and newPos[0] >= 0 and newPos[0] < len(playareaState[0]):
            newCell = playareaState[newPos[1]][newPos[0]]
            if not newCell.visited:
                # print("NEIGHBOR:", newCell, newCell.pos)
                newCell.prev = curr

                curr.highlight(colorWalkPath)
                newCell.highlight(colorWalkNext)

                # time.sleep(delaySolveSteps / 1000)
                # done = goBFSSolve(newCell)
                tk.after(delaySolveSteps, goBFSSolve, newCell)
                # if done: return True  # End early if found early.

goBFSSolve(playareaState[0][0])

tk.mainloop()
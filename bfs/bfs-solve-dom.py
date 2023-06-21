print("What is going on?")

from pyscript import Element

biggrid = Element('biggrid')
# print("BIGGRID:", biggrid.select("div"))

animDelay = 0
# sideSize = biggrid.children.length
sideSize = 20

puzzleColor = "lime"
pathColor = "darkgreen"

allDirs = ["S", "E", "W", "N"]
# # gallDirs = ["N", "E", "S", "W"];

start = biggrid.select("div[data-x='0'][data-y='0']")
end = biggrid.select(f"div[data-x='{sideSize - 1}'][data-y='{sideSize - 1}']")
start.add_class("bg-pink")
end.add_class("bg-yellow")

print(start.innerHtml)

# 2023-05-06: DEADEND.
# This isn't going to go anywhere. PyScript has, so far, no way of getting CSS styles or classes currently applied.



# visited = [start]
# allDone = False
# def goBFS(curr):
#     if (allDone): return  # Early quit branches if the maze is solved.

#     visited.append(curr)  # Add to list of visited.
#     curr.add_class(pathColor)  # Show where we are.

#     if curr == end:
#         print("FINISHED!")
#         allDone = true
#         return

#     # Get neighbors and go to wherever is open.
#     # allDirs.forEach((dir) => {
#     foundNeighbor = False
#     fromCell = None
#     # console.log("CHECKING:", curr);
#     for dir in allDirs:
#         newY = curr.y
#         newX = curr.x

#         match dir:
#             case "S":
#                 if (curr.style.borderBottom === "none") newY += 1;
#             case "E":
#                 if (curr.style.borderRight === "none") newX += 1;
#             case "W":
#                 if (curr.style.borderLeft === "none") newX -= 1;
#             case _:
#                 if (curr.style.borderTop === "none") newY -= 1;
#         }

# #         # console.log("Trying to go:", curr.dataset.x, newX, curr.dataset.y, newY);
# #         # If there is a possibility to move, then go.
# #         if (newX != curr.dataset.x || newY != curr.dataset.y) {
# #             const neighbor = biggrid.children[newY].children[newX];
# #             # console.log("NEIGH:", newY, newX, neighbor);
# #             if (!visited.includes(neighbor)) {
# #                 foundNeighbor = true;
# #                 setTimeout(() => goBFS(neighbor), animDelay);
# #                 # break;  # If commented out, all branches are explored and added to JS's event queue. Ghetto BFS!
# #             } else if (neighbor.style.backgroundColor === pathColor) {
# #                 from = neighbor;
# #             }
# #         }
# #     }

# goBFS(start)

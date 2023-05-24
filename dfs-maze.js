const cellSideSize = 8;
const playareaSideSizeInCells = 5;  // Num of cells.
const playareaSideSize = cellSideSize * playareaSideSizeInCells;

const cellWallSize = 2;

const delayNewPath = 0;  // Millisecond delay per walking step.
const delayPathSteps = 0;  // Millisecond delay per walking step.


// const allDirs = ["N", "S", "W", "E"];
// const allDirs = [[-1, 0], [1, 0], [0, -1], [0, 1]];  // [X, Y]
const allDirs = [[0, -1], [0, 1], [-1, 0], [1, 0]];  // [X, Y]


class Cell {
    constructor(col, row) {
        this.x = col;
        this.y = row;
        this.visited = false;
        this.walls = [...allDirs];  // Make sure this is a copy! Removed: makes for crappy "rooms".
        this.prev = null;  // To path back to walking start.
    }
}

const playareaState = []
for (let row = 0; row < playareaSideSizeInCells; row++) {
    const newRow = [];
    playareaState.push(newRow);
    for (let col = 0; col < playareaSideSizeInCells; col++) {
        const newCell = new Cell(col, row);
        newRow.push(newCell);
    }
}

// Seed the initial 'inPath' cell.
curr = playareaState[0][0];

// for (; ;) {  // For the non-recursive version. Can't really do timelapse with it.
function nextPath() {  // Recursive version for timelapse.
    // console.log("NEW CURR:", curr);
    curr.visited = true;

    // Get neighbors.
    let newCell = null;
    let newDir = "";
    const potentialNeighbors = [...allDirs];
    while (!newCell && potentialNeighbors.length > 0) {  // The ! here tests both newCell? and visited. Meh.
        newDir = potentialNeighbors.splice((Math.random() * potentialNeighbors.length) | 0, 1)[0];
        const newX = curr.x + newDir[0];
        const newY = curr.y + newDir[1];
        if (newY >= 0 && newY < playareaState.length && newX >= 0 && newX < playareaState[0].length) {
            newCell = playareaState[newY][newX];
            if (newCell.visited) newCell = null;
        }
    }
    // console.log("NEIGHBOR:", newCell);

    if (newCell) {
        curr.walls = curr.walls.filter(d => d.toString() !== newDir.toString());  // Break down the wall.

        newCell.prev = curr;
        const oppositeNewDir = newDir.map(v => v ? v * -1 : v);  // Beware of -0, since we're doing comparisons in filter.
        newCell.walls = newCell.walls.filter(d => d.toString() !== oppositeNewDir.toString());  // Break down the wall.

        curr = newCell;
        setTimeout(() => nextPath(), delayPathSteps);  // Comment out for non-recursive.
    }
    else {  // No mo' neighbors.
        if (curr.x === 0 && curr.y === 0) {
            console.log("DONE!");
            generateTextMap();
            // drawPlayArea();
            // break;  // Enable for non-recursive.
        }
        else {
            curr = curr.prev;  // Back it up.
            setTimeout(() => nextPath(), delayNewPath);  // Comment out for non-recursive.
        }
    }
}
nextPath();


function generateTextMap() {
    const textMap = new Array((playareaSideSizeInCells * 2) + 1).fill().map(r => new Array((playareaSideSizeInCells * 2) + 1).fill(" "));  // Should pre-create so that you can set south horizontal walls.
    textMap[0].fill('#');

    playareaState.forEach((row, i) => {
        const textRow = (i * 2) + 1;

        row.forEach((col, k) => {
            if (k === 0 || k === playareaSideSizeInCells - 1) textMap[textRow][k] = '#';
            const textCol = (k * 2) + 1;

            col.walls.forEach(wall => {
                textMap[textRow + wall[1]][textCol + wall[0]] = '#';
            });
        });

        // console.log("SO FAR:", textMap[i].join(""));
        // console.log("SO FAR:", textMap[textRow].join(""));
    });

    textMap[textMap.length - 1].fill('#');

    textMap.forEach(row => console.log(row.join("")));
}
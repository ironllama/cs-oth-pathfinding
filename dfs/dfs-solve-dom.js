const biggrid = document.getElementById("biggrid");

const animDelay = 0;
const sideSize = biggrid.children.length;

const puzzleColor = "lime";
const pathColor = "darkgreen";

const allDirs = ["S", "E", "W", "N"];
// const allDirs = ["N", "E", "S", "W"];

const start = biggrid.children[0].children[0];
const end = biggrid.children[sideSize - 1].children[sideSize - 1];
start.style.backgroundColor = "pink";
end.style.backgroundColor = "yellow";

const visited = [start];
function goDFS(curr) {
    visited.push(curr); // Add to list of visited.
    curr.style.backgroundColor = pathColor; // Show where we are.

    if (curr === end) {
        console.log("FINISHED!");
        return;
    }

    // Get neighbors and go to wherever is open.
    // allDirs.forEach((dir) => {
    let foundNeighbor = false;
    let from = null;
    // console.log("CHECKING:", curr);
    for (let dir of allDirs) {
        let newY = parseInt(curr.dataset.y, 10);
        let newX = parseInt(curr.dataset.x, 10);

        switch (dir) {
            case "S":
                if (curr.style.borderBottom === "none") newY += 1;
                break;
            case "E":
                if (curr.style.borderRight === "none") newX += 1;
                break;
            case "W":
                if (curr.style.borderLeft === "none") newX -= 1;
                break;
            default:
                if (curr.style.borderTop === "none") newY -= 1;
                break;
        }

        // console.log("Trying to go:", curr.dataset.x, newX, curr.dataset.y, newY);
        // If there is a possibility to move, then go.
        if (newX != curr.dataset.x || newY != curr.dataset.y) {
            const neighbor = biggrid.children[newY].children[newX];
            // console.log("NEIGH:", newY, newX, neighbor);
            if (!visited.includes(neighbor)) {
                foundNeighbor = true;
                setTimeout(() => goDFS(neighbor), animDelay);
                break;
            } else if (neighbor.style.backgroundColor === pathColor) {
                from = neighbor;
            }
        }
    }

    if (!foundNeighbor && from) {
        // Probably a dead-end!
        // console.log("DEADEND!");
        curr.style.backgroundColor = puzzleColor;
        curr = from;
        setTimeout(() => goDFS(from), animDelay);
    }
    // });
}
goDFS(start);

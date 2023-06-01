const poles = new Array(3).fill().map(() => []);
const discs = new Array(6).fill().map((v, i) => i + 1);
// console.log(poles, discs);

poles[0] = [...discs].reverse(); // Smallest at end (or top)
// console.log(poles, discs);

// End state we're looking for. Pre-stringified to make
// the comparison faster later in the algo.
const end = [[], [], [6, 5, 4, 3, 2, 1]];
const endStr = JSON.stringify(end);

const stack = []; // Contains path and backtracking
const discovered = [];

function matrixIsEqual(a, b) {
    for (const [i, v1] of a.entries()) {
        for (const [k, v2] of v1.entries()) {
            if (v2 !== b[i][k]) return false;
        }
    }
    return true;
}
function continueWith(newState) {
    const discIdx = inDiscovered(newState);
    if (discIdx !== -1 && newState.numMoves <= discovered[discIdx].numMoves) {
        // discovered.splice(discIdx, 1);
        // discovered.push(newState);
        discovered[discIdx].numMoves = newState.numMoves;  // ~10% time improvement over splice/push.
        return true;
    }
    else if (discIdx === -1) {
        discovered.push(newState);
        return true;
    }
    else return false;
}

function inDiscovered(newState) {
    // return discovered.findIndex(v => JSON.stringify(v.poles) === JSON.stringify(newState.poles));
    return discovered.findIndex(v => matrixIsEqual(v.poles, newState.poles));
}

// Data structure to conveniently store path and num moves.
class PlayState {
    constructor(poles, numMoves) {
        this.poles = poles;
        this.numMoves = numMoves;
    }
}

let count = 0;
stack.push(new PlayState(poles, 0)); // Starting state.

let lowestNumMoves = Infinity;

while (stack.length > 0) {
    // BFS!
    if (++count % 100000 === 0) console.log("LOOP:", count, stack.length);
    // const curr = stack.pop();
    const curr = stack.shift();

    if (
        // JSON.stringify(curr.poles) === endStr &&
        matrixIsEqual(curr.poles, end) &&
        curr.numMoves < lowestNumMoves
    ) {
        // console.log("FINISHED:", stack.length, curr.numMoves);
        lowestNumMoves = curr.numMoves;
        break;
    }

    // if (discovered.includes(curr)) {  // Doesn't work because of array compare [] !== []
    // if (!inDiscovered(curr)) {
    //     discovered.push(curr);
    if (continueWith(curr)) {
        // Find "neighbors" or next game state we can go to.
        for (let [i, sourcePole] of curr.poles.entries()) {
            // For each pole.
            if (sourcePole.length > 0) {
                // If there's something on the pole.
                const topDisc = sourcePole.at(-1);
                for (let [k, otherPole] of curr.poles.entries()) {
                    // Try moving it to other poles.
                    if (i === k) continue; // Don't check the same pole.

                    // We're going to check for possible valid moves, without regard
                    // to strategy. If the target pole is empty or has a larger disc
                    // on top, then it is a valid move.
                    let goodMove = false;
                    if (otherPole.length > 0) {
                        // Check if pole has discs already.
                        const otherTopDisc = otherPole.at(-1);
                        if (otherTopDisc > topDisc) goodMove = true; // If existing disc is larger.
                    } else goodMove = true; // If not, then it's a viable move.

                    if (goodMove) {
                        // Remember to duplicate the state deeply, as it's an object composed of objects.
                        const newState = JSON.parse(JSON.stringify(curr.poles));

                        newState[i].pop(); // Remove from source pole.
                        newState[k].push(topDisc); // Put on target pole.
                        stack.push(new PlayState(newState, curr.numMoves + 1)); // New play state to check.
                    }
                }
            }
        }
    }
}
console.log("FINISHED:", stack.length, lowestNumMoves);


// Previous version, with random poles
//
// const jsonFile = 'dfs-hanoi.json';

// const discs = new Array(6).fill().map((v, i) => i + 1);
// let poles = new Array(3).fill().map(() => []);

// function createNewTowers() {
//     const disc_queue = [...discs];
//     while (disc_queue.length > 0) {
//         const randPoleIdx = Math.floor(Math.random() * poles.length);

//         const randDiscIdx = Math.floor(Math.random() * disc_queue.length);
//         const randDisc = disc_queue.splice(randDiscIdx, 1);

//         poles[randPoleIdx].push(randDisc);
//     }
//     require('fs').writeFileSync(jsonFile, JSON.stringify(poles));
// }
// // createNewTowers();

// function showTowers() {
//     poles.forEach((pole, i) => console.log(i + ":", pole.join(", ")));
// }

// function readTowers() {
//     poles = JSON.parse(require('fs').readFileSync(jsonFile, { encoding: 'utf-8', }));
// }
// readTowers();
// showTowers();

// class TowerState {
//     constructor(poles) {
//         this.poles = poles;
//         this.numMoves = 0;
//     }
// }

// const discoveredStates = [];
// function isDiscovered(inState) {
//     let foundSame = false;
//     outerLoop:
//     for (let v of discoveredStates) {
//         for (const [i, vp] of v.poles.entries()) {
//             for (const [k, vd] of vp.entries()) {
//                 console.log(vd, inState.poles[i][k], i, k);
//                 if (vd !== inState.poles[i][k]) continue outerLoop;
//             }
//         }
//         return true;
//     };
//     return false;
// }
// Tests.
// discoveredStates.push(new TowerState([[2, 3], [1], [6, 4, 5]]));
// discoveredStates.push(new TowerState([[1, 3], [6], [2, 4, 5]]));
// discoveredStates.push(new TowerState([[5], [6, 1, 3], [2, 4]]));
// console.log(isDiscovered(new TowerState([[2, 3], [1], [6, 4, 5]])));
// console.log(isDiscovered(new TowerState([[5], [6, 1, 3], [2, 4]])));

// function dfs_interative(firstState) {
//     const pathStack = [];
//     pathStack.push(firstState);  // Starting state.

//     while (pathStack.length > 0) {
//         const currState = pathStack.pop();

//         if (isDiscovered(currState)) {
//             discoveredStates.push(currState);

//             // All possible moves, using top blocks and only on top of larger blocks.
//             currState.poles.forEach((pole, i) => {
//                 if (pole.length > 0) {
//                     const topDisc = pole[i].at(-1);

//                     newPoles.forEach((newPole, k) => {
//                         if (i === k) return;  // Skip checking same pole.
//                         if (topDisc < newPole.at(-1)) {  // Valid move!
//                             const newPoles = JSON.parse(JSON.stringify(pole));
//                             newPoles[i].pop();
//                             newPole.push(topDisc);

//                         }
//                     });
//                     pathStack.push()
//                 }
//             });
//         }
//     }

// }
// dfs_interative(new TowerState(poles));
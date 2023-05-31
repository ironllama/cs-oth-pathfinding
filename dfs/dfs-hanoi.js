const jsonFile = 'dfs-hanoi.json';

const discs = new Array(6).fill().map((v, i) => i + 1);
let poles = new Array(3).fill().map(() => []);

function createNewTowers() {
    const disc_queue = [...discs];
    while (disc_queue.length > 0) {
        const randPoleIdx = Math.floor(Math.random() * poles.length);

        const randDiscIdx = Math.floor(Math.random() * disc_queue.length);
        const randDisc = disc_queue.splice(randDiscIdx, 1);

        poles[randPoleIdx].push(randDisc);
    }
    require('fs').writeFileSync(jsonFile, JSON.stringify(poles));
}
// createNewTowers();

function showTowers() {
    poles.forEach((pole, i) => console.log(i + ":", pole.join(", ")));
}

function readTowers() {
    poles = JSON.parse(require('fs').readFileSync(jsonFile, { encoding: 'utf-8', }));
}
readTowers();
showTowers();

class TowerState {
    constructor(poles) {
        this.poles = poles;
        this.numMoves = 0;
    }
}

const discoveredStates = [];
function isDiscovered(inState) {
    let foundSame = false;
    outerLoop:
    for (let v of discoveredStates) {
        for (const [i, vp] of v.poles.entries()) {
            for (const [k, vd] of vp.entries()) {
                console.log(vd, inState.poles[i][k], i, k);
                if (vd !== inState.poles[i][k]) continue outerLoop;
            }
        }
        return true;
    };
    return false;
}
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
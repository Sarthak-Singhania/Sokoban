import sys
import solver
from Level import Level


def movePlayer(direction, myLevel):

    matrix = myLevel.getMatrix()

    myLevel.addToHistory(matrix)

    matrix.successor(direction, True)

    if matrix.isSuccess():
        global current_level
        current_level += 1
        initLevel(level_set, current_level)


def initLevel(level_set, level):
    global myLevel
    myLevel = Level(level_set, level)


def runGame():
    global current_level
    current_level = 1
    global level_set
    level_set = "own"
    # level_set = "sir"
    initLevel(level_set, current_level)
    count = 0

    old_level = current_level - 1
    while old_level is current_level - 1:
        old_level = current_level
        moves = solve(myLevel)
        if moves != "":
            for move in moves:
                movePlayer(move, myLevel)
        else:
            print("Failed for level %d" % (current_level))

            current_level = current_level + 1
            if current_level > 20:
                print("No more levels")
                sys.exit(0)
            initLevel(level_set, current_level)


def solve(myLevel):
    moves_cache = []
    solution = solver.solver()
    solution.refresh()
    moves_cache = solution.astar(
        myLevel.getMatrix())
    print("Level: %d, Moves: %s States Explored: %d" %
          (current_level, moves_cache[0], moves_cache[1]))
    return moves_cache[0]


if __name__ == '__main__':
    runGame()

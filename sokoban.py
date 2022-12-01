import collections
import sys
import heapq
from Level import Level
from levels.level_parser import convert


def distance(method):
    def calc(state, cache):
        if 'min_distance' not in cache:
            cache['min_distance'] = {}
        player = state.getPlayerPosition()
        boxes = state.getBoxes()
        targets = state.getTargets()
        total = 0
        key = (",".join([str(x[0]) + "-" + str(x[1]) for x in boxes]),
                ",".join([str(x[0]) + "-" + str(x[1]) for x in targets]))
        if key in cache['min_distance']:
            total = cache['min_distance'][key]
        else:
            for b in boxes:
                total += min([method(b, t) for t in targets] or [0])
            cache['min_distance'][key] = total
        total += sum([method(player, b) for b in boxes] or [0])
        return total

    return calc


class solver():
    cache = {}
    global distance
    heuristic = distance(lambda a, b: abs(a[0] - b[0]) + abs(a[1] - b[1]))

    def refresh(self):
        self.cache = {}

    def astar(self, startState, maxCost=1000, cache={}):
        h = solver.heuristic
        queue = PriorityQueue()
        action_map = {}
        startState.h = h(startState, self.cache)
        queue.update(startState, startState.h)
        action_map[startState.toString()] = ""
        while not queue.empty():
            state, cost = queue.removeMin()
            actions = action_map[state.toString()]
            cache[state.toString()] = len(actions)
            if state.isSuccess():
                return (actions, len(cache))
            for (action, cost_delta) in state.getPossibleActions():
                successor = state.successor(action)
                if successor.toString() in cache:
                    continue
                action = action.lower() if cost_delta == 'Move' else action.upper()
                old = action_map[successor.toString()] if successor.toString() in action_map else None
                if not old or len(old) > len(actions) + 1:
                    action_map[successor.toString()] = actions + action
                successor.h = h(successor, self.cache)
                queue.update(successor, cost + 1 + successor.h - state.h)
        return ("", 0)


    def cost(self, actions):
        return len([x for x in actions if x.islower()])
    
    def uniformCostSearch(self, state):
        beginBox = state
        beginPlayer = state.getPlayerPosition()

        startState = (beginPlayer, beginBox)
        frontier = PriorityQueue()
        frontier.push([startState], 0)
        exploredSet = set()
        actions = PriorityQueue()
        actions.push([0], 0)
        count = 0
        while frontier:
            node = frontier.pop()
            node_action = actions.pop()
            if node[-1][-1].isSuccess():
                solution = ','.join(node_action[1:]).replace(',','')
                print(count)
                return solution
                # break
            if node[-1] not in exploredSet:
                exploredSet.add(node[-1])
                Cost = cost(node_action[1:])
                for action in node[-1][0].getPossibleActions():
                    count = count + 1
                    newPosPlayer, newPosBox = frontier.update(node[-1][0], node[-1][1], action)
                    if newPosBox.isFailure():
                        continue
                    frontier.push(node + [(newPosPlayer, newPosBox)], Cost)
                    actions.push(node_action + [action[-1]], Cost)

    def depthFirstSearch(self, state):
        """Implement depthFirstSearch approach"""
        beginBox = state
        beginPlayer = state.getPlayerPosition()

        startState = (beginPlayer, beginBox)
        frontier = collections.deque([[startState]])
        exploredSet = set()
        actions = [[0]]
        count = 0
        while frontier:
            node = frontier.pop()
            node_action = actions.pop()
            if node[-1][-1].isSuccess():
                solution = ','.join(node_action[1:]).replace(',','')
                print(count)
                return solution
                # break
            if node[-1] not in exploredSet:
                exploredSet.add(node[-1])
                for action in node[-1][0].getPossibleActions():
                    count = count + 1
                    newPosPlayer, newPosBox = frontier.update(node[-1][0], node[-1][1], action)
                    if newPosBox.isFailure():
                        continue
                    frontier.append(node + [(newPosPlayer, newPosBox)])
                    actions.append(node_action + [action[-1]])

    def isFailed(state):
        rotatePattern = [[0,1,2,3,4,5,6,7,8],
                        [2,5,8,1,4,7,0,3,6],
                        [0,1,2,3,4,5,6,7,8][::-1],
                        [2,5,8,1,4,7,0,3,6][::-1]]
        flipPattern = [[2,1,0,5,4,3,8,7,6],
                        [0,3,6,1,4,7,2,5,8],
                        [2,1,0,5,4,3,8,7,6][::-1],
                        [0,3,6,1,4,7,2,5,8][::-1]]
        allPattern = rotatePattern + flipPattern

        for box in state.getBoxes():
            if box not in state.getTargets():
                board = [(box[0] - 1, box[1] - 1), (box[0] - 1, box[1]), (box[0] - 1, box[1] + 1),
                        (box[0], box[1] - 1), (box[0], box[1]), (box[0], box[1] + 1),
                        (box[0] + 1, box[1] - 1), (box[0] + 1, box[1]), (box[0] + 1, box[1] + 1)]
                for pattern in allPattern:
                    newBoard = [board[i] for i in pattern]
                    if newBoard[1] in state.getBoxes() and newBoard[5] in state: return True
                    elif newBoard[1] in state.getBoxes() and newBoard[2] in state and newBoard[5] in state: return True
                    elif newBoard[1] in state.getBoxes() and newBoard[2] in state and newBoard[5] in state.getBoxes(): return True
                    elif newBoard[1] in state.getBoxes() and newBoard[2] in state.getBoxes() and newBoard[5] in state.getBoxes(): return True
                    elif newBoard[1] in state.getBoxes() and newBoard[6] in state.getBoxes() and newBoard[2] in state and newBoard[3] in state and newBoard[8] in state: return True
        return False

class PriorityQueue:
    def __init__(self):
        self.DONE = -100000
        self.heap = []
        self.priorities = {}

    def update(self, state, newPriority):
        oldPriority = self.priorities.get(state)
        if oldPriority == None or newPriority < oldPriority:
            self.priorities[state] = newPriority
            heapq.heappush(self.heap, (newPriority, state))
            return True
        return False

    def removeMin(self):
        while len(self.heap) > 0:
            priority, state = heapq.heappop(self.heap)
            if self.priorities[state] == self.DONE:
                continue
            self.priorities[state] = self.DONE
            return (state, priority)
        return (None, None)

    def empty(self):
        return len(self.heap) == 0


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


def output(moves):
    f = open('moves.txt', 'a+')
    f.read()
    f.write(moves+'\n')
    f.close()


def runGame():
    global current_level
    current_level = 1
    global level_set
    level_set = "own"
    # level_set = "sir"
    initLevel(level_set, current_level)
    count = 0
    old_level = current_level - 1
    open('moves.txt', 'w').close()
    while old_level is current_level - 1:
        old_level = current_level
        moves = solve(myLevel)
        if moves != "":
            for move in moves:
                movePlayer(move, myLevel)
            output(moves)
        else:
            print("Failed for level %d" % (current_level))

        current_level = current_level + 1
        if current_level > 20:
            print("No more levels")
            sys.exit(0)
        initLevel(level_set, current_level)


def solve(myLevel):
    moves_cache = []
    solution = solver()
    solution.refresh()
    moves_cache = solution.astar(
        myLevel.getMatrix())
    print("Level: %d, Moves: %s States Explored: %d" %
          (current_level, moves_cache[0], moves_cache[1]))
    return moves_cache[0]


if __name__ == '__main__':
    convert(input('Enter path to xsb file: '),input('Enter level directory name: '))
    runGame()

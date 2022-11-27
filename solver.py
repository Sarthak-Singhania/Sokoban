import heapq


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
    # costs = default
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
            if state.isFailure():
                continue
            if cost >= maxCost:
                continue

            if len(action_map) % 10000 == 0:
                print(len(action_map))
            for (action, cost_delta) in state.getPossibleActions():
                successor = state.successor(action)
                if successor.toString() in cache:
                    continue
                old = action_map[successor.toString(
                )] if successor.toString() in action_map else None
                if not old or len(old) > len(actions) + 1:
                    action_map[successor.toString()] = actions + action
                successor.h = h(successor, self.cache)
                queue.update(successor, cost + 1 + successor.h - state.h)
        return ("", 0)


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

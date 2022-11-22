import os
import psutil
import time
from state import State
from move import Up, Down, Left, Right

def counted(f):
    def wrapped(*args, **kwargs):
        wrapped.calls += 1
        return f(*args, **kwargs)
    wrapped.calls = 0
    return wrapped

class MyPuzzle:
    def __init__(self):
        self.walls = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1], [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1], [1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1], [1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1], [1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1], [1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1], [1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1], [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1], [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
        self.player = (8, 11)
        # self.boxes = [(2, 3), (2, 6), (2, 12), (2, 15), (3, 1), (3, 7), (3, 10), (4, 3), (4, 14), (6, 3), (6, 6), (7, 11), (7, 16), (8, 11), (8, 16), (9, 3), (9, 6), (11, 3), (11, 14), (12, 1), (12, 7), (12, 10), (13, 3), (13, 6), (13, 12), (13, 15)]
        # self.goals = [(1, 3), (1, 7), (2, 1), (3, 12), (3, 15), (3, 17), (4, 1), (4, 6), (5, 12), (5, 15), (5, 17), (7, 6), (7, 14), (8, 6), (8, 14), (10, 12), (10, 15), (10, 17), (11, 1), (11, 6), (12, 12), (12, 15), (12, 17), (13, 1), (14, 3), (14, 7)]
        self.boxes = [(3, 4), (3, 7), (3, 13), (3, 16), (4, 2), (4, 8), (4, 11), (5, 4), (5, 15), (7, 4), (7, 7), (8, 12), (8, 17), (9, 12), (9, 17), (10, 4), (10, 7), (12, 4), (12, 15), (13, 2), (13, 8), (13, 11), (14, 4), (14, 7), (14, 13), (14, 16)]
        self.goals = [(2, 4), (2, 8), (3, 2), (4, 13), (4, 16), (4, 18), (5, 2), (5, 7), (6, 13), (6, 16), (6, 18), (8, 7), (8, 15), (9, 7), (9, 15), (11, 13), (11, 16), (11, 18), (12, 2), (12, 7), (13, 13), (13, 16), (13, 18), (14, 2), (15, 4), (15, 8)]

@counted
def search(path, g, bound, puzzle):
    node = path[-1]
    f = g + node.distance(puzzle.goals)
    if f > bound:
        return False, f
    if node.success(puzzle.goals):
        for state_index in range(1, len(path)):
            if path[state_index-1].player[0] < path[state_index].player[0]:
                print("Down", end=" ")
            elif path[state_index-1].player[0] > path[state_index].player[0]:
                print("Up", end=" ")
            elif path[state_index-1].player[1] < path[state_index].player[1]:
                print("Right", end=" ")
            else:
                print("Left", end=" ")
        return True, bound
    minimum = None
    moves = [Up, Down, Right, Left]
    for cm in moves:
        m = cm(puzzle.walls)
        new_state = m.get_state(node)
        if new_state is None:
            continue
        if new_state not in path:
            path.append(new_state)
            found, value = search(path, g+1, bound, puzzle)
            if found:
                return found, bound
            if value is not None and (minimum is None or value < minimum):
                minimum = value
            path.pop(-1)
    return False, minimum


def main():
    puzzle = MyPuzzle()
    state = State(puzzle.player, puzzle.boxes)
    bound = state.distance(puzzle.goals)*2  # since in general we have to move and go back
    path = [state]
    while True:
        found, value = search(path, 0, bound, puzzle)
        if found:
            print()
            print("search calls:", search.calls)
            process = psutil.Process(os.getpid())
            print(process.memory_info().rss / (1024 * 1024))  # in megabytes
            return path, bound
        if value is None:
            return "not found"
        bound = value


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
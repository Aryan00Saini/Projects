from pyamaze import maze, agent, COLOR, textLabel
import time
import tkinter as tk
import heapq


def BFS(m):
    start = (m.rows, m.cols)
    frontier = [start]
    explored = [start]
    bfsPath = {}

    while frontier:
        currCell = frontier.pop(0)
        if currCell == (1, 1): break

        for d in 'ESNW':
            if m.maze_map[currCell][d]:
                if d == 'E': childCell = (currCell[0], currCell[1] + 1)
                elif d == 'W': childCell = (currCell[0], currCell[1] - 1)
                elif d == 'N': childCell = (currCell[0] - 1, currCell[1])
                elif d == 'S': childCell = (currCell[0] + 1, currCell[1])
                if childCell not in explored:
                    frontier.append(childCell)
                    explored.append(childCell)
                    bfsPath[childCell] = currCell

    return constructPath(bfsPath, start)


def DFS(m):
    start = (m.rows, m.cols)
    frontier = [start]
    explored = [start]
    dfsPath = {}

    while frontier:
        currCell = frontier.pop()
        if currCell == (1, 1): break

        for d in 'ESNW':
            if m.maze_map[currCell][d]:
                if d == 'E': childCell = (currCell[0], currCell[1] + 1)
                elif d == 'W': childCell = (currCell[0], currCell[1] - 1)
                elif d == 'N': childCell = (currCell[0] - 1, currCell[1])
                elif d == 'S': childCell = (currCell[0] + 1, currCell[1])
                if childCell not in explored:
                    frontier.append(childCell)
                    explored.append(childCell)
                    dfsPath[childCell] = currCell

    return constructPath(dfsPath, start)


def Dijkstra(m):
    start = (m.rows, m.cols)
    goal = (1, 1)
    frontier = []
    heapq.heappush(frontier, (0, start))
    costSoFar = {start: 0}
    dijkstraPath = {}

    while frontier:
        currCost, currCell = heapq.heappop(frontier)
        if currCell == goal: break

        for d in 'ESNW':
            if m.maze_map[currCell][d]:
                if d == 'E': childCell = (currCell[0], currCell[1] + 1)
                elif d == 'W': childCell = (currCell[0], currCell[1] - 1)
                elif d == 'N': childCell = (currCell[0] - 1, currCell[1])
                elif d == 'S': childCell = (currCell[0] + 1, currCell[1])
                newCost = currCost + 1
                if childCell not in costSoFar or newCost < costSoFar[childCell]:
                    costSoFar[childCell] = newCost
                    heapq.heappush(frontier, (newCost, childCell))
                    dijkstraPath[childCell] = currCell

    return constructPath(dijkstraPath, start)


def AStar(m):
    start = (m.rows, m.cols)
    goal = (1, 1)
    def heuristic(a, b): return abs(a[0]-b[0]) + abs(a[1]-b[1])
    frontier = []
    heapq.heappush(frontier, (0 + heuristic(start, goal), 0, start))
    cameFrom = {}
    costSoFar = {start: 0}

    while frontier:
        _, currCost, currCell = heapq.heappop(frontier)
        if currCell == goal: break

        for d in 'ESNW':
            if m.maze_map[currCell][d]:
                if d == 'E': childCell = (currCell[0], currCell[1] + 1)
                elif d == 'W': childCell = (currCell[0], currCell[1] - 1)
                elif d == 'N': childCell = (currCell[0] - 1, currCell[1])
                elif d == 'S': childCell = (currCell[0] + 1, currCell[1])
                newCost = currCost + 1
                if childCell not in costSoFar or newCost < costSoFar[childCell]:
                    costSoFar[childCell] = newCost
                    priority = newCost + heuristic(childCell, goal)
                    heapq.heappush(frontier, (priority, newCost, childCell))
                    cameFrom[childCell] = currCell

    return constructPath(cameFrom, start)


def constructPath(cameFrom, start):
    cell = (1, 1)
    path = {}
    while cell != start:
        path[cameFrom[cell]] = cell
        cell = cameFrom[cell]
    return path


def getScreenSizeMaze():
    root = tk.Tk()
    width, height = root.winfo_screenwidth(), root.winfo_screenheight()
    root.destroy()
    cell_size = 25
    return (height - 100) // cell_size, (width - 100) // cell_size


def animatePath(m, path, a, delay=0.01):
    for k, v in path.items():
        m.tracePath({a: {k: v}}, delay=delay)


if __name__ == '__main__':
    rows, cols = getScreenSizeMaze()
    print(f"Screen Maze Size: {rows}x{cols}")

    m = maze(rows, cols)
    m.CreateMaze(loopPercent=30)

    # Run all algorithms
    timers = {}
    paths = {}

    print("Solving maze with all 4 algorithms...")

    start = time.time()
    paths['BFS'] = BFS(m)
    timers['BFS'] = round(time.time() - start, 4)

    start = time.time()
    paths['DFS'] = DFS(m)
    timers['DFS'] = round(time.time() - start, 4)

    start = time.time()
    paths['Dijkstra'] = Dijkstra(m)
    timers['Dijkstra'] = round(time.time() - start, 4)

    start = time.time()
    paths['A*'] = AStar(m)
    timers['A*'] = round(time.time() - start, 4)

    # Assign different agents and colors
    agents = {
    'BFS': agent(m, filled=True, footprints=True, color=COLOR.green),
    'DFS': agent(m, filled=True, footprints=True, color=COLOR.yellow), 
    'Dijkstra': agent(m, filled=True, footprints=True, color=COLOR.red),
    'A*': agent(m, filled=True, footprints=True, color=COLOR.blue)
}


    # Animate and trace paths
    for algo in paths:
        m.tracePath({agents[algo]: paths[algo]}, delay=30)

    # Show stats
    for algo in paths:
        textLabel(m, f'{algo} Time (s)', timers[algo])
        textLabel(m, f'{algo} Path Length', len(paths[algo]) + 1)

    m.run()

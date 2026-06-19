import random
from collections import deque


def GenerateMaze(Width, Height, Seed=None, OnProgress=None):
    """
    基于种子生成指定大小的迷宫点阵，并标注解法路径。

    参数:
        Width: 迷宫横向单元格数
        Height: 迷宫纵向单元格数
        Seed: 随机种子（字符串或数字）
        OnProgress: 进度回调，接收 0.0 ~ 1.0

    返回:
        二维列表 (2*Height+1) x (2*Width+1)，其中:
            1 = 墙
            0 = 通路
            2 = 解法路径
    """
    if Seed is not None:
        random.seed(Seed)

    # 初始化全墙网格
    Grid = [[1 for _ in range(2 * Width + 1)] for _ in range(2 * Height + 1)]
    Visited = [[False for _ in range(Width)] for _ in range(Height)]

    # 迭代回溯生成迷宫（显式栈，避免递归深度限制）
    Stack = [(0, 0)]
    Visited[0][0] = True
    VisitedCount = 1
    Grid[1][1] = 0
    Directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    TotalCells = Width * Height

    while Stack:
        CellX, CellY = Stack[-1]
        Neighbors = []
        for DeltaX, DeltaY in Directions:
            NextX, NextY = CellX + DeltaX, CellY + DeltaY
            if 0 <= NextX < Width and 0 <= NextY < Height and not Visited[NextY][NextX]:
                Neighbors.append((DeltaX, DeltaY, NextX, NextY))

        if Neighbors:
            DeltaX, DeltaY, NextX, NextY = random.choice(Neighbors)
            Visited[NextY][NextX] = True
            VisitedCount += 1
            if OnProgress and VisitedCount % 10 == 0:
                OnProgress(0.7 * VisitedCount / TotalCells)
            Grid[2 * CellY + 1 + DeltaY][2 * CellX + 1 + DeltaX] = 0
            Grid[2 * NextY + 1][2 * NextX + 1] = 0
            Stack.append((NextX, NextY))
        else:
            Stack.pop()

    # 使用 BFS 寻找从起点到终点的最短路径
    Start = (0, 0)
    End = (Width - 1, Height - 1)

    Queue = deque([(Start, [Start])])
    Seen = {Start}
    SeenCount = 1
    SolutionPath = []

    while Queue:
        (CurrentX, CurrentY), Path = Queue.popleft()
        if (CurrentX, CurrentY) == End:
            SolutionPath = Path
            break

        for DeltaX, DeltaY in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            NextX, NextY = CurrentX + DeltaX, CurrentY + DeltaY
            if 0 <= NextX < Width and 0 <= NextY < Height:
                WallY = 2 * CurrentY + 1 + DeltaY
                WallX = 2 * CurrentX + 1 + DeltaX
                if Grid[WallY][WallX] == 0 and (NextX, NextY) not in Seen:
                    Seen.add((NextX, NextY))
                    SeenCount += 1
                    if OnProgress and SeenCount % 10 == 0:
                        OnProgress(0.7 + 0.3 * SeenCount / TotalCells)
                    Queue.append(((NextX, NextY), Path + [(NextX, NextY)]))

    # 在网格上标记解法路径（包含单元格本身及单元格之间的通道）
    for i in range(len(SolutionPath)):
        CellX, CellY = SolutionPath[i]
        Grid[2 * CellY + 1][2 * CellX + 1] = 2
        if i < len(SolutionPath) - 1:
            NextX, NextY = SolutionPath[i + 1]
            Grid[CellY + NextY + 1][CellX + NextX + 1] = 2

    # 入口与出口也算作解法路径的一部分
    Grid[0][1] = 2
    Grid[2 * Height][2 * Width - 1] = 2

    if OnProgress:
        OnProgress(1.0)

    return Grid

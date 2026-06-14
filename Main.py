import pygame
import threading
from UiComponents.SimpleButton import SimpleButton
from UiComponents.TextInput import TextInput
from UiComponents.Label import Label
from MazeGenerator import GenerateMaze

# 游戏状态
GameState = {
    "State": "NOSTART",
    "Maze": None,
    "MazeWidth": 0,
    "MazeHeight": 0,
    "PlayerX": 0,
    "PlayerY": 0,
    "CellSize": 20,
    "MoveTimer": 0,
    "ShowSolution": False
}


def GameLogic(StopEvent):
    """游戏逻辑（副线程）"""
    while not StopEvent.is_set():
        pass

def ConsoleInput(StopEvent):
    """控制台输入（副线程）"""
    while not StopEvent.is_set():
        try:
            command = input(">> ")
            if command == "quit":
                StopEvent.set()
            elif command == "help":
                print("可用指令: quit, help, show")
            elif command == "show":
                GameState["ShowSolution"] = not GameState["ShowSolution"]
                print("解法路径已" + ("开启" if GameState["ShowSolution"] else "关闭"))
            else:
                print(f"未知指令: {command}")
        except EOFError:
            StopEvent.set()
            break

def Render(Screen, StartBtn, SeedInput, WidthInput, HeightInput, WinTitle, BackBtn):
    """渲染"""
    match GameState["State"]:
        case "NOSTART":
            DrawStartUi(Screen, StartBtn, SeedInput, WidthInput, HeightInput)
        case "START":
            Screen.fill((0, 0, 0))
            DrawMaze(Screen)
        case "WIN":
            Screen.fill((0, 0, 0))
            DrawMaze(Screen)
            DrawWinUi(Screen, WinTitle, BackBtn)

    pygame.display.flip()

def DrawStartUi(Screen, StartBtn, SeedInput, WidthInput, HeightInput):
    """绘制开始界面"""
    # 绘制背景
    Screen.fill((0, 0, 0))
    # 更新按钮位置
    StartBtn.UpdatePosition(Screen)
    # 绘制按钮
    StartBtn.Draw(Screen)
    # 更新并绘制输入框
    SeedInput.UpdatePosition(Screen)
    SeedInput.Draw(Screen)
    WidthInput.UpdatePosition(Screen)
    WidthInput.Draw(Screen)
    HeightInput.UpdatePosition(Screen)
    HeightInput.Draw(Screen)


def DrawMaze(Screen):
    """绘制迷宫（带相机跟随与视口剔除）"""
    Maze = GameState["Maze"]
    if Maze is None:
        return

    CellSize = GameState["CellSize"]
    PlayerX = GameState["PlayerX"]
    PlayerY = GameState["PlayerY"]

    # 相机偏移：以角色为中心
    PlayerPixelX = (2 * PlayerX + 1) * CellSize + CellSize // 2
    PlayerPixelY = (2 * PlayerY + 1) * CellSize + CellSize // 2
    CameraX = Screen.get_width() // 2 - PlayerPixelX
    CameraY = Screen.get_height() // 2 - PlayerPixelY

    ScreenWidth = Screen.get_width()
    ScreenHeight = Screen.get_height()

    for RowIndex, Row in enumerate(Maze):
        for ColIndex, Cell in enumerate(Row):
            PixelX = ColIndex * CellSize + CameraX
            PixelY = RowIndex * CellSize + CameraY

            # 视口剔除：只渲染屏幕内及边缘的格子
            if PixelX + CellSize < 0 or PixelX > ScreenWidth or PixelY + CellSize < 0 or PixelY > ScreenHeight:
                continue

            if Cell == 1:
                Color = (40, 40, 40)
            elif Cell == 2 and GameState["ShowSolution"]:
                Color = (0, 60, 0)
            else:
                Color = (0, 0, 0)

            pygame.draw.rect(Screen, Color, (PixelX, PixelY, CellSize, CellSize))

    # 绘制角色
    PlayerDrawX = (2 * PlayerX + 1) * CellSize + CameraX
    PlayerDrawY = (2 * PlayerY + 1) * CellSize + CameraY
    pygame.draw.rect(Screen, (255, 100, 100), (PlayerDrawX + 2, PlayerDrawY + 2, CellSize - 4, CellSize - 4), border_radius=CellSize // 4)


def DrawWinUi(Screen, WinTitle, BackBtn):
    """绘制胜利界面"""
    Overlay = pygame.Surface((Screen.get_width(), Screen.get_height()))
    Overlay.set_alpha(180)
    Overlay.fill((0, 0, 0))
    Screen.blit(Overlay, (0, 0))

    WinTitle.UpdatePosition(Screen)
    WinTitle.Draw(Screen)

    BackBtn.UpdatePosition(Screen)
    BackBtn.Draw(Screen)


def ReturnToMenu():
    """返回主菜单"""
    GameState["State"] = "NOSTART"
    GameState["Maze"] = None


def StartGame(SeedInput, WidthInput, HeightInput):
    """开始游戏"""
    print("开始游戏")
    try:
        Width = int(WidthInput.GetText())
        Height = int(HeightInput.GetText())
    except ValueError:
        Width, Height = 10, 10
    if Width < 5:
        Width = 5
    elif Width > 1000:
        Width = 1000
    if Height < 5:
        Height = 5
    elif Height > 1000:
        Height = 1000
    GameState["State"] = "START"
    GameState["Maze"] = GenerateMaze(Width, Height, SeedInput.Text)
    GameState["MazeWidth"] = Width
    GameState["MazeHeight"] = Height
    GameState["PlayerX"] = 0
    GameState["PlayerY"] = 0
    GameState["CellSize"] = 20
    GameState["MoveTimer"] = 0

def Main():
    print("Success Start of maze-python-game!")
    pygame.init()

    Screen = pygame.display.set_mode((640, 480), pygame.RESIZABLE)
    pygame.display.set_caption("Maze-Python-Game")
    Clock = pygame.time.Clock()

    StopEvent = threading.Event()

    # 创建种子输入框
    SeedInput = TextInput(
        Width=200,
        Height=40,
        FontSize=24,
        Placeholder="请输入种子",
        PositionFunc=lambda Screen: (Screen.get_width() - 200, Screen.get_height() - 50)
    )
    WidthInput = TextInput(
        Width=200,
        Height=40,
        FontSize=24,
        Placeholder="宽度 (5-1000)",
        PositionFunc=lambda Screen: (Screen.get_width() - 200, Screen.get_height() - 150)
    )
    HeightInput = TextInput(
        Width=200,
        Height=40,
        FontSize=24,
        Placeholder="高度 (5-1000)",
        PositionFunc=lambda Screen: (Screen.get_width() - 200, Screen.get_height() - 100)
    )

    # 创建按钮（绑定回调和动态位置）
    StartBtn = SimpleButton(
        Text="开始游戏",
        FontSize=36,
        OnClick=lambda: StartGame(SeedInput, WidthInput, HeightInput),
        PositionFunc=lambda Screen: (Screen.get_width() - 200, Screen.get_height() - 210)
    )

    WinTitle = Label(
        Text="恭喜通关！",
        FontSize=48,
        TextColor=(255, 215, 0),
        PositionFunc=lambda Screen: (Screen.get_width() // 2 - 120, Screen.get_height() // 2 - 100)
    )
    BackBtn = SimpleButton(
        Text="返回主菜单",
        FontSize=28,
        OnClick=ReturnToMenu,
        PositionFunc=lambda Screen: (Screen.get_width() // 2 - 100, Screen.get_height() // 2)
    )

    threading.Thread(target=GameLogic, args=(StopEvent,), daemon=True).start()
    threading.Thread(target=ConsoleInput, args=(StopEvent,), daemon=True).start()

    while not StopEvent.is_set():
        TimeDelta = Clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                StopEvent.set()
                break

            if GameState["State"] == "NOSTART":
                StartBtn.HandleEvent(event)
                SeedInput.HandleEvent(event)
                WidthInput.HandleEvent(event)
                HeightInput.HandleEvent(event)
            elif GameState["State"] == "WIN":
                BackBtn.HandleEvent(event)

        if GameState["State"] == "NOSTART":
            SeedInput.Update(TimeDelta)
            WidthInput.Update(TimeDelta)
            HeightInput.Update(TimeDelta)
        elif GameState["State"] == "START":
            GameState["MoveTimer"] += TimeDelta
            if GameState["MoveTimer"] >= 0.15:
                Keys = pygame.key.get_pressed()
                Maze = GameState["Maze"]
                PlayerX = GameState["PlayerX"]
                PlayerY = GameState["PlayerY"]
                Width = GameState["MazeWidth"]
                Height = GameState["MazeHeight"]
                Moved = False

                if (Keys[pygame.K_w] or Keys[pygame.K_UP]) and PlayerY > 0:
                    if Maze[2 * PlayerY][2 * PlayerX + 1] != 1:
                        GameState["PlayerY"] -= 1
                        Moved = True
                elif (Keys[pygame.K_s] or Keys[pygame.K_DOWN]) and PlayerY < Height - 1:
                    if Maze[2 * PlayerY + 2][2 * PlayerX + 1] != 1:
                        GameState["PlayerY"] += 1
                        Moved = True
                elif (Keys[pygame.K_a] or Keys[pygame.K_LEFT]) and PlayerX > 0:
                    if Maze[2 * PlayerY + 1][2 * PlayerX] != 1:
                        GameState["PlayerX"] -= 1
                        Moved = True
                elif (Keys[pygame.K_d] or Keys[pygame.K_RIGHT]) and PlayerX < Width - 1:
                    if Maze[2 * PlayerY + 1][2 * PlayerX + 2] != 1:
                        GameState["PlayerX"] += 1
                        Moved = True

                if Moved:
                    GameState["MoveTimer"] = 0
                    if GameState["PlayerX"] == Width - 1 and GameState["PlayerY"] == Height - 1:
                        GameState["State"] = "WIN"

        Render(Screen, StartBtn, SeedInput, WidthInput, HeightInput, WinTitle, BackBtn)

    pygame.quit()

if __name__ == "__main__":
    Main()

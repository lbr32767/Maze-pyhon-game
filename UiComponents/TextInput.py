import pygame
from .FontManager import GetChineseFont


class TextInput:
    def __init__(self, Width=200, Height=40, FontSize=24, Placeholder="", PositionFunc=None, OnSubmit=None):
        self.Width = Width
        self.Height = Height
        self.FontSize = FontSize
        self.Placeholder = Placeholder
        self.PositionFunc = PositionFunc
        self.OnSubmit = OnSubmit
        self.Rect = pygame.Rect(0, 0, Width, Height)
        self.Text = ""
        self.Active = False
        self.CursorVisible = True
        self.CursorTimer = 0

    def UpdatePosition(self, Screen):
        """更新位置"""
        if self.PositionFunc:
            X, Y = self.PositionFunc(Screen)
            self.Rect.x = X
            self.Rect.y = Y

    def Draw(self, Screen):
        """绘制输入框"""
        # 边框颜色（激活时高亮）
        BorderColor = (100, 100, 100) if self.Active else (60, 60, 60)
        pygame.draw.rect(Screen, (30, 30, 30), self.Rect)
        pygame.draw.rect(Screen, BorderColor, self.Rect, 2)

        # 渲染文字
        Font = GetChineseFont(self.FontSize)
        if self.Text:
            TextSurface = Font.render(self.Text, True, (255, 255, 255))
        else:
            TextSurface = Font.render(self.Placeholder, True, (120, 120, 120))

        Screen.blit(TextSurface, (self.Rect.x + 8, self.Rect.y + (self.Height - TextSurface.get_height()) // 2))

        # 绘制光标
        if self.Active and self.CursorVisible:
            CursorX = self.Rect.x + 8
            if self.Text:
                CursorX += TextSurface.get_width()
            pygame.draw.line(Screen, (255, 255, 255), (CursorX, self.Rect.y + 5), (CursorX, self.Rect.y + self.Height - 5), 2)

    def HandleEvent(self, Event):
        """处理事件"""
        if Event.type == pygame.MOUSEBUTTONDOWN:
            self.Active = self.Rect.collidepoint(Event.pos)
            return self.Active

        if Event.type == pygame.KEYDOWN and self.Active:
            if Event.key == pygame.K_RETURN:
                if self.OnSubmit:
                    self.OnSubmit(self.Text)
            elif Event.key == pygame.K_BACKSPACE:
                self.Text = self.Text[:-1]
            else:
                self.Text += Event.unicode
            return True

        return False

    def Update(self, TimeDelta):
        """更新光标闪烁"""
        self.CursorTimer += TimeDelta
        if self.CursorTimer >= 0.5:
            self.CursorTimer = 0
            self.CursorVisible = not self.CursorVisible

    def GetText(self):
        """获取输入内容"""
        return self.Text

    def SetText(self, Text):
        """设置输入内容"""
        self.Text = Text

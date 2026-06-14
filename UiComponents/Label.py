import pygame
from .FontManager import GetChineseFont


class Label:
    def __init__(self, Text, FontSize=24, TextColor=(255, 255, 255), PositionFunc=None):
        self.Text = Text
        self.FontSize = FontSize
        self.TextColor = TextColor
        self.PositionFunc = PositionFunc
        self.Rect = pygame.Rect(0, 0, 0, 0)

    def UpdatePosition(self, Screen):
        """更新位置"""
        if self.PositionFunc:
            X, Y = self.PositionFunc(Screen)
            self.Rect.x = X
            self.Rect.y = Y

    def Draw(self, Screen):
        """绘制文字标签"""
        Font = GetChineseFont(self.FontSize)
        TextSurface = Font.render(self.Text, True, self.TextColor)
        self.Rect.width = TextSurface.get_width()
        self.Rect.height = TextSurface.get_height()
        Screen.blit(TextSurface, (self.Rect.x, self.Rect.y))

    def SetText(self, Text):
        """更新文字内容"""
        self.Text = Text

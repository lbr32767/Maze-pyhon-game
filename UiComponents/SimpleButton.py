import pygame
from .FontManager import GetChineseFont


class SimpleButton:
    def __init__(self, Text, FontSize=36, OnClick=None, PositionFunc=None, Width=200, Height=50):
        self.Text = Text
        self.FontSize = FontSize
        self.OnClick = OnClick
        self.PositionFunc = PositionFunc
        self.Width = Width
        self.Height = Height
        self.Rect = pygame.Rect(0, 0, Width, Height)
        self.ClickTime = 0

    def UpdatePosition(self, Screen):
        """更新位置（支持动态计算）"""
        if self.PositionFunc:
            X, Y = self.PositionFunc(Screen)
            self.Rect.x = X
            self.Rect.y = Y

    def Draw(self, Screen):
        """绘制按钮"""
        if pygame.time.get_ticks() - self.ClickTime < 300:
            BgColor = (100, 100, 100)
        else:
            BgColor = (60, 60, 60)
        pygame.draw.rect(Screen, BgColor, self.Rect)
        Font = GetChineseFont(self.FontSize)
        TextSurface = Font.render(self.Text, True, (255, 255, 255))
        Screen.blit(TextSurface, (self.Rect.x + (self.Rect.width - TextSurface.get_width()) // 2,
                                   self.Rect.y + (self.Rect.height - TextSurface.get_height()) // 2))

    def HandleEvent(self, Event):
        """处理事件"""
        if Event.type == pygame.MOUSEBUTTONDOWN and self.Rect.collidepoint(Event.pos):
            self.ClickTime = pygame.time.get_ticks()
            if self.OnClick:
                self.OnClick()
            return True
        return False

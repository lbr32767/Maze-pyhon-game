import pygame
import sys


# 跨平台中文字体路径
_FONT_PATHS = {
    "win32": [
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/simsun.ttc",
    ],
    "darwin": [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/STHeiti Medium.ttc",
    ],
    "linux": [
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
        "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto-cjk/NotoSansCJK-Regular.ttc",
    ],
}

_font_cache = {}


def GetChineseFont(Size=36):
    """获取支持中文的字体（带缓存）"""
    if Size in _font_cache:
        return _font_cache[Size]

    for Path in _FONT_PATHS.get(sys.platform, []):
        try:
            Font = pygame.font.Font(Path, Size)
            _font_cache[Size] = Font
            return Font
        except (OSError, pygame.error):
            continue

    Font = pygame.font.Font(None, Size)
    _font_cache[Size] = Font
    return Font

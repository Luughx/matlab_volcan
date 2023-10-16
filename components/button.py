import pygame as py
from components.functions import draw_text 

class Button():
    def __init__(self, x, y, width, height, color, label, spaceX, spaceY):
        self.bg = py.Surface((width, height))
        self.bg.fill(color)
        self.rect = py.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.defaultWidth = width
        self.defaultHeight = height 
        self.clicked = False
        self.label = label
        self.spaceX = spaceX
        self.spaceY = spaceY

    def draw(self, surface):
        action = False

        pos = py.mouse.get_pos()

        bg = self.bg

        if self.rect.collidepoint(pos):
            bg = py.transform.scale(self.bg, (self.width + 3, self.height + 3))
            if py.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        else:
            bg = py.transform.scale(self.bg, (self.width, self.height))

        if py.mouse.get_pressed()[0] == 0:
            self.clicked = False

        surface.blit(bg, (self.x, self.y))
        draw_text(self.label, py.font.Font("assets/Helvetica-Font/Helvetica.ttf", 25), (255, 255, 255), surface, self.x + self.spaceX, self.y + self.spaceY)

        return action
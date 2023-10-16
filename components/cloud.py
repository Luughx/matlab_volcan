import random
import pygame as py
import os

class Cloud():
    def __init__(self):
        self.velocity = random.uniform(0.6, 2.3)
        imageRaw = py.image.load(os.path.join("assets", "cloud.png"))
        imageRaw.set_alpha(random.randrange(130, 230))
        rand = random.uniform(100, 170)
        randRight = random.randrange(1, 3, 1)
        self.right = True
        
        if randRight == 1: 
            self.right = True
        else: 
            self.right = False

        self.image = py.transform.scale(imageRaw, (rand+(rand/2), rand))
        if self.right:
            self.x = 0 - (rand+(rand/2)) - random.randrange(100, 500)
        else:
            self.x = 1280 + (rand+(rand/2) + random.randrange(100, 500))

        self.y = random.randrange(80, 400)
    
    def move(self, surface, dt):
        if self.right:
            self.x += self.velocity * dt
            if self.x > surface.get_width():
                self.get_values()
            else:   
                surface.blit(self.image, (self.x, self.y))
        else:
            self.x -= self.velocity * dt
            if self.x < 0 - self.image.get_width():
                self.get_values()
            else:   
                surface.blit(self.image, (self.x, self.y))

    def get_values(self):
        self.velocity = random.uniform(0.6, 2.3)
        imageRaw = py.image.load(os.path.join("assets", "cloud.png"))
        imageRaw.set_alpha(random.uniform(130, 170))
        rand = random.uniform(100, 200)
        randRight = random.randrange(1, 3, 1)
        self.right = True
        
        if randRight == 1: 
            self.right = True
        else: 
            self.right = False

        self.image = py.transform.scale(imageRaw, (rand+(rand/2), rand))
        if self.right:
            self.x = 0 - (rand+(rand/2)) - random.randrange(100, 500)
        else:
            self.x = 1280 + (rand+(rand/2) + random.randrange(100, 500))

        self.y = random.randrange(50, 300)
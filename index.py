import pygame as py
from matlab_data import Matlab
import os
from time import time
import sys
from random import uniform
from components.cloud import Cloud
from components.functions import draw_text
from components.input import TextInput
from components.button import Button

py.init()

screenWidth = 1280
screenHeight = 720

screen = py.display.set_mode((screenWidth, screenHeight))

volcanPngRaw = py.image.load(os.path.join("assets", "volcan.png"))
volcanPng = py.transform.scale(volcanPngRaw, (513/3, 307/3))#.convert()

py.display.set_icon(volcanPng)
py.display.set_caption("HUEHUETÉOTL")

clock = py.time.Clock()

class GameState():
    def __init__(self):
        print("cargando matlab...")
        self.matlab = Matlab()
        self.state = "intro"
        self.linesArray = [1, 1, 1]
        self.clouds = [Cloud(), Cloud(), Cloud()]
        self.widthP2 = screenWidth/2-100
        self.widthP3 = screenWidth-50-180-50
        self.heightP = 190
        self.inputs = [
            TextInput(50, self.heightP, 180, 40, "Ángulo", "°"), TextInput(50, self.heightP+80, 180, 40, "Velocidad", "m/s²"), # proyectil 1
            TextInput(self.widthP2, self.heightP, 180, 40, "Ángulo", "°"), TextInput(self.widthP2, self.heightP+80, 180, 40, "Velocidad", "m/s²"), # proyectil 2
            TextInput(self.widthP3, self.heightP, 180, 40, "Ángulo", "°"), TextInput(self.widthP3, self.heightP+80, 180, 40, "Velocidad", "m/s²"), # proyectil 3
            TextInput(self.widthP2, 50, 180, 40, "Resistencia del aire", "N/(m·s²)"),
        ]
        self.velocityInput = ""
        self.velocityActive = False
        self.buttonStart = Button(self.widthP2+140, self.heightP + 160, 180, 40, (225, 141, 67), "Iniciar", 59, 10)
        self.buttonRandom = Button(self.widthP2-140, self.heightP + 160, 180, 40, (225, 141, 67), "Random", 50, 10)
        self.buttonRestart = Button(self.widthP2, self.heightP + 160, 180, 40, (225, 141, 67), "Reiniciar", 43, 10)
        self.active = False
        self.posX = [[], [], []]
        self.posY = [[], [], []]
        self.posYPos = [[], [], []]
        self.maxY = [0, 0, 0]
        self.first = [False, False, False]
        self.lastTime = time()
        self.dt = time() - self.lastTime
        self.timeP = [0, 0, 0]
        self.shapesP = [[], [], []]
        self.overflow = 0
        self.xVolcan = screenWidth/2 - 150/2

    def intro(self):
        screen.fill((47, 47, 47))

        self.dt = time() - self.lastTime
        self.dt *= 60
        self.lastTime = time()
        
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()
            if event.type == py.MOUSEBUTTONDOWN or event.type == py.KEYDOWN:
                self.state = "main_game"

        screen.fill((35, 211, 235))

        for cloud in self.clouds:
            cloud.move(screen, self.dt)

        screen.blit(volcanPng, (screenWidth/2 - 150/2, screenHeight-volcanPng.get_height()-10))

        py.draw.rect(screen, (149, 183, 55), (0, 708, 1280, 20))
        py.draw.rect(screen, (28, 155, 79), (0, 712, 1280, 20))

        opacity = py.Surface((screenWidth, screenHeight))
        opacity.set_alpha(150)
        opacity.fill((0, 0, 0))

        screen.blit(opacity, (0, 0))

        draw_text("HUEHUETÉOTL", py.font.Font("assets/Helvetica-Font/Helvetica-Bold.ttf", 70), (255, 255, 255), screen, center=True)
        draw_text("Presiona cualquier tecla para jugar", py.font.Font("assets/Helvetica-Font/Helvetica.ttf", 30), (255, 255, 255), screen, (screenWidth/2-235), (screenHeight/2+50))

    def main_game(self):
        screen.fill((35, 211, 235))

        self.dt = time() - self.lastTime
        self.dt *= 60
        self.lastTime = time()
        
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()

            for input in self.inputs:
                input.events(event)

        for cloud in self.clouds:
            cloud.move(screen, self.dt)

        if not self.active:
            heightTitles = self.heightP-70
            draw_text("Proyectil 1", py.font.Font("assets/Helvetica-Font/Helvetica-Bold.ttf", 25), (0, 0, 0), screen, 50, heightTitles)
            draw_text("Proyectil 2", py.font.Font("assets/Helvetica-Font/Helvetica-Bold.ttf", 25), (0, 0, 0), screen, self.widthP2, heightTitles)
            draw_text("Proyectil 3", py.font.Font("assets/Helvetica-Font/Helvetica-Bold.ttf", 25), (0, 0, 0), screen, self.widthP3, heightTitles)

            if self.buttonStart.draw(screen):
                self.start_button()
            if self.buttonRandom.draw(screen):
                self.random_button()

            for input in self.inputs:
                input.main(screen)
        else:
            self.updating()

        
        """ if self.overflow != 0:
            self.xVolcan -= 10 * self.dt
        else:
            self.xVolcan = screenWidth/2 - 150/2 """
        
        screen.blit(volcanPng, (self.xVolcan,  screenHeight-volcanPng.get_height()-10))

        py.draw.rect(screen, (149, 183, 55), (0, 708, 1280, 20))
        py.draw.rect(screen, (28, 155, 79), (0, 712, 1280, 20))

    def start_button(self):
        self.active = self.input_validate()
        if not self.active: return

    def random_button(self):
        self.inputs[-1].set_text(uniform(0, 0.5))
        
        self.inputs[0].set_text(uniform(0, 360))
        self.inputs[1].set_text(uniform(35, 130))

        self.inputs[2].set_text(uniform(0, 360))
        self.inputs[3].set_text(uniform(35, 130))

        self.inputs[4].set_text(uniform(0, 360))
        self.inputs[5].set_text(uniform(35, 130))
        self.active = True

    def updating(self):
        airResistant = float(self.inputs[-1].get_text())
        
        ang1 = self.inputs[0].get_text()
        vel1 = self.inputs[1].get_text()
        
        ang2 = self.inputs[2].get_text()
        vel2 = self.inputs[3].get_text()
        
        ang3 = self.inputs[4].get_text()
        vel3 = self.inputs[5].get_text()

        if vel1 != "" and ang1 != "":
            self.validate_lines(0, vel1, ang1, airResistant)

        if vel2 != "" and ang2 != "":
            self.validate_lines(1, vel2, ang2, airResistant)

        if vel3 != "" and ang3 != "":
            self.validate_lines(2, vel3, ang3, airResistant)

        self.create_data()
        
    def create_data(self):
        if len(self.posX[0]) != 0:
            self.draw_data(0, 50)
        if len(self.posX[1]) != 0:
            self.draw_data(1, self.widthP2)
        if len(self.posX[2]) != 0:
            self.draw_data(2, self.widthP3)

    def draw_data(self, num, width):
        heightP = 70
        heightTitles = heightP-40
        draw_text(f"Proyectil {num+1}", py.font.Font("assets/Helvetica-Font/Helvetica-Bold.ttf", 25), (0, 0, 0), screen, width, heightTitles)
        draw_text(f"Altura máxima: {self.convert_to_meters(self.maxY[num]):.1f} m", py.font.Font("assets/Helvetica-Font/Helvetica.ttf", 23), (0, 0, 0), screen, width, heightP)
        draw_text(f"Impacto: ({self.convert_to_meters(self.posX[num][-1]):.1f} m, {self.convert_to_meters(self.posYPos[0][-1]):.2f} m)", py.font.Font("assets/Helvetica-Font/Helvetica.ttf", 23), (0, 0, 0), screen, width, heightP+40)
        draw_text(f"Altura: {self.convert_to_meters(self.posYPos[num][self.linesArray[num]]):.1f} m", py.font.Font("assets/Helvetica-Font/Helvetica.ttf", 23), (0, 0, 0), screen, width, heightP+80)
        draw_text(f"Distancia: {self.convert_to_meters(self.posX[num][self.linesArray[num]]):.1f} m", py.font.Font("assets/Helvetica-Font/Helvetica.ttf", 23), (0, 0, 0), screen, width, heightP+120)
        draw_text(f"Velocidad: ", py.font.Font("assets/Helvetica-Font/Helvetica.ttf", 23), (0, 0, 0), screen, width, heightP+160)

    def validate_lines(self, num, vel, angle, airResistant):
        if not self.first[num]:
            self.posX[num], self.posY[num], self.posYPos[num] = self.request_lines(float(vel), float(vel), airResistant, volcanPng.get_height())
            self.maxY[num] = self.posYPos[num][0]
            self.first[num] = True
        else:
            self.create_lines(self.posX[num], self.posY[num], num)
    
    def convert_to_meters(self, value):
        return ((value * 3768) / volcanPng.get_height())

    def create_lines(self, xpos, ypos, num=0):
        for i in range(self.linesArray[num]):
            lineColor = (255, 156, 1)
            if i > len(xpos)/2:
                lineColor = (223-i, 39, 39) 
            else:
                lineColor = (255-i, 156-i, 1)

            if self.posYPos[num][i] > self.maxY[num]: 
                self.maxY[num] = self.posYPos[num][i]

            localX = xpos[i] + 78 + (screenWidth/2- 150/2)
            localY = ypos[i] + screenHeight
            
            """ if self.overflow != 0:
                print(localX)
                localX += (self.xVolcan - (screenWidth/2 - 150/2)) * self.dt
                print(localX) """

            #shape = py.draw.circle(screen, lineColor, (localX, localY), 5)
            shape = py.draw.line(screen, lineColor, (localX, localY), (xpos[i+1]+78 + (screenWidth/2 - 150/2), ypos[i+1]+screenHeight), 8)
            self.shapesP[0].append(shape)
        if self.linesArray[num] > len(xpos) - 2:
                if self.buttonRestart.draw(screen):
                    self.active = False
                    self.linesArray = [1, 1, 1]
                    self.posX = [[], [], []]
                    self.posY = [[], [], []]
                    self.first = [False, False, False]
                    self.timeP = [0, 0, 0]
                    self.overflow = 0
                    for input in self.inputs:
                        input.clear_text()
        if py.time.get_ticks() - self.timeP[num] > 150: # Tiempo que tarda cada circulo en aparecer, contando como milisegundos
            if self.linesArray[num] <= len(xpos) - 2:
                self.linesArray[num] += 1
            """ else:
                self.overflow = 0
            
            if xpos[i]+78 + (screenWidth/2- 150/2) > screenWidth:
                self.overflow = xpos[i]+78 + (screenWidth/2- 150/2) """

            self.timeP[num] = py.time.get_ticks()

    def request_lines(self, velocityX, velocityY, airResistant, volcanHeight):
        xpos, ypos = self.matlab.getPositions(velocityX, velocityY, airResistant, volcanHeight)
        yposNeg = []

        print(xpos)
        print("-----------")
        print(ypos)

        for i, pos in enumerate(ypos):
            yposNeg.append(pos*(-1))

        return xpos, yposNeg, ypos

    def input_validate(self):
        return self.inputs[0].get_text() != "" and self.inputs[1].get_text() != "" and self.inputs[6].get_text() != "" or self.inputs[2].get_text() != "" and self.inputs[3].get_text() != "" and self.inputs[6].get_text() != "" or self.inputs[4].get_text() != "" and self.inputs[5].get_text() != "" and self.inputs[6].get_text() != ""
        
    def state_manager(self):
        if self.state == "intro":
            self.intro()
        elif self.state == "main_game":
            self.main_game()
 
game_state = GameState()

while True:
    game_state.state_manager()
    py.display.update()

    clock.tick(60)

#pygame.quit()
#This code was made for school science competition

import pygame
import math
from sys import exit

pygame.init()

width = 1280
height = 720
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("physics demo")
clock = pygame.time.Clock()
running  = True

cameraOffset = pygame.Vector2(0,0)
isDragging = False
previousCameraPos = pygame.Vector2(0,0)

G = 4 # gravitational constant
objFolder = []
def align(screen,x,y): 
   # pygame.draw.line(screen,"aliceblue",(0,y),(1280,y),2)
   # pygame.draw.line(screen,"aliceblue",(x,0),(x,720),2)
    pygame.draw.line(screen,"aliceblue",(x,y-10),(x,y+10),2)
    pygame.draw.line(screen,"aliceblue",(x-10,y),(x+10,y),2)
  
def gridLines(startPos,endPos):
    pygame.draw.line(screen,"grey12",startPos,endPos,2)

gridSpacing = 100
gridSize = [width,height]
def grid():
    for x in range(0,gridSize[0],gridSpacing):
        gridLines((x,0),(x,gridSize[1])) 

    for y in range(0,gridSize[1],gridSpacing):
        gridLines((0,y),(gridSize[0],y)) 

class celestialBody():
    def __init__(self,x,y,vx,vy,mass):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.mass = mass
        self.trail = []

    def createGravity(self,obj2): # F = G{m1*m2/distance^2}
        dx = obj2.x  - self.x
        dy = obj2.y - self.y
        distance = math.sqrt(dx**2 + dy **2)

        if distance < 250:
            return

        dx /= distance
        dy /= distance

        force = G * (self.mass * obj2.mass) / (distance)**2

        ax = dx * force / self.mass
        ay = dy * force / self.mass

        self.vx += ax
        self.vy += ay

    def updatePos(self):
        self.x += self.vx
        self.y += self.vy

for i in range(100): #number of planets/bodies
    body = celestialBody(20* i,20* i,0,0,15) #[x,y,vx,vy,mass]
    objFolder.append(body)

Star = celestialBody(640,360,0,0,5000) #[x,y,vx,vy,mass] -- the star itself
objFolder.append(Star)

#denserStar = celestialBody(1280,360,0,0,600) #[x,y,vx,vy,mass] -- another mass heavier than the planets but lighter than the Star
#objFolder.append(denserStar)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
             pygame.quit()
             exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            isDragging = True
            previousCameraPos = pygame.Vector2(event.pos)

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            isDragging = False

        if event.type == pygame.MOUSEMOTION and isDragging:
            mousePos = pygame.Vector2(event.pos)
            cameraOffset += mousePos - previousCameraPos
            previousCameraPos = mousePos

        
   
    screen.fill("grey2")
    grid()
    mouse_x, mouse_y = pygame.mouse.get_pos()

    pygame.draw.circle(screen, "lightgoldenrod1", (Star.x + cameraOffset.x,Star.y + cameraOffset.y),50)
    #pygame.draw.circle(screen, "coral", (denserStar.x + cameraOffset.x + cameraOffset.y,denserStar.y),30)
    for i in objFolder:
        for j in objFolder:
            if i != j:
                i.createGravity(j)

    for obj in objFolder:
        obj.updatePos()
        if obj.mass < 100:
            pygame.draw.circle(screen,"mediumseagreen",(obj.x + cameraOffset.x,obj.y + cameraOffset.y),2)

    align(screen,mouse_x,mouse_y)

    pygame.display.update()
    dt = clock.tick(60)
import pygame
import turtle
import time
import random

pygame.init()

width = 1156 # should be 1280
height = 629 # should be 720
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Physics Simulation") 
clock = pygame.time.Clock()
running  = True

gonzi_img = pygame.image.load('Images/Pi Placeholder layout.png').convert()

x = 0
balls_num = 5
ball_radius = 40

black = (0,0,0)
white = (255,255,255)
red = (255, 0, 0)
blue = (0,0,255)

speed = [10,10]

balls = []
velocities = []

for _ in range(balls_num):

    x = random.randint(ball_radius,width - ball_radius)
    y = random.randint(ball_radius, height - ball_radius)
    balls.append(pygame.Rect(x,y,ball_radius*2,ball_radius*2))
    velocities.append([random.choice([-5, 5]), random.choice([-5, 5])])

while running:  

    #screen.blit(gonzi_img, (x,0))

    #x += 0.5

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
             pygame.quit()
             exit()
    
    screen.fill("black")

    for i in range(balls_num):
        
        ball = balls[i]
        ball.x += velocities[i][0]
        ball.y += velocities[i][1]

        if ball.left <= 0 or ball.right >= width:
            velocities[i][0] = -velocities[i][0]
        if ball.top <= 0 or ball.bottom >= height:
            velocities[i][1] = -velocities[i][1]

        pygame.draw.circle(screen, blue, ball.center, ball_radius)


    pygame.display.flip()
    pygame.display.update()
    dt = clock.tick(60)

import pygame
import random

pygame.init()

width = 1280
height = 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Physics Simulation")
clock = pygame.time.Clock()
running = True

gonzi_img = pygame.image.load('Images/Pi Placeholder layout.png').convert()

balls_num = 20
ball_radius = 40

black = (0, 0, 0)
white = (255,255,255)
random_colour = (125,74,36)

texture = pygame.image.load('Images/golf ball.jpg').convert()
texture = pygame.transform.scale(texture, (ball_radius * 2, ball_radius * 2))

balls = []
velocities = []

def text(text_colour,text,typeof_font):

    typeof_font = pygame.font.SysFont(typeof_font,30)
    text_colour = text_colour

    text_surface = typeof_font.render(text,True,text_colour)
    text_rect = text_surface.get_rect()

    text_rect.bottomright = (width - int(10.222222222222222222222222222), height- float(10))
    screen.blit(text_surface,text_rect)

def createBall():

    ball = balls[i]
    ball.x += velocities[i][0] 
    ball.y += velocities[i][1]

    ball_surface = pygame.Surface((ball_radius * 2, ball_radius * 2), pygame.SRCALPHA)

    pygame.draw.circle(ball_surface, (255, 255, 255, 255), (ball_radius, ball_radius), ball_radius)

    ball_surface.blit(texture, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    screen.blit(ball_surface, (ball.x, ball.y))

    if ball.left <= 0 or ball.right >= width:
        velocities[i][0] = -velocities[i][0]

    if ball.top <= 0 or ball.bottom >= height:
        velocities[i][1] = -velocities[i][1]



for _ in range(balls_num):

    x = random.randint(ball_radius, width - ball_radius)
    y = random.randint(ball_radius, height - ball_radius)
    balls.append(pygame.Rect(x, y, ball_radius * 2, ball_radius * 2))
    velocities.append([random.choice([-5, 5]), random.choice([-5, 5])])


while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill(black)

    for i in range(balls_num):

        createBall()

        text(random_colour,"V 1.01","Segoe UI")

    pygame.display.flip()
    clock.tick(60)

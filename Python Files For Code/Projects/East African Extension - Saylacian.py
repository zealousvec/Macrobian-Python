import pygame
import math

pygame.init()

Width_Num = 800
Height_Num = 800
Screen = pygame.display.set_mode((Width_Num, Height_Num))
pygame.display.set_caption("π: Visualizing an Irrational Number")
Clock = pygame.time.Clock()

Center_X = Width_Num // 2
Center_Y = Height_Num // 2
Radius = 200

Trace_Points = []
Angle = 0
Speed = 0.15  # Higher precision and smoother motion

Font = pygame.font.SysFont("Segoe UI", 24)

Running = True

while Running:
    for Event in pygame.event.get():
        if Event.type == pygame.QUIT:
            Running = False

    Screen.fill((255, 255, 255))

    # Update angle using irrational π step
    Angle += Speed

    X = Center_X + math.cos(Angle * math.pi) * Radius
    Y = Center_Y + math.sin(Angle * math.pi) * Radius

    Trace_Points.append((X, Y))

    # Draw traced points
    for Point in Trace_Points:
        pygame.draw.circle(Screen, (200, 200, 255), (int(Point[0]), int(Point[1])), 1)

    # Draw center and rotating line
    pygame.draw.circle(Screen, (0, 0, 0), (Center_X, Center_Y), 4)
    pygame.draw.line(Screen, (0, 0, 0), (Center_X, Center_Y), (X, Y), 2)

    # Title
    Label = Font.render("Tracing a Circle Using Steps of π", True, (0, 0, 0))
    Screen.blit(Label, (Width_Num // 2 - Label.get_width() // 2, 20))

    pygame.display.flip()
    Clock.tick(60)

pygame.quit()


import pygame
import random
import math

pygame.init()

Width_Num = 1280
Height_Num = 720

Ball_Radius = 40
Balls_Num = 20

White = (255, 255, 255)
Black = (0, 0, 0)

Screen = pygame.display.set_mode((Width_Num, Height_Num))
pygame.display.set_caption("Physics Simulation")
Clock = pygame.time.Clock()
Running = True

Texture_Image = pygame.image.load('Images/golf ball.jpg').convert()
PlayButton_Image = pygame.image.load('Images/Play Button Text.jpg').convert()
Texture = pygame.transform.scale(Texture_Image, (Ball_Radius * 2, Ball_Radius * 2))

Balls = []
Velocities = []

Start_Simulation = False
Show_Credits = False

def Text(Text_Colour, Text, TypeOfFont, Width_Num, Height_Num, Size, Align='bottomright'):
    Font = pygame.font.SysFont(TypeOfFont, Size)
    Text_Surface = Font.render(Text, True, Text_Colour)
    Text_Rect = Text_Surface.get_rect()

    if Align == 'center':
        Text_Rect.center = (Width_Num, Height_Num)
    elif Align == 'topleft':
        Text_Rect.topleft = (Width_Num, Height_Num)
    elif Align == 'topright':
        Text_Rect.topright = (Width_Num, Height_Num)
    elif Align == 'bottomleft':
        Text_Rect.bottomleft = (Width_Num, Height_Num)
    else:
        Text_Rect.bottomright = (Width_Num, Height_Num)

    Screen.blit(Text_Surface, Text_Rect)

def Create_Ball(i):
    
    Ball = Balls[i]
    Ball.x += Velocities[i][0]
    Ball.y += Velocities[i][1]

    Ball_Surface = pygame.Surface((Ball_Radius * 2, Ball_Radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(Ball_Surface, (255, 255, 255, 255), (Ball_Radius, Ball_Radius), Ball_Radius)
    Ball_Surface.blit(Texture, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    Screen.blit(Ball_Surface, (Ball.x, Ball.y))

    if Ball.left <= 0 or Ball.right >= Width_Num:
        Velocities[i][0] = -Velocities[i][0]

    if Ball.top <= 0 or Ball.bottom >= Height_Num:
        Velocities[i][1] = -Velocities[i][1]

def Add_Balls(num):
    global Balls_Num

    for _ in range(num):
        x = random.randint(Ball_Radius, Width_Num - Ball_Radius)
        y = random.randint(Ball_Radius, Height_Num - Ball_Radius)
        Balls.append(pygame.Rect(x, y, Ball_Radius * 2, Ball_Radius * 2))
        Velocities.append([random.choice([-5, 5]), random.choice([-5, 5])])

    Balls_Num = len(Balls)

def Remove_Balls(num):
    global Balls_Num

    if len(Balls) >= num:
        for _ in range(num):
            Balls.pop()
            Velocities.pop()

        Balls_Num = len(Balls)

def Initialize_Balls():
    global Start_Simulation
    Start_Simulation = True

def Start_Sim(self):
    global Start_Simulation, Show_Credits
    Start_Simulation = True
    Show_Credits = False
    Add_Balls(10)
    self.Clicked = not self.Clicked

def Show_Credits_Screen(self):
    global Start_Simulation, Show_Credits
    Start_Simulation = False
    Show_Credits = True
    self.Clicked = not self.Clicked

class Button:

    def __init__(self, x, y, Text_Str, Font_Name, Font_Size, Text_Colour, Align='center', On_Click=None):

        self.X = x
        self.Y = y
        self.Text_Str = Text_Str
        self.Font_Name = Font_Name
        self.Font_Size = Font_Size
        self.Text_Colour = Text_Colour
        self.Align = Align
        self.Clicked = False
        self.On_Click = On_Click

        Font_Obj = pygame.font.SysFont(Font_Name, Font_Size)
        Text_Surface = Font_Obj.render(Text_Str, True, Text_Colour)
        Text_Rect = Text_Surface.get_rect()

        if Align == 'center':
            Text_Rect.center = (x, y)
        elif Align == 'topleft':
            Text_Rect.topleft = (x, y)
        elif Align == 'topright':
            Text_Rect.topright = (x, y)
        elif Align == 'bottomleft':
            Text_Rect.bottomleft = (x, y)
        else:
            Text_Rect.bottomright = (x, y)

        self.Text_Rect = Text_Rect

    def Draw(self):
        Pos = pygame.mouse.get_pos()

        if self.Text_Rect.collidepoint(Pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.Clicked: # its a tuple btw (go on docs if u dont get it)
                self.Clicked = True

                if self.On_Click:
                    self.On_Click(self)

        if not self.Clicked:
            Text(self.Text_Colour, self.Text_Str, self.Font_Name, self.X, self.Y, self.Font_Size, Align=self.Align)

Button_Spacing = 80
Button_Center_X = Width_Num // 2
Button_Center_Y = Height_Num // 2

Play_Button = Button(

    Button_Center_X,
    Button_Center_Y - 20,
    "Play",
    "Segoe UI",
    60,
    White,
    Align='center',
    On_Click=Start_Sim

)

Credit_Button = Button(

    Button_Center_X,
    Button_Center_Y + 40,
    "Credits",
    "Segoe UI",
    40,
    White,
    Align='center',
    On_Click=Show_Credits_Screen

)

while Running:

    events = pygame.event.get()

    for event in events:

        if event.type == pygame.QUIT:

            Running = False
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                Start_Simulation = False
                Show_Credits = False

            if event.key == pygame.K_e:
                Add_Balls(10)

            elif event.key == pygame.K_q:
                Remove_Balls(10)

    Screen.fill(Black)

    if not Start_Simulation and not Show_Credits:

        Play_Button.Draw()
        Credit_Button.Draw()

        Text(White, "Physics Simulation", "SegoeUI", Width_Num // 2, Height_Num // 2 - 100, 100, Align='center')

    if Show_Credits:

        Text(White, "Created by Dahir Hassan", "Segoe UI", Width_Num // 2, Height_Num // 2, 40, Align='center')
        Text(White, "Press ESC to return", "Segoe UI", Width_Num // 2, Height_Num // 2 + 50, 30, Align='center')
        Text(White, "V 1.01", "Segoe UI", Width_Num - 10, Height_Num - 5, 30, Align='bottomright')

    if Start_Simulation:

        for i in range(len(Balls)):
            Create_Ball(i)

        Text(White, "V 1.01", "Segoe UI", Width_Num - 10, Height_Num - 5, 30, Align='bottomright')
        Text(White, "Created by Dahir Hassan", "Segoe UI", Width_Num - 10, Height_Num - 40, 20, Align='bottomright')

    pygame.display.flip()
    Clock.tick(60)


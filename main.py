import pygame
import os
import random
import sys
pygame.init()
from pygame import mixer

# Global constants
SCREEN_HEIGHT=600
SCREEN_WIDTH=1100
SCREEN=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
RUNNING=[pygame.image.load(os.path.join("Game/run","marioRUN1.PNG")),
         pygame.image.load(os.path.join("Game/run","marioRUN2.PNG")),
         pygame.image.load(os.path.join("Game/run","marioRUN3.PNG"))]
JUMP=pygame.image.load(os.path.join("Game/jump","marioRUN2.PNG"))
SMALL_PIPE=[pygame.image.load(os.path.join("Game/pipe","pipe1.PNG")),
            pygame.image.load(os.path.join("Game/pipe","pipe2.PNG")),
            pygame.image.load(os.path.join("Game/pipe","pipe3.PNG"))]
BIG_PIPE=[pygame.image.load(os.path.join("Game/pipe","pipe4.PNG")),
          pygame.image.load(os.path.join("Game/pipe","pipe5.PNG")),
          pygame.image.load(os.path.join("Game/pipe","pipe6.PNG"))]
CLOUD=pygame.image.load(os.path.join("Game/cloud","backgroung.PNG"))
BG=pygame.image.load(os.path.join("Game/backgroung","base.PNG"))
music=pygame.mixer.music.load('start.mp3')
pygame.mixer.music.play(-1)
jumping=pygame.mixer.Sound('jump.wav')
gameover=pygame.mixer.Sound('gameover.mp3')


class Mario:
    X_pos=10
    Y_pos=470
    JUMP_VEL=11
    def __init__(self):
        self.run_img=RUNNING
        self.jump_img=JUMP

        self.mario_run=True
        self.mario_jump =False

        self.step_index = 0
        self.jump_vel=self.JUMP_VEL
        self.image = self.run_img[0]
        self.mario_rect = self.image.get_rect()
        self.mario_rect.x = self.X_pos
        self.mario_rect.y = self.Y_pos

    def update(self, userInput):
            if self.mario_run:
                self.run()
            if self.mario_jump:
                self.jump()

            if self.step_index >= 15:
                self.step_index = 0

            if userInput[pygame.K_UP] and not self.mario_jump:
                jumping.play()
                self.mario_run = False
                self.mario_jump = True
            elif not (self.mario_jump):
                self.mario_run = True
                self.mario_jump = False

    def jump(self):
        self.image= self.jump_img
        if self.mario_jump:
            self.mario_rect.y-=self.jump_vel*4
            self.jump_vel -=0.9
        if self.jump_vel < -self.JUMP_VEL:
            self.mario_jump= False
            self.jump_vel = self.JUMP_VEL

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.mario_rect = self.image.get_rect()
        self.mario_rect.x = self.X_pos
        self.mario_rect.y = self.Y_pos
        self.step_index += 1

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.mario_rect.x, self.mario_rect.y))

class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(40, 100)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(70, 100)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))

class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

class SmallPipe(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 480

class LargePipe(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0,2)
        super().__init__(image, self.type)
        self.rect.y = 460

def main():
    global game_speed , x_pos_bg,y_pos_bg,points,obstacles
    run=True
    clock=pygame.time.Clock()
    cloud = Cloud()
    player=Mario()
    game_speed = 10
    x_pos_bg = 0
    y_pos_bg = 550
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 30)
    obstacles = []
    death_count=0

    def score():
        global points, game_speed
        points += 1

        text = font.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed


    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
                pygame.quit()
                quit()
                sys.exit()
        SCREEN.fill((152,245,255))
        userInput=pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(userInput)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallPipe(SMALL_PIPE))
            elif random.randint(0,2) == 1:
                obstacles.append(LargePipe(BIG_PIPE))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.mario_rect.colliderect(obstacle.rect):
                gameover.play()
                pygame.time.delay(2000)
                death_count+=1
                menu(death_count)


        background()

        cloud.draw(SCREEN)
        cloud.update()

        score()

        clock.tick(32)
        pygame.display.update()

def menu(death_count):
    global points
    run = True
    while run:
        SCREEN.fill((152,245,255))
        font = pygame.font.Font('freesansbold.ttf', 30)

        if death_count == 0:
            text = font.render("Press any Key to Start & UP Key to jump", True, (0, 0, 0))
        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, (0, 0, 0))
            score = font.render("Your Score: " + str(points), True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
                pygame.quit()
                quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                main()



menu(death_count=0)




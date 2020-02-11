import pygame
pygame.font.init()
# pygame.init()
# WIDTH = 500 #your width
# HEIGHT = 500 #your height
# window = pygame.display.set_mode((WIDTH, HEIGHT))
"""
FLAPPY BIRD IMPLEMENTATION 
inspired by tutorial on building the game in python by
Tech With Tim on youtube 

"""

import neat
import time
import os
import random

STAT_FONT = pygame.font.SysFont("comicsans", 50)

"""Set window size"""
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 800

"""Load in images"""
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BACKGROUND_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

"Bird class"
class Bird:
    """Load image, set animation constants"""
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROTATION_VELOCITY = 20
    ANIMATION_TIME = 5

    def __init__(self,x,y):
        self.x = x
        self.y = y  
        self.tilt = 0
        self.tick_count = 0
        self.velocity = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        "-ve velocity as 0,0 pos is top left and you need to go up when you jump "
        self.velocity = -10.5 
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count +=1
        """Tick count represents time, instantly move bird up velocity and then fall"""
        displacement = self.velocity*self.tick_count + 1.5 * self.tick_count**2
        
        """ stop bird moving too much """ 
        if displacement >= 16:
            displacement = 16

        if displacement < 0:
            displacement -= 2
        
        self.y = self.y + displacement

        """If bird is above center, tilt """
        if displacement < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else: 
            if self.tilt > -90:
                self.tilt -= self.ROTATION_VELOCITY
        
    def draw(self, window): 
        self.img_count += 1
        
        """Bird image animation cycle"""
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        """Hold animation when moving downard angle to look like nosedive"""
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2

        blitRotateCenter(window, self.img, (self.x, self.y),self.tilt)
   
    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Pipe:
    GAP = 200
    VELOCITY = 5


    def __init__(self, x):
        self.x = x
        self.height = 0
        self.gap = 100
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG
        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50,450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VELOCITY

    def draw(self, window):
        window.blit(self.PIPE_TOP, (self.x, self.top))
        window.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True
        return False

class Base:
    VELOCITY = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VELOCITY
        self.x2 -= self.VELOCITY
    
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH


    def draw(self, window):
        window.blit(self.IMG, (self.x1, self.y))
        window.blit(self.IMG, (self.x2, self.y))



def draw_window(window, bird, pipes, base, score):
    window.blit(BACKGROUND_IMG, (0,0))
    for pipe in pipes: 
        pipe.draw(window)
    text = STAT_FONT.render("Score: " + str(score), 1, (255,255,255))
    window.blit(text,( WINDOW_WIDTH - 10 - text.get_width(), 10))
    base.draw(window)
    bird.draw(window)
    pygame.display.update()


def main():

    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    bird = Bird(230,350)
    base = Base(730)
    pipes = [Pipe(700)]



    run = True
    clock = pygame.time.Clock()
    score = 0
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        add_pipe = False
        remove = []
        for pipe in pipes: 
            if pipe.collide(bird):
                pass

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                remove.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

            pipe.move()
        if add_pipe:
            score += 1 
            pipes.append(Pipe(700))

        for item in remove:
            pipes.remove(item)
            
        if bird.y + bird.img.get_height() > 730 :
            pass
        
        bird.move()
        base.move()
        draw_window(window, bird, pipes, base,score)

    pygame.quit()
    quit()

def blitRotateCenter(surface, image, topleft, angle):
    """
    Rotate a surface and blit it to the window
    :param surf: the surface to blit to
    :param image: the image surface to rotate
    :param topLeft: the top left position of the image
    :param angle: a float value for angle
    :return: None
    """
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

    surface.blit(rotated_image, new_rect.topleft)
main()



"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>

Creates a game where player shoots asteroid and gets points
If asteroid goes past player player loses points
If player and asteroid touch, a life is lost
If all 3 lives are lost game is over
Has:
Background music
Sound effects
Collision detection
Space background and spaceship
Life gain after certain time
Start Screen
Version .3
March 3rd, 2017
Author: Hamzah Ahmed
"""

import pygame, sys, time, random
from pygame.locals import *

listAsteroid=[]
listLaser=[]
leveltime=50
lives = 3
score = 0
scorelist = []
creationTime=leveltime
save = 0
time=0
gameover=False
into=True

class Background(pygame.sprite.Sprite): #Creates space background
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.image = pygame.transform.scale(self.image, (1187, 800))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class Entity(pygame.sprite.Sprite):
    """Inherited by any object in the game."""

    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # This makes a rectangle around the entity, used for anything
        # from collision to moving around.
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

class Spaceship(Entity):
    """
    Player controlled or AI controlled, main interaction with
    the game
    """

    def __init__(self, x, y, width, height):
        super(Spaceship, self).__init__(x, y, width, height)
        self.image = spaceship

class Player(Spaceship):
    """The player controlled Spaceship"""

    def __init__(self, x, y, width, height):
        super(Player, self).__init__(x, y, width, height)

        # How many pixels the Player Spaceship should move on a given frame.
        self.x_change = 0
        # How many pixels the spaceship should move each frame a key is pressed.
        self.x_dist = 5

    def MoveKeyDown(self, key):
        """Responds to a key-down event and moves accordingly"""
        if (key == pygame.K_LEFT or key == pygame.K_a):
            self.x_change += -self.x_dist
        elif (key == pygame.K_RIGHT or key == pygame.K_d):
            self.x_change += self.x_dist
        elif (key == pygame.K_SPACE):
            x = Laser(player.rect.x + 55, player.rect.y-18, 5, 2)
            lasersound.play()
            all_sprites_list.add(x)
            listLaser.append(x)
    def MoveKeyUp(self, key):
        """Responds to a key-up event and stops movement accordingly"""
        if (key == pygame.K_LEFT or key == pygame.K_a):
            self.x_change += self.x_dist
        elif (key == pygame.K_RIGHT or key == pygame.K_d):
            self.x_change += -self.x_dist
    def update(self):
        """
        Moves the Spaceship while ensuring it stays in bounds
        """
        # Moves it relative to its current location.
        self.rect.move_ip(self.x_change, 0)

        # If the Spaceship moves off the screen, put it back on.
        if self.rect.x <= 0:
            self.rect.x = 0
        elif self.rect.x > window_width:
            self.rect.x = window_width


class Laser(Entity):
    """ This class represents the laser . """

    def __init__(self, x, y, width, height):
        super(Laser, self).__init__(x, y, width, height)

        self.image = laser

        # Positive = down, negative = up
        self.y_direction = -10
        # Current speed.
        self.speed = .1
    def update(self):
        """ Move the laser. """
        self.rect.y -= 3

class Asteroid(Entity):
    """
    The Asteroid!  Moves around the screen.
    """

    def __init__(self, x, y, width, height):
        super(Asteroid, self).__init__(x, y, width, height)


        self.image = asteroids

        # Positive = down, negative = up
        self.y_direction = 3
        # # Current speed.
        self.speed = 5

    def update(self):
        # Move the Asteroid!
        self.rect.y += 3


def checkScreen(asteroids,lasers): #Checks if lasers are out of the screen and then removes
    try:
        for i in lasers:
            if i.rect.y<=-10:
                i.remove(all_sprites_list)
                lasers.remove(i)
    except:
        pass

def laserHit(asteroids,lasers): #Checks if laser hit an asteroid and removes laser and asteroid while adding score and explosion sound
    global score
    try:
        for i in asteroids:
            for x in listLaser:
                if i.rect.colliderect(x):
                    score+=100
                    explosion.play()
                    i.remove(all_sprites_list)
                    x.remove(all_sprites_list)
                    asteroids.remove(i)
                    lasers.remove(x)
    except:
        pass

def checkKill(all): #Checks if spaceship was destroyed by asteroid and removes asteroid and spaceship
    global lives, score
    for i in all:
        if i.rect.colliderect(player.rect):
            all.remove(i)
            i.remove(all_sprites_list)
            lives-=1
            deathsound.play()
            score-=100
def loadscores():
    global scorelist
    try:
        myfile = open("highscores.txt", "r")
        lines = myfile.readlines()
        scorelist = [item.strip("\n") for item in lines]
    except FileNotFoundError:
        with open('highscores.txt', 'w') as myfile:
            for i in range(10):
                myfile.write("0" + "\n")


def savescore():
    global scorelist
    loadscores()
    with open('highscores.txt', 'w') as myfile:
        scorelist.append(score)
        scorelist = [int(i) for i in scorelist]
        scorelist.sort()
        scorelist.reverse()
        scorelist = [str(i) for i in scorelist]
        for i in scorelist:
            myfile.write(str(i) + "\n")

def switchmusic(condition):
    if condition:
        pygame.mixer.music.load('Computer-melody-80s-style.mp3')
        pygame.mixer.music.play(-1, 0.0)

pygame.init()

FPS = 60  # frames per second setting
clock = pygame.time.Clock()

# set up the window


screen = pygame.display.set_mode((700, 800))
pygame.display.set_caption('Asteroid Shooter')

window_width = 540
window_height = 800

#Adds spaceship, laser, and asteroid images
BackGround = Background('space.jpg', [0,0])
spaceship = pygame.image.load('spaceship.png')
spaceship = pygame.transform.scale(spaceship, (120, 160))
laser = pygame.image.load('laser.png')
asteroids = pygame.image.load('asteroid.png')
asteroids = pygame.transform.scale(asteroids, (125, 125))

#Creates spaceship object and the first asteroid
player = Player((window_height/2)-130, 630, 120, 160)
First = Asteroid(random.randint(0, window_width), 0, 125, 125)

#Adds the first asteroid and all_sprites
listAsteroid.append(First)
all_sprites_list = pygame.sprite.Group()
all_sprites_list.add(First)
all_sprites_list.add(player)

#Text for the screen
fontObj = pygame.font.Font('freesansbold.ttf', 30)
textSurfaceObj = fontObj.render("Lives: " + str(lives), True,(255,255,255))
textRectObj=textSurfaceObj.get_rect()
textSurfaceObj2 = fontObj.render("GAME OVER", True,(255,255,255))
textSurfaceObj3 = fontObj.render("Score:" + str(score), True,(255,255,255))


loadscores()
#Scores
textSurfaceObj4 = fontObj.render("High Scores", True,(255,255,255))
score1 = fontObj.render(scorelist[0], True,(255,255,255))
score2 = fontObj.render(scorelist[1], True,(255,255,255))
score3 = fontObj.render(scorelist[2], True,(255,255,255))
score4 = fontObj.render(scorelist[3], True,(255,255,255))
score5 = fontObj.render(scorelist[4], True,(255,255,255))
score6 = fontObj.render(scorelist[5], True,(255,255,255))
score7 = fontObj.render(scorelist[6], True,(255,255,255))
score8 = fontObj.render(scorelist[7], True,(255,255,255))
score9 = fontObj.render(scorelist[8], True,(255,255,255))
score10 = fontObj.render(scorelist[9], True,(255,255,255))
#Sounds
music = pygame.mixer.music.load('spacemusic.mp3')
pygame.mixer.music.play(-1, 0.0)
lasersound = pygame.mixer.Sound('lasersound.wav')
explosion = pygame.mixer.Sound('explosion.wav')
deathsound = pygame.mixer.Sound('DJ_Scratching.wav')


#Title screen fonts
fontObj2 = pygame.font.Font('freesansbold.ttf', 60)
title = fontObj2.render("Astroshooter", True,(255,255,255))
start = fontObj2.render("Start", True,(255,255,255))

while into: #Equivalent to into == True
    screen.blit(BackGround.image, BackGround.rect)
    screen.blit(title, ((window_width/2) - 115, 80))
    screen.blit((fontObj2.render("High Score", True,(255,255,255))), ((window_width / 2)-80, 250))
    screen.blit((fontObj2.render(scorelist[0], True,(255,255,255))), ((window_width / 2), 350))
    screen.blit(start, (window_width / 2, 600))
    screen.blit(start, (window_width / 2, 600))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        #got rid of another if statement
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if start.get_rect(x=window_width / 2, y=600).collidepoint(x, y): #changed start.get_rect
                start = fontObj2.render("Start", True, (192,192,192))
                into = False

    #same as before
    pygame.display.flip()
    pygame.display.update()
    clock.tick(FPS)

while into==False:  # the main game loop
    #Adds images and text
    screen.blit(BackGround.image, BackGround.rect)
    screen.blit(textSurfaceObj,textRectObj)
    screen.blit(textSurfaceObj3,(500, 0))
    laserHit(listAsteroid,listLaser) #Check if laser hits asteroid
    checkScreen(listAsteroid,listLaser) #Check if anything off screen
    checkKill(listAsteroid)
    if creationTime<=0 and len(listAsteroid) < 5 and lives > 0:#This creates asteroids after set amount of time and if there arent more then 5 on screen and player has lives
        x=Asteroid(random.randint(0, window_width), 0, 125, 125)
        listAsteroid.append(x)
        all_sprites_list.add(x)
        leveltime-=1 #each time an asteroid is formed we make it shorter until next is made
        creationTime=leveltime

    for event in pygame.event.get(): #Closes game
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYUP:
            player.MoveKeyUp(event.key)
        elif event.type == pygame.KEYDOWN:
            player.MoveKeyDown(event.key)

    for ent in all_sprites_list:
        ent.update()
    all_sprites_list.update()
    # Calculate mechanics for each laser

    #Removes asteroid if they leave screen and takes points away
    try:
        for asteroid in listAsteroid:
            if asteroid.rect.y > window_height:
                listAsteroid.remove(asteroid)
                all_sprites_list.remove(asteroid)
                score -= 100
    except:
        pass
    if time%900==0 and time>=900: #Everytime while loop runes 1200 times a life is added
        lives+=1
        listAsteroid=listAsteroid[0:2]
    #Displays Score and lives
    textSurfaceObj = fontObj.render("Lives: " + str(lives), True,(255,255,255))
    textSurfaceObj3 = fontObj.render("Score: " + str(score), True,(255,255,255))
    if save == 0 and lives == 0:
        savescore()
        music = pygame.mixer.music.load('Computer-melody-80s-style.mp3')
        pygame.mixer.music.play(-1, 0.0)
        gameover=True
    if lives == 0 or gameover==True: #If lives are 0 removes asteroids on screen and states game over
        screen.blit(textSurfaceObj2,(window_width/2, 0))
        time=0
        listAsteroid=[]
        screen.blit(textSurfaceObj4, (window_width/2, 70))
        screen.blit(score1, (window_width / 2, 140))
        screen.blit(score2, (window_width / 2, 190))
        screen.blit(score3, (window_width / 2, 240))
        screen.blit(score4, (window_width / 2, 290))
        screen.blit(score5, (window_width / 2, 340))
        screen.blit(score6, (window_width / 2, 390))
        screen.blit(score7, (window_width / 2, 440))
        screen.blit(score8, (window_width / 2, 490))
        screen.blit(score9, (window_width / 2, 540))
        screen.blit(score10, (window_width / 2, 590))
        score1 = fontObj.render(scorelist[0], True, (255, 255, 255))
        score2 = fontObj.render(scorelist[1], True, (255, 255, 255))
        score3 = fontObj.render(scorelist[2], True, (255, 255, 255))
        score4 = fontObj.render(scorelist[3], True, (255, 255, 255))
        score5 = fontObj.render(scorelist[4], True, (255, 255, 255))
        score6 = fontObj.render(scorelist[5], True, (255, 255, 255))
        score7 = fontObj.render(scorelist[6], True, (255, 255, 255))
        score8 = fontObj.render(scorelist[7], True, (255, 255, 255))
        score9 = fontObj.render(scorelist[8], True, (255, 255, 255))
        score10 = fontObj.render(scorelist[9], True, (255, 255, 255))
        place = fontObj.render("Player place: " + str(scorelist.index(str(score))+1), True, (255, 255, 255))
        screen.blit(place, ((window_width / 2) - 30, 640))
        save+= 1
    time+=1
    all_sprites_list.draw(screen)
    creationTime-=1
    pygame.display.flip()
    pygame.display.update()
    clock.tick(FPS)

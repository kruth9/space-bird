import random 
import sys
import pygame
from pygame.locals import*

#global vaiables for the games

FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SC = {}
GAME_SOUND = {}
PLAYER = 'gallery/sprites/bird.png'
BACKGROUND = 'gallery/sprites/background.png'
PIPE = 'gallery/sprites/pipe.png'


def welcomeScreen():

    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SC['player'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_SC['message'].get_width())/2)
    messagey = int(SCREENHEIGHT*0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            #if user click click on cross close thy game
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            
            # if user press space or up key,start
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SC['background'], (0, 0))
                SCREEN.blit(GAME_SC['player'], (playerx, playery))
                SCREEN.blit(GAME_SC['message'], (messagex, messagey))
                SCREEN.blit(GAME_SC['base'], (basex, GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def maingame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0 

    # pipes blit
    newpipe1 = getRandomPipe()
    newpipe2 = getRandomPipe()

    #upper pipe lsit
    upperPipes = [
        {'x':SCREENWIDTH + 200, 'y':newpipe1[0]['y']},
        {'x':SCREENWIDTH + 200 + (SCREENWIDTH/2) , 'y':newpipe2[0]['y']},
    ]

    #lower pipes
    lowerPipes = [
        {'x':SCREENWIDTH + 200, 'y':newpipe1[1]['y']},
        {'x':SCREENWIDTH + 200 + (SCREENWIDTH/2) , 'y':newpipe2[1]['y']},
    ]

    pipeVelocityX = -4

    playerVelocityY = -9
    playerMaxVelocityY =10
    playerMinVelocityY = -8
    playerAccY = 1

    playerFlapVelocity = -8 #vel while flap
    playerFlapped = False #only tru when bird flaps

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelocityY = playerFlapVelocity
                    playerFlapped = True
                    GAME_SOUND['wing'].play()
        

        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)#func when plyer crashes into a pole
        if crashTest:
            return
        
        #score
        playerMidPos = playerx + GAME_SC['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SC['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos +4:
                score = score + 1
                print(f"your score is {score}")
                GAME_SOUND['point'].play()

        if playerVelocityY < playerMaxVelocityY and not playerFlapped:
            playerVelocityY += playerAccY

        if playerFlapped:
            playerFlapped = False
        playerHeight = GAME_SC['player'].get_height()
        playery = playery + min(playerVelocityY, GROUNDY - playery - playerHeight)# logic so that the player wont go below ground

        #move pipe left
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelocityX
            lowerPipe['x'] += pipeVelocityX
        
        # new pipe when prepious pipe is gonna left screen in left side
        if 0<upperPipes[0]['x']<5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        #remove screen out pipes
        if upperPipes[0]['x'] < -GAME_SC['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        #images aka sprites in screen 
        SCREEN.blit(GAME_SC['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SC['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SC['pipe'][1], (lowerPipe['x'], lowerPipe['y']))
            
        SCREEN.blit(GAME_SC['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SC['player'], (playerx, playery))
        mydigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in mydigits:
            width += GAME_SC['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in mydigits:
            SCREEN.blit(GAME_SC['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SC['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery> GROUNDY -25 or playery < 0:
        GAME_SOUND['hit'].play()
        return True

    for pipe in upperPipes:
        pipeHeight = GAME_SC['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and (abs(playerx - pipe['x']) < GAME_SC['pipe'][0].get_width())):
            GAME_SOUND['hit'].play()
            return True
    
    for pipe in lowerPipes:
        if (playery + GAME_SC['player'].get_height() > pipe['y']) and (abs(playerx - pipe['x']) < GAME_SC['pipe'][0].get_width()):
            GAME_SOUND['hit'].play()
            return True


def getRandomPipe():
    # logic for two pipes
    pipeHeight = GAME_SC['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SC['base'].get_height() - 1.2 *offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x':pipeX, 'y':-y1},# upper pipe
        {'x':pipeX, 'y': y2} #lower
    ]
    return pipe

if __name__ == "__main__":
    # GAME START
    pygame.init()#intilazie all pygame modules
    FPSCLOCK = pygame.time.Clock()#fps control
    pygame.display.set_caption('SPACE BIRD')
    GAME_SC['numbers'] = (
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),
    )

    
    GAME_SC['message'] = pygame.image.load('gallery/sprites/message.png').convert_alpha()
    GAME_SC['base'] = pygame.image.load('gallery/sprites/base.png').convert_alpha()

    GAME_SC['pipe'] = (
    pygame.transform.rotate(pygame.image.load( PIPE ).convert_alpha(), 180),
    pygame.image.load( PIPE ).convert_alpha()
    )


    #  GAME SOUND
    GAME_SOUND['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUND['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUND['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUND['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')
    GAME_SOUND['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')

    GAME_SC['background'] = pygame.image.load( BACKGROUND ).convert()
    GAME_SC['player'] = pygame.image.load( PLAYER ).convert_alpha()

    while True:
        welcomeScreen() #start screen show
        maingame() #main g func to start 
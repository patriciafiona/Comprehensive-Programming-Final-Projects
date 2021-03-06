# For generating random height of pipes
import random  
from threading import Timer
import sys 
import pygame
from pygame.locals import * 
from enum import Enum 
  
# Global Variables for the game
window_width = 300
window_height = 600
framepersecond = 60
app_name = "Flappy Bird"
flappy_x_pos = 100
gap = 180
pipeVelX = -4 #pipe velocity along x

# List containing lower pipes
down_pipes = []
  
# List Containing upper pipes
up_pipes = []

vertical = int(window_width/2)

black = (0,0,0)
white = (255,255,255)

class GameState(Enum):
    loby = 1
    waiting = 2
    started = 3
    gameover = 4

isFirstTime = True
isMusicPlaying = True

# set height and width of window
window = pygame.display.set_mode((window_width, window_height))   
elevation = window_height * 2

textures = {
    'flappy': [pygame.image.load("./resources/images/flappy1.png").convert_alpha(),
               pygame.image.load("./resources/images/flappy2.png").convert_alpha(),
               pygame.image.load("./resources/images/flappy3.png").convert_alpha()],
    'background': pygame.image.load("./resources/images/background.png").convert_alpha(),
    'logo': pygame.image.load("./resources/images/logo.png").convert_alpha(),
    'start_btn': pygame.image.load("./resources/images/start.png").convert_alpha(),
    'getReady': pygame.image.load("./resources/images/getReady.png").convert_alpha(),
    'gameover': pygame.image.load("./resources/images/gameover.png").convert_alpha(),
    }

Game = {
	'score': 0,
	'highscore': 0,
	'frames': 0,
	'pressC': 'Press C to continue',
	'highscoreText': 'Best Score: ',
	'gameState': GameState.loby
    }

Flappy = {
    'v': window_height / 2, # Velocity
    'isFlap': False,
	'frame': 0,
	'sprite': textures['flappy'][0],
	}

game_images = {}
game_images['pipeimage'] = (
    pygame.transform.rotate(pygame.image.load("./resources/images/pipe.png").convert_alpha(), 180), 
    pygame.image.load("./resources/images/pipe.png").convert_alpha()
    )


# -------------------------------------------------------------------------------------
# Event Listener Start
def eventListener():
    global vertical 
    global down_pipes
    global up_pipes

    for event in pygame.event.get():
        # if user clicks on cross button, close the game
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit(0)
        elif Game['gameState'] == GameState.loby and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Set the x, y postions of the mouse click
            x, y = event.pos
            btn_start_pos = textures['start_btn'].get_rect()
            btn_start_pos = btn_start_pos.move(100, 320) # Position of the button
            if btn_start_pos.collidepoint(x, y):
                pygame.mixer.music.stop()
                Game['gameState'] = GameState.waiting
                waiting_screen()
        elif (event.type == KEYDOWN and event.key == K_SPACE):
            if (Game['gameState'] == GameState.waiting):
                Game['gameState'] = GameState.started

            if (Game['gameState'] == GameState.started):
                if vertical > 0:
                    Flappy['v'] = -8
                    Flappy['isFlap'] = True

				    #Play sound hop
                    pygame.mixer.init()
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("./resources/audio/flap.wav"), maxtime=1000)

			    # restart
        elif (Game['gameState'] == GameState.gameover and event.type == KEYDOWN and event.key == K_c):
            Game['gameState'] = GameState.loby
            
            # set to begin value
            Game['score'] = 0
            down_pipes = []
            up_pipes = []
            vertical = int(window_width/2)

            # show loading screen
            loading_screen()

        else:
            # Just Refresh the screen
            pygame.display.update()        
                      
            # set the rate of frame per second
            framepersecond_clock.tick(framepersecond)
# Event Listener End
# -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
# Loading Screen Method Start
def loading_screen():
    pygame.mixer.init()
    pygame.mixer.music.load("./resources/audio/themesong.wav")
    pygame.mixer.music.play(loops = -1)

    textures['background'] = pygame.transform.scale(textures['background'], (window_width + window_width * .2, window_height + window_height * .2))
    window.blit(textures['background'], (0, 0))

    textures['logo'] = pygame.transform.scale(textures['logo'], (200, 50))
    window.blit(textures['logo'], (50, 250))

    textures['start_btn'] = pygame.transform.scale(textures['start_btn'], (100, 40))
    window.blit(textures['start_btn'], (100, 320))
# Loading Screen Method End
# -------------------------------------------------------------------------------------

def updateToWaiting(firstTime: str):
    global isFirstTime
    Game['gameState'] = GameState.waiting
    if firstTime == "True":
        isFirstTime = False

# -------------------------------------------------------------------------------------
# Waiting Screen Method Start
def waiting_screen():
    window.fill(black)

    textures['background'] = pygame.transform.scale(textures['background'], (window_width + window_width * .2, window_height + window_height * .2))
    window.blit(textures['background'], (0, 0))

    textures['getReady'] = pygame.transform.scale(textures['getReady'], (250, 250))
    window.blit(textures['getReady'], (20, 150))

    if isFirstTime == True:
        t = Timer(2, updateToWaiting, args=("True",))  
        t.start()

# Waiting Screen Method End
# -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
# Create Pipe Method Start
def createPipe(r, gap):
    global window_height
    global window_width

    pipe = [
        # upper Pipe
        {'x': window_width, 'y': r - gap * 2},
  
        # lower Pipe
        {'x': window_width, 'y': r + gap}
    ]
    return pipe

# -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
# check isGameOver start
def isGameOver(horizontal, vertical, up_pipes, down_pipes):
    if vertical > elevation - 25 or vertical < 0:
        return True
  
    for pipe in up_pipes:
        pipeHeight = game_images['pipeimage'][0].get_height() + game_images['pipeimage'][0].get_height() * 0.2
        if(vertical < pipeHeight + pipe['y'] and abs(horizontal - pipe['x']) < game_images['pipeimage'][0].get_width()):
            return True
  
    for pipe in down_pipes:
        if (vertical + Flappy['sprite'].get_height() > pipe['y']) and abs(horizontal - pipe['x']) < game_images['pipeimage'][0].get_width():
            return True
    return False
# check isGameOver end
# -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
# updateGameComponent method Start
def updateGameComponent():
    global isFirstTime
    global gap
    global pipeVelX
    global vertical
    global elevation
    global down_pipes
    global up_pipes

    
    window.fill(black)

    textures['background'] = pygame.transform.scale(textures['background'], (window_width, window_height))

    Flappy['sprite'] = textures['flappy'][1]

    pygame.font.init() # you have to call this at the start, 
    scoreFont = pygame.font.Font("./resources/fonts/flappy.ttf", 75)
    score_txt = scoreFont.render(str(Game['score']), False, white)

    bestScoreFont = pygame.font.Font("./resources/fonts/flappy.ttf", 20)
    best_score_txt = bestScoreFont.render("Best Score: " + str(Game['highscore']), False, white)

    # Update flappy
    flappy_sprite = Flappy['sprite'].get_rect().move(flappy_x_pos, vertical)
    fx = flappy_sprite.x
    fy = flappy_sprite.y

    # Flap the wings if playing
    if Game['gameState'] == GameState.waiting or Game['gameState'] == GameState.started:
		# change the texture once in 6 frames
        if(Game['frames'] % 6 == 0):
            Flappy['frame'] =  Flappy['frame'] + 1

        if (Flappy['frame'] == 3):
            Flappy['frame'] = 0

    Flappy['sprite'] = textures['flappy'][Flappy['frame']]

    # Move flappy
    if Game['gameState'] == GameState.started: 
        if Flappy['v'] < 10 and not Flappy['isFlap']:
            Flappy['v'] += 0.5

        # collision detection
        if isGameOver(flappy_x_pos,vertical, up_pipes, down_pipes):
            Game['gameState'] = GameState.gameover

            #Play sound dishk
            pygame.mixer.init()
            pygame.mixer.Channel(0).play(pygame.mixer.Sound("./resources/audio/crash.wav"), maxtime=1000)

        # if hits ceiling, stop ascending
        # if out of screen, game over
        if (fy < 0):
            Flappy['v'] = 0
        elif (fy > window_height):
            Flappy['v'] = 0
            Game['gameState'] = GameState.gameover

            #Play sound dishk
            pygame.mixer.init()
            pygame.mixer.Channel(0).play(pygame.mixer.Sound("./resources/audio/crash.wav"), maxtime=1000)

    if Flappy['isFlap']: 
        Flappy['isFlap'] = False

    if Game['gameState'] == GameState.started: 
        # update vertical value - bird y position
        vertical = vertical + min(Flappy['v'], elevation - vertical - fy)
    elif Game['gameState'] == GameState.waiting:
        vertical = window_height / 2

    # check for your_score
    if Game['gameState'] == GameState.started: 
        for pipe in up_pipes:
            pipeMidPos = pipe['x'] + game_images['pipeimage'][0].get_width()/2
            if pipeMidPos <= fx < pipeMidPos + 4:
                Game['score'] = Game['score'] + 1

                if (Game['score'] > Game['highscore']):
                    Game['highscore'] = Game['score']

                #Play sound score
                pygame.mixer.init()
                pygame.mixer.Channel(0).play(pygame.mixer.Sound("./resources/audio/score.wav"), maxtime=1000)
                
        # move pipes to the left
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
            upperPipe['x'] = upperPipe['x'] + pipeVelX
            lowerPipe['x'] = lowerPipe['x'] + pipeVelX
  
        # Add a new pipe when the first is
        # about to cross the leftmost part of the screen
        if (Game['frames'] % 60 == 0):
            r = random.randint(0, window_height/2) % (window_height/2) + 75

            newpipe = createPipe(r, gap)
            up_pipes.append(newpipe[0])
            down_pipes.append(newpipe[1])
  
        # if the pipe is out of the screen, remove it
        if len(up_pipes) > 0 and len(down_pipes) > 0:
            if up_pipes[0]['x'] < -game_images['pipeimage'][0].get_width():
                up_pipes.pop(0)
                down_pipes.pop(0)


    #display all component
    window.blit(textures['background'], (0, 0))
        
    if (Game['gameState'] == GameState.started):
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
            pipeScale01 = pygame.transform.scale(game_images['pipeimage'][0], (game_images['pipeimage'][0].get_width(), 
                                                                                game_images['pipeimage'][0].get_height() + 
                                                                                game_images['pipeimage'][0].get_height() * 0.2))
            window.blit(pipeScale01,
                        (upperPipe['x'] ,upperPipe['y']))

            pipeScale02 = pygame.transform.scale(game_images['pipeimage'][1], (game_images['pipeimage'][1].get_width(), 
                                                                                game_images['pipeimage'][1].get_height() + 
                                                                                game_images['pipeimage'][1].get_height() * 0.2))
            window.blit(pipeScale02,
                        (lowerPipe['x'], lowerPipe['y']))

    window.blit(score_txt,(10,10))
    window.blit(best_score_txt,(10,80))

    bird = pygame.transform.scale(Flappy['sprite'], (Flappy['sprite'].get_width() + 
                                                        Flappy['sprite'].get_width() * 0.2, 
                                                                                Flappy['sprite'].get_height() + 
                                                                                Flappy['sprite'].get_height() * 0.2))

    window.blit(bird,(flappy_x_pos, vertical))   

    if Game['gameState'] == GameState.gameover:
        # Show Game Over
        updateGameOverScreen()

    # dont forget to update total frames
    Game['frames'] += 1;

    # Just Refresh the screen
    pygame.display.update()        
                      
    # set the rate of frame per second
    framepersecond_clock.tick(framepersecond)

# updateGameComponent method End
# -------------------------------------------------------------------------------------

def updateGameOverScreen():
    window.fill(black)
    textures['background'] = pygame.transform.scale(textures['background'], (window_width, window_height))
    textures['gameover'] = pygame.transform.scale(textures['gameover'], (150, 30))

    font = pygame.font.Font("./resources/fonts/flappy.ttf", 20)
    pressC_text = font.render("Press C to continue", False, white)

    window.blit(textures['background'], (0, 0))
    window.blit(textures['gameover'], (80, 285))
    if (Game['frames'] % 60 < 30):
        window.blit(pressC_text,(50, 325))

# -------------------------------------------------------------------------------------
# Main Program Start
if __name__ == "__main__":
    pygame.init()  

    # Sets the title on top of game window
    pygame.display.set_caption('Flappy Bird')    
    
    # Set program icon
    pygame.display.set_icon(textures['flappy'][0])

    framepersecond_clock = pygame.time.Clock()

    loading_screen()

    while True:
        pygame.init()

        # Event listener
        eventListener()

        if Game['gameState'] != GameState.loby:
            if isFirstTime == False:
                updateGameComponent()

# Main Program End
# -------------------------------------------------------------------------------------

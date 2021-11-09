# For generating random height of pipes
import random  
import sys 
import pygame
from pygame.locals import * 
from enum import Enum 
  
# Global Variables for the game
window_width = 300
window_height = 600
framepersecond = 60
app_name = "Flappy Bird"

black = (0,0,0)

class GameState(Enum):
    loby = 1
    waiting = 2
    started = 3
    gameover = 4

isFirstTime = True
isMusicPlaying = True

# set height and width of window
window = pygame.display.set_mode((window_width, window_height))   
elevation = window_height * 0.8

textures = {
    'flappy': [pygame.image.load("./resources/images/flappy1.png").convert_alpha(),
               pygame.image.load("./resources/images/flappy2.png").convert_alpha(),
               pygame.image.load("./resources/images/flappy3.png").convert_alpha()],
    'pipe': pygame.image.load("./resources/images/pipe.png").convert_alpha(),
    'background': pygame.image.load("./resources/images/background.png").convert_alpha(),
    'logo': pygame.image.load("./resources/images/logo.png").convert_alpha(),
    'start_btn': pygame.image.load("./resources/images/start.png").convert_alpha(),
    'getReady': pygame.image.load("./resources/images/getReady.png").convert_alpha(),
    'gameover': pygame.image.load("./resources/images/gameover.png").convert_alpha(),
    'ground': pygame.image.load("./resources/images/ground.png").convert_alpha(),
    }

Game = {
	'score': 0,
	'highscore': 0,
	'frames': 0,
	'pressC': 'Press C to continue',
	'highscoreText': 'Best Score: ',
	'gameState': GameState.loby
    }

# -------------------------------------------------------------------------------------
# Event Listener Start
def eventListener():
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
                print("Go to Waiting Room")
                pygame.mixer.music.stop()
                Game['gameState'] = GameState.waiting
                waiting_screen()
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
    pygame.mixer.music.load("./resources/audio/themesong.wav")
    pygame.mixer.music.play(loops = -1)

    textures['background'] = pygame.transform.scale(textures['background'], (window_width, window_height))
    window.blit(textures['background'], (0, 0))

    textures['ground'] = pygame.transform.scale(textures['ground'], (window_width, 30))
    window.blit(textures['ground'], (0, window_height-30))

    textures['logo'] = pygame.transform.scale(textures['logo'], (200, 50))
    window.blit(textures['logo'], (50, 250))

    textures['start_btn'] = pygame.transform.scale(textures['start_btn'], (100, 40))
    window.blit(textures['start_btn'], (100, 320))
# Loading Screen Method End
# -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
# Waiting Screen Method Start
def waiting_screen():
    window.fill(black)

    textures['background'] = pygame.transform.scale(textures['background'], (window_width, window_height))
    window.blit(textures['background'], (0, 0))

    textures['ground'] = pygame.transform.scale(textures['ground'], (window_width, 30))
    window.blit(textures['ground'], (0, window_height-30))

    textures['getReady'] = pygame.transform.scale(textures['getReady'], (200, 230))
    window.blit(textures['getReady'], (50, 170))
# Waiting Screen Method End
# -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
# Main Program Start
if __name__ == "__main__":
    pygame.init()  
    pygame.mixer.init()

    # Sets the title on top of game window
    pygame.display.set_caption('Flappy Bird')      

    framepersecond_clock = pygame.time.Clock()

    loading_screen()

    while True:
        while True:
            pygame.init()
            # Event listener
            eventListener()
# Main Program End
# -------------------------------------------------------------------------------------

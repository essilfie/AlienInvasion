import sys 
import pygame

def run_game():
    '''Sets the screen and runs the simple game.'''

    # Initialize the screen
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption('Exercise')

    bg_color = (200, 200, 200)

    while True:
        # Fill the background color
        screen.fill(bg_color)

        # Watch for mouse and keyboard events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            elif event.type == pygame.KEYDOWN:
                print(event.key)

        pygame.display.flip()





run_game()
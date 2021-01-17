''' To start our game, we first create and empty Pygame window'''

import sys 
import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from alien import Alien
import game_functions as gf


def run_game():
    # Initialize game and crate a screen sobject.

    ai_settings = Settings()
    pygame.init()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Make the Play button
    play_button = Button(ai_settings, screen, "Play")

    # Create an instance to store game statistics and create a scoreboard.
    stats = GameStats(ai_settings)
    sb =Scoreboard(ai_settings, screen, stats)

    # Make a ship, a group of bullets, and a group of aliens
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()

    # Create a fleet of aliens.
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Start the main loop for the game.
    while True:

        # Watch for keyboard and mouse event.
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)

        if stats.game_active:
            ship.update() # this allows the ship's movement to be seen.

            # Updates the bullet position and deletes old bullets  
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)

            # Update the aliens moving on the screen
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)

        # Redraw the screen during each passs through the loop.
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)

        # Make the most recently drawn screen visible.
        pygame.display.flip()

run_game()
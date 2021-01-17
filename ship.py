import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    '''We will be adding the ship image in this file'''

    def __init__(self, ai_settings, screen):
        '''Initialize the ship and sets its starting position.'''
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the ship image and get its rect or rectangle, which will be used to adjust the positioning of the ship.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        #self.rect.centery = self.screen_rect.centery. this puts an image to the center of the screen.

        # Store a decimal value for the ship's center.
        self.center = float(self.rect.centerx)

        # Movement flag
        self.moving_right = False
        self.moving_left = False

    def update(self):
        '''Update the ship's position based on the movement flag.'''
        
        # For movement to the right side
        # Updating the ship's center value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor

        # For movement to the left side
        if self.moving_left and self.rect.left > 0: 
            self.center -= self.ai_settings.ship_speed_factor

        # Update rect object from self.center.
        self.rect.centerx = self.center

    def blitme(self):
        '''Draw the ship at its current location.'''
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        '''Center the ship on the screeen.'''
        self.center = self.screen_rect.centerx

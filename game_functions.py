import sys
from time import sleep

import pygame

from bullet import Bullet
from alien import Alien


def get_number_rows(ai_settings, ship_height, alien_height):
    '''Determine the number of rows of aliens that fit on the screen.'''
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def get_number_aliens_x(ai_settings, alien_width):
    '''Determine the number of aliens that fit in a row.'''
    available_space_x = ai_settings.screen_width - (2 * alien_width)
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    '''Create an alien and place it in the row.'''
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    '''Create a full fleet of aliens.'''
    # Create an alien and find the number of aliens in a row.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # Create the fleet of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)        


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    '''Respond to key presses.'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        # Create a new bullet and add it to the bullets group.
        fire_bullets(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def fire_bullets(ai_settings, screen, ship, bullets):
    '''Fire a bullet if limit is not reached yet.'''
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def check_keyup_events(event, ship):
    '''Responds to keypresses.'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    '''Responds to keypress and mouse events.'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        # Checks the flag for when a key is pressed down
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
           
        # Sets the flag back to false when the key is released
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos() # this restricts the game to only when the player click on the play button
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    '''Start a new game when the player clicks Play.'''
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings.
        ai_settings.initialize_dynamic_settings()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

        # Reset the game statistics.
        stats.reset_stats()
        stats.game_active = True

        # Reset the scoreboard image.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''Update position of bullets and get rid of old bullets.'''
    # Update bullet positions.
    bullets.update()

    # Get ride of bullets that have disappeared.
    for bullet in bullets.copy():  # We use a copy here because it's bad to remove items from a list or gprup within a for loop
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)   

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)  

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''Responds to bullet-alien collisions'''
    # Check for any bullet that have hit aliens.
    # If so, get rid of the bullets and the alien.
    collisions= pygame.sprite.groupcollide(bullets, aliens, True, True)   
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()  
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # If the entire fleet is destroyed. Start a new level
        bullets.empty()
        ai_settings.increase_speed()

        # Increase level.
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)  

def update_screen(ai_asettings, screen, stats, sb, ship, aliens, bullets, play_button):
    '''Update images on the screen and flip to the new screen.''' 
    # Redraw the screen during each pass through the loop
    screen.fill(ai_asettings.bg_color)      
    
    # Redraw all bullets behind ships and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen) # this function draws each alien in the group to the screen.

    # Draw the scoreboard information.
    sb.show_score()

    # Draw the play button if the game is inactive.
    if not stats.game_active:
        play_button.draw_button()

    # Make the most recently drawn screen visible.
    pygame.display.flip()

def check_fleet_edges(ai_settings, aliens):
    '''Respond appropriately if any aliens have reached an edge.'''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    '''Drop the entire fleet and change the fleet's direction.'''
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''Responds to ship being hit by alien.'''
    if stats.ships_left > 0:
        # Decrement ships left.
        stats.ships_left -= 1

        # Update the scoreboard.
        sb.prep_ships()

        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottoms(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''Check if any alien have reached the bottom of the screen.'''
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break

def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''Check if the fleet is at an edge, 
    and then update the positions of all aliens in the fleet.'''
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens): # The method spritecollideany() takes two arguments, a sprite and a group 
                                                    # The method looks for any member of the group that's collided with the sprite
                                                    # and stops  looping through the group.
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottoms(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_high_score(stats, sb):
    '''Check to see if there's a new high score.'''
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
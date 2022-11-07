import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """Class for controlling resources and game logic"""

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Alien Invasion")

        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        self.stats = GameStats(self)
        self.scoreboard = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        # Buttons
        self.play_button = Button(self, "Play")
        self._make_difficulty_buttons()

    def _make_difficulty_buttons(self):
        # Difficulty buttons
        self.easy_button = Button(self, "Soyjack")
        self.medium_button = Button(self, "Normie")
        self.hard_button = Button(self, "Dark Souls")

        self.easy_button.rect.left -= self.easy_button.widht * 1.2
        self.hard_button.rect.left += self.hard_button.widht * 1.2

        self.easy_button.update_msg_position()
        self.hard_button.update_msg_position()

    def run_game(self):
        """Main game loop"""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        """Respond to keypresses and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stats.save_high_score()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_button(mouse_pos)

    def _check_button(self, mouse_pos):
        """Starts the game when play button is pressed"""
        play_button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        easy_button_clicked = self.easy_button.rect.collidepoint(mouse_pos)
        medium_button_clicked = self.medium_button.rect.collidepoint(mouse_pos)
        hard_button_clicked = self.hard_button.rect.collidepoint(mouse_pos)

        if self.stats.play_screen and play_button_clicked:
            self.stats.play_screen = False
            self.stats.difficulty_select = True

        elif self.stats.difficulty_select:
            if easy_button_clicked:
                self._set_mode("easy")
            elif medium_button_clicked:
                self._set_mode("medium")
            elif hard_button_clicked:
                self._set_mode("hard")

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p and self.stats.play_screen:
            self.stats.play_screen = False
            self.stats.difficulty_select = True
        elif event.key == pygame.K_u:
            self._end_game()
        elif event.key == pygame.K_q:
            self.stats.save_high_score()
            sys.exit()

        if self.stats.difficulty_select:
            if event.key == pygame.K_e:
                self._set_mode("easy")
            elif event.key == pygame.K_m:
                self._set_mode("medium")
            elif event.key == pygame.K_h:
                self._set_mode("hard")

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = False

    def _update_screen(self):
        """Updates images and redraws them on the screen"""
        self.screen.fill(self.settings.bg_color)

        # Only when game is active
        if self.stats.game_active:
            self.ship.blitme()
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.aliens.draw(self.screen)
            self.scoreboard.show_score()

        # Draw play button before and after the game
        if self.stats.play_screen:
            self.play_button.draw_button()
        elif self.stats.difficulty_select:
            self._draw_difficulty_buttons()

        pygame.display.flip()

    def _update_bullets(self):
        """Update position of bullets and delete old bullets"""
        self.bullets.update()

        # Delete old bullets
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collision()

    def _check_bullet_alien_collision(self):
        """Respond to bullet alien collisions"""

        # Check for collisions
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, not self.settings.super_bullet, True
        )
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.scoreboard.prep_score()
            self.scoreboard.check_high_score()

        # Create new fleet if old one is destroyed
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.scoreboard.prep_level()

    def _fire_bullet(self):
        """Create new bullet and add it to bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _create_fleet(self):
        """Create a fleet of aliens"""

        # Calculate number of aliens in a row
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (6 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width) + 1

        # Calculate number of rows
        ship_height = self.ship.rect.height
        available_space_y = (
            self.settings.screen_height - (4 * alien_height) - ship_height
        )
        number_rows = available_space_y // (2 * alien_height)

        # Create alien matrix
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number, alien_width, alien_height)

    def _check_fleet_edges(self):
        """Changes direction of a fleet if fleet has reached the edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Moves the fleet down and changes direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_aliens_bottom(self):
        """Checks if any aliens have reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _create_alien(self, alien_number, row_number, alien_width, alien_height):
        alien = Alien(self)
        alien.x = alien_width * 3 + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.y = alien_height * 2 + 2 * alien_height * row_number
        alien.rect.y = alien.y
        self.aliens.add(alien)

    def _update_aliens(self):
        """
        Checks if the fleet has reached the edge,
        then updates the positions of all aliens in the fleet
        """
        self._check_fleet_edges()
        self.aliens.update()

        # Check for collision with a ship
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_aliens_bottom()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien"""
        # Decrement ships left
        self.stats.ships_left -= 1
        self.scoreboard.prep_ships()

        if self.stats.ships_left > 0:
            self._reset_game()
            # Pause
            sleep(1)
        else:
            self._end_game()

    def _draw_difficulty_buttons(self):
        self.easy_button.draw_button()
        self.medium_button.draw_button()
        self.hard_button.draw_button()

    def _set_mode(self, mode):
        self.settings.difficulty = mode
        self.stats.difficulty_select = False
        self._start_new_game()

    def _reset_game(self):
        """Resets game state"""
        # Clear remaining aliens and bullets
        self.aliens.empty()
        self.bullets.empty()

        # Create a new fleet and center the ship
        self._create_fleet()
        self.ship.center_ship()

    def _start_new_game(self):
        # Reset
        self._reset_game()
        self.stats.reset_stats()
        self.scoreboard.prep_score()
        self.scoreboard.prep_level()
        self.scoreboard.prep_ships()
        self.settings.initialize_dynamic_settings()

        self.stats.game_active = True

        # Hide mouse pointer
        pygame.mouse.set_visible(False)

    def _end_game(self):
        self.stats.game_active = False
        self.stats.play_screen = True
        pygame.mouse.set_visible(True)


if __name__ == "__main__":
    # Starting a game
    game = AlienInvasion()
    game.run_game()

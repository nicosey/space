import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Player
player_width = 50
player_height = 40
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 10
player_speed = 5

# Bullets
bullet_width = 5
bullet_height = 15
bullets = []
bullet_speed = 7

# Aliens
alien_width = 50
alien_height = 50
aliens = []
alien_speed = 1

# Game state
game_over = False
bullets_fired = 0
initial_alien_count = 25  # 5x5 grid of aliens
aliens_destroyed = 0
font = pygame.font.Font(None, 36)

# Create initial aliens
for i in range(5):
    for j in range(5):
        alien = {
            'x': i * (alien_width + 20) + 50,
            'y': j * (alien_height + 20) + 50,
            'width': alien_width,
            'height': alien_height
        }
        aliens.append(alien)

def draw_alien(screen, alien):
    alien_color = (0, 255, 0)  # Green
    points = [
        (alien['x'], alien['y'] + alien['height']),
        (alien['x'] + alien['width'] // 2, alien['y']),
        (alien['x'] + alien['width'], alien['y'] + alien['height']),
        (alien['x'] + alien['width'] - 10, alien['y'] + alien['height'] - 15),
        (alien['x'] + 10, alien['y'] + alien['height'] - 15)
    ]
    pygame.draw.polygon(screen, alien_color, points)
    
    # Alien eyes
    eye_color = (255, 255, 255)  # White
    eye_size = 5
    eye_x = alien['x'] + alien['width'] // 2 - eye_size // 2
    eye_y = alien['y'] + alien['height'] // 2 - eye_size // 2
    pygame.draw.ellipse(screen, eye_color, (eye_x, eye_y, eye_size, eye_size))

def draw_player(screen, x, y):
    # Main body
    pygame.draw.polygon(screen, WHITE, [
        (x + player_width // 2, y),
        (x, y + player_height),
        (x + player_width, y + player_height)
    ])
    # Cockpit
    pygame.draw.polygon(screen, (100, 100, 100), [
        (x + player_width // 2, y + 10),
        (x + player_width // 2 - 10, y + 25),
        (x + player_width // 2 + 10, y + 25)
    ])
    # Left wing
    pygame.draw.polygon(screen, WHITE, [
        (x, y + player_height),
        (x - 10, y + player_height + 5),
        (x + 15, y + player_height - 5)
    ])
    # Right wing
    pygame.draw.polygon(screen, WHITE, [
        (x + player_width, y + player_height),
        (x + player_width + 10, y + player_height + 5),
        (x + player_width - 15, y + player_height - 5)
    ])

def draw_bullet_counter():
    counter_text = font.render(f"Bullets: {bullets_fired}", True, WHITE)
    screen.blit(counter_text, (10, 10))

def draw_game_over_screen():
    screen.fill(BLACK)
    game_over_text = font.render("Game Over!", True, WHITE)
    restart_text = font.render("Restart", True, WHITE)
    quit_text = font.render("Quit", True, WHITE)
    
    # Ensure aliens_destroyed doesn't exceed initial_alien_count
    displayed_aliens_destroyed = min(aliens_destroyed, initial_alien_count)
    stats_text = font.render(f"Bullets Fired: {bullets_fired} | Aliens Destroyed: {displayed_aliens_destroyed}", True, WHITE)
    
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 150))
    screen.blit(stats_text, (WIDTH // 2 - stats_text.get_width() // 2, HEIGHT // 2 - 100))
    
    restart_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
    quit_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 70, 200, 50)
    
    pygame.draw.rect(screen, WHITE, restart_rect, 2)
    pygame.draw.rect(screen, WHITE, quit_rect, 2)
    
    screen.blit(restart_text, (restart_rect.centerx - restart_text.get_width() // 2, restart_rect.centery - restart_text.get_height() // 2))
    screen.blit(quit_text, (quit_rect.centerx - quit_text.get_width() // 2, quit_rect.centery - quit_text.get_height() // 2))
    
    return restart_rect, quit_rect

def reset_game():
    global player_x, player_y, bullets, aliens, game_over, bullets_fired, aliens_destroyed
    player_x = WIDTH // 2 - player_width // 2
    player_y = HEIGHT - player_height - 10
    bullets = []
    aliens = []
    for i in range(5):
        for j in range(5):
            alien = {
                'x': i * (alien_width + 20) + 50,
                'y': j * (alien_height + 20) + 50,
                'width': alien_width,
                'height': alien_height
            }
            aliens.append(alien)
    game_over = False
    bullets_fired = 0
    aliens_destroyed = 0  # Ensure this is reset to 0

# Game loop
clock = pygame.time.Clock()
running = True
restart_rect = None
quit_rect = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bullet = pygame.Rect(player_x + player_width // 2 - bullet_width // 2, 
                                     player_y, bullet_width, bullet_height)
                bullets.append(bullet)
                bullets_fired += 1
        if event.type == pygame.MOUSEBUTTONDOWN and game_over:
            mouse_pos = pygame.mouse.get_pos()
            if restart_rect and restart_rect.collidepoint(mouse_pos):
                reset_game()
            elif quit_rect and quit_rect.collidepoint(mouse_pos):
                running = False

    if not game_over:
        # Move player
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > -10:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width + 10:
            player_x += player_speed

        # Move bullets
        for bullet in bullets[:]:
            bullet.y -= bullet_speed
            if bullet.bottom < 0:
                bullets.remove(bullet)

        # Move aliens
        for alien in aliens:
            alien['x'] += alien_speed
            if alien['x'] <= 0 or alien['x'] + alien['width'] >= WIDTH:
                alien_speed = -alien_speed
                for a in aliens:
                    a['y'] += 10

        # Check for collisions
        for bullet in bullets[:]:
            bullet_rect = pygame.Rect(bullet.x, bullet.y, bullet.width, bullet.height)
            for alien in aliens[:]:
                alien_rect = pygame.Rect(alien['x'], alien['y'], alien['width'], alien['height'])
                if bullet_rect.colliderect(alien_rect):
                    bullets.remove(bullet)
                    aliens.remove(alien)
                    aliens_destroyed += 1
                    break

        # Ensure aliens_destroyed doesn't exceed initial_alien_count
        aliens_destroyed = min(aliens_destroyed, initial_alien_count)

        # Check if all aliens are destroyed
        if len(aliens) == 0:
            game_over = True

        # Draw everything
        screen.fill(BLACK)
        draw_player(screen, player_x, player_y)
        for bullet in bullets:
            pygame.draw.rect(screen, WHITE, bullet)
        for alien in aliens:
            draw_alien(screen, alien)
        draw_bullet_counter()
    else:
        restart_rect, quit_rect = draw_game_over_screen()

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()
sys.exit()
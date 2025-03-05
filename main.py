import pygame
import random

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Load images
background_img = pygame.image.load("background.jpg")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
ship_img = pygame.image.load("ship.png")
enemy_img = pygame.image.load("enemy.png")
bullet_img = pygame.image.load("bullet.png")
blast_img = pygame.image.load("blast.png")

# Resize images
ship_img = pygame.transform.scale(ship_img, (50, 50))
enemy_img = pygame.transform.scale(enemy_img, (50, 50))
bullet_img = pygame.transform.scale(bullet_img, (10, 20))
blast_img = pygame.transform.scale(blast_img, (50, 50))

# Load sounds
pygame.mixer.init()
shoot_sound = pygame.mixer.Sound("shoot.wav")
explosion_sound = pygame.mixer.Sound("explosion.mp3")
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)  # Loop the background music

# Ship settings
ship_x, ship_y = WIDTH // 2, HEIGHT - 80
ship_speed = 9
ship_health = 3

# Bullet settings
bullets = []
bullet_speed = 9
shoot_cooldown = 0

# Enemy settings
enemies = []
enemy_speed = 2
enemy_spawn_rate = 50  # Initial enemy spawn rate
frame_count = 0

# Score settings
score = 0
font = pygame.font.Font(None, 36)
game_over = False
blast_animations = []

# Main loop
running = True
while running:
    screen.blit(background_img, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            ship_x, ship_y = WIDTH // 2, HEIGHT - 80
            bullets.clear()
            enemies.clear()
            blast_animations.clear()
            score = 0
            ship_health = 3
            game_over = False
            frame_count = 0
            enemy_spawn_rate = 50
    
    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and ship_x > 0:
            ship_x -= ship_speed
        if keys[pygame.K_RIGHT] and ship_x < WIDTH - 50:
            ship_x += ship_speed
        if keys[pygame.K_SPACE] and shoot_cooldown == 0:
            bullets.append([ship_x + 20, ship_y])
            shoot_sound.play()
            shoot_cooldown = 10  # Cooldown to prevent rapid-fire abuse
    
        # Cooldown management
        if shoot_cooldown > 0:
            shoot_cooldown -= 1
    
        # Move bullets
        for bullet in bullets:
            bullet[1] -= bullet_speed
        bullets = [b for b in bullets if b[1] > 0]
    
        # Increase enemy spawn rate over time
        if frame_count % 500 == 0:
            enemy_spawn_rate = max(10, enemy_spawn_rate - 2)
    
        # Spawn enemies
        if frame_count % enemy_spawn_rate == 0:
            enemies.append([random.randint(0, WIDTH - 50), 0])
    
        # Move enemies
        for enemy in enemies:
            enemy[1] += enemy_speed
    
        # Check for collisions
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if (enemy[0] < bullet[0] < enemy[0] + 50) and (enemy[1] < bullet[1] < enemy[1] + 50):
                    enemies.remove(enemy)
                    bullets.remove(bullet)
                    explosion_sound.play()
                    blast_animations.append([enemy[0], enemy[1], 10])
                    score += 1
                    break
    
        # Check if enemy touches the ship or goes past it
        for enemy in enemies[:]:
            if (ship_x < enemy[0] + 50 and ship_x + 50 > enemy[0]) and (ship_y < enemy[1] + 50 and ship_y + 50 > enemy[1]):
                ship_health -= 1
                enemies.remove(enemy)
                explosion_sound.play()
                if ship_health <= 0:
                    game_over = True
                break
            if enemy[1] > HEIGHT:
                ship_health -= 1
                enemies.remove(enemy)
                if ship_health <= 0:
                    game_over = True
                break
    
    # Draw everything
    screen.blit(ship_img, (ship_x, ship_y))
    for bullet in bullets:
        screen.blit(bullet_img, (bullet[0], bullet[1]))
    for enemy in enemies:
        screen.blit(enemy_img, (enemy[0], enemy[1]))
    
    # Draw blast animations
    for blast in blast_animations[:]:
        screen.blit(blast_img, (blast[0], blast[1]))
        blast[2] -= 1
        if blast[2] <= 0:
            blast_animations.remove(blast)
    
    # Display score and health
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    health_text = font.render(f"Health: {ship_health}", True, RED)
    screen.blit(health_text, (10, 40))
    
    if game_over:
        game_over_text = font.render("Game Over! Press R to Restart", True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2))
    
    pygame.display.flip()
    frame_count += 1
    clock.tick(60)

pygame.quit()

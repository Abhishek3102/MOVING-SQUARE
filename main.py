import pygame
import sys
import random

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Exciting Pygame Example")

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

player_size = 50
player_x = screen_width // 2 - player_size // 2
player_y = screen_height // 2 - player_size // 2
player_speed = 6

enemy_size = 30
enemy_speed = 3
enemies = []

circle_radius = 15
circles = []

score = 0
font = pygame.font.Font(None, 36)

def spawn_enemy():
    x = random.randint(0, screen_width - enemy_size)
    y = random.randint(0, screen_height - enemy_size)
    direction = random.choice(["up", "down", "left", "right"])
    return {"x": x, "y": y, "direction": direction, "type": "square"}

def spawn_circle():
    x = random.randint(0, screen_width - circle_radius * 2)
    y = random.randint(0, screen_height - circle_radius * 2)
    return {"x": x, "y": y, "type": "circle"}

def draw_text(text, font, color, x, y):
    surface = font.render(text, True, color)
    rect = surface.get_rect()
    rect.midtop = (x, y)
    screen.blit(surface, rect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed

    if player_x < 0:
        player_x = 0
    elif player_x > screen_width - player_size:
        player_x = screen_width - player_size
    if player_y < 0:
        player_y = 0
    elif player_y > screen_height - player_size:
        player_y = screen_height - player_size

    if len(enemies) < 10:
        enemies.append(spawn_enemy())

    if len(circles) < 5:
        circles.append(spawn_circle())

    for enemy in enemies:
        if enemy["direction"] == "up":
            enemy["y"] -= enemy_speed
            if enemy["y"] < 0:
                enemy["direction"] = "down"
        elif enemy["direction"] == "down":
            enemy["y"] += enemy_speed
            if enemy["y"] > screen_height - enemy_size:
                enemy["direction"] = "up"
        elif enemy["direction"] == "left":
            enemy["x"] -= enemy_speed
            if enemy["x"] < 0:
                enemy["direction"] = "right"
        elif enemy["direction"] == "right":
            enemy["x"] += enemy_speed
            if enemy["x"] > screen_width - enemy_size:
                enemy["direction"] = "left"

    for circle in circles:
        circle["x"] += random.randint(-1, 1)
        circle["y"] += random.randint(-1, 1)

    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    for enemy in enemies:
        enemy_rect = pygame.Rect(enemy["x"], enemy["y"], enemy_size, enemy_size)
        if player_rect.colliderect(enemy_rect):
            if enemy["type"] == "square":
                enemies.remove(enemy)
                score -= 1

    for circle in circles:
        circle_rect = pygame.Rect(circle["x"], circle["y"], circle_radius * 2, circle_radius * 2)
        if player_rect.colliderect(circle_rect):
            circles.remove(circle)
            score += 1

    screen.fill(WHITE)

    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_size, player_size))

    for enemy in enemies:
        pygame.draw.rect(screen, RED, (enemy["x"], enemy["y"], enemy_size, enemy_size))

    for circle in circles:
        pygame.draw.circle(screen, GREEN, (circle["x"], circle["y"]), circle_radius)

    draw_text(f"Score: {score}", font, BLUE, screen_width // 2, 10)

    if player_x <= 0 or player_x >= screen_width - player_size or player_y <= 0 or player_y >= screen_height - player_size:
        print("Game Over! Your score:", score)
        pygame.quit()
        sys.exit()

    pygame.display.flip()

    pygame.time.Clock().tick(60)

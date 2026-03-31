import pygame
import random
import os

base_path = os.path.dirname(__file__)

pygame.init()
pygame.mixer.init()

# Screen
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Game")

# Load images
car_img = pygame.image.load(os.path.join(base_path, "images", "car.png"))
coin_img = pygame.image.load(os.path.join(base_path, "images", "coin.jpg"))
enemy_img = pygame.image.load(os.path.join(base_path, "images", "enemy.png"))
bomb_img = pygame.image.load(os.path.join(base_path, "images", "bomb.png"))
bg_img = pygame.image.load(os.path.join(base_path, "images", "bg.jpg"))

car_img = pygame.transform.scale(car_img, (50, 80))
coin_img = pygame.transform.scale(coin_img, (30, 30))
enemy_img = pygame.transform.scale(enemy_img, (50, 80))
bomb_img = pygame.transform.scale(bomb_img, (40, 40))
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))

# Sounds 🔊

import os

coin_sound = pygame.mixer.Sound(os.path.join(base_path, "assets", "sounds", "coin.wav"))
bomb_sound = pygame.mixer.Sound(os.path.join(base_path, "assets", "sounds", "bomb.wav"))
gameover_sound = pygame.mixer.Sound(os.path.join(base_path, "assets","sounds", "gameover.wav"))

# Background
bg_y1 = 0
bg_y2 = -HEIGHT

# Car
car = pygame.Rect(175, 500, 50, 80)

# Variables
score = 0
speed = 5
game_over = False

font = pygame.font.SysFont(None, 30)
big_font = pygame.font.SysFont(None, 60)

# Lists
enemies = []
coins = []
bombs = []

clock = pygame.time.Clock()

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def reset_game():
    global score, speed, enemies, coins, bombs, game_over
    score = 0
    speed = 5
    enemies.clear()
    coins.clear()
    bombs.clear()
    game_over = False
    car.x = 175

while True:

    # Background movement
    bg_y1 += speed
    bg_y2 += speed

    if bg_y1 >= HEIGHT:
        bg_y1 = -HEIGHT
    if bg_y2 >= HEIGHT:
        bg_y2 = -HEIGHT

    screen.blit(bg_img, (0, bg_y1))
    screen.blit(bg_img, (0, bg_y2))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEMOTION:
            x, y = event.pos
            car.x = x - 25

        if game_over and event.type == pygame.MOUSEBUTTONDOWN:
            reset_game()

    if not game_over:

        # Enemy spawn
        if random.randint(1, 100) == 1:
            enemies.append(pygame.Rect(random.randint(0, 350), 0, 50, 80))

        # Coin spawn
        if random.randint(1, 40) == 1:
            coins.append(pygame.Rect(random.randint(0, 370), 0, 30, 30))

        # Bomb spawn 💣
        if random.randint(1, 120) == 1:
            bombs.append(pygame.Rect(random.randint(0, 360), 0, 40, 40))

        # Enemies
        for enemy in enemies[:]:
            enemy.y += speed
            screen.blit(enemy_img, (enemy.x, enemy.y))

            if car.colliderect(enemy):
                gameover_sound.play()
                game_over = True

            if enemy.y > HEIGHT:
                enemies.remove(enemy)

        # Coins
        for coin in coins[:]:
            coin.y += speed
            screen.blit(coin_img, (coin.x, coin.y))

            if car.colliderect(coin):
                coins.remove(coin)
                score += 1
                coin_sound.play()

                if score % 5 == 0:
                    speed += 1

            elif coin.y > HEIGHT:
                coins.remove(coin)

        # Bombs 💣
        for bomb in bombs[:]:
            bomb.y += speed
            screen.blit(bomb_img, (bomb.x, bomb.y))

            if car.colliderect(bomb):
                bomb_sound.play()
                gameover_sound.play()
                game_over = True

            if bomb.y > HEIGHT:
                bombs.remove(bomb)

    # Car boundary
    if car.x < 0:
        car.x = 0
    if car.x > WIDTH - 50:
        car.x = WIDTH - 50

    # Draw car
    screen.blit(car_img, (car.x, car.y))

    # UI
    draw_text("Score: " + str(score), font, (0,0,0), 10, 10)
    draw_text("Speed: " + str(speed), font, (0,0,0), 250, 10)

    # Game Over
    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        draw_text("GAME OVER", big_font, (255, 0, 0), 70, 250)
        draw_text("Tap to Restart", font, (255, 255, 255), 120, 320)

    pygame.display.update()
    clock.tick(60)
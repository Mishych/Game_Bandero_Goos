import pygame
import os
import random
from pygame.constants import K_DOWN, K_RIGHT, K_UP, K_LEFT, K_SPACE

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("sounds/kordhell_-_live_another_day_muzati.net.mp3")
pygame.mixer.music.play(-1)

explosion_sound_1 = pygame.mixer.Sound("sounds/boevoy-vzryiv.wav")
explosion_sound_2 = pygame.mixer.Sound("sounds/katastroficheskiy-spontannyiy-vzryiv-snaryada.wav")
explosion_sound_3 = pygame.mixer.Sound("sounds/aa4b773936bb0cb.mp3")
game_over_sound = pygame.mixer.Sound("sounds/provalil-igru-pohoronnyi-marsh.mp3")

pygame.init()
HEIGHT = 800
WIDTH = 1200

main_display = pygame.display.set_mode((WIDTH, HEIGHT))

COLOR_WHITE = (250, 250,250)
COLOR_BlACK = (0, 0, 0)
COLOR_RED = (250, 0, 0)
COLOR_BLUE = (0, 0, 250)

bg = pygame.transform.scale(pygame.image.load('images/background.png'), (WIDTH, HEIGHT))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 3

IMAGE_PATH = "goose"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)

player = pygame.image.load('images/player.png').convert_alpha()

player_rect = player.get_rect()

player_rect.x = 200
player_rect.y = 240

player_move_down = [0, 4]
player_move_right = [4, 0]
player_move_top = [0, -4]
player_move_left = [-4, 0]

def create_boss():
    boss = pygame.transform.scale(pygame.image.load('images/pngwing.com (4).png'), (300, 260)).convert_alpha()
    boss_rect = boss.get_rect()
    boss_rect.x = WIDTH
    boss_rect.y = random.randint(70, HEIGHT-300)
    boss_move = [random.randint(-13, -4), 0]
    return [boss, boss_rect, boss_move]

CREATE_BOSS = pygame.USEREVENT
pygame.time.set_timer(CREATE_BOSS, 10000)

bosses = []

def create_enemy():
    enemy = pygame.image.load('images/enemy.png').convert_alpha()
    enemy_rect = enemy.get_rect()
    enemy_rect.x = WIDTH
    enemy_rect.y = random.randint(70, HEIGHT-150)
    enemy_move = [random.randint(-13, -4), 0]
    return [enemy, enemy_rect, enemy_move]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

enemies = []

def create_bonus():
    bonus = pygame.transform.scale(pygame.image.load('images/bonus.png'), (200, 150)).convert_alpha()
    bonus_rect = bonus.get_rect()
    bonus_rect.x = random.randint(100, WIDTH-200)
    bonus_rect.y = -270
    bonus_move = [0, random.randint(3, 5)]
    return [bonus, bonus_rect, bonus_move]

CREATE_BONUS = CREATE_ENEMY + 1
pygame.time.set_timer(CREATE_BONUS, 1500)

CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE, 200)

bonuses = []
encountered_enemies = 0

FONT_1 = pygame.font.SysFont('Verdana', 40)
FONT_3 = pygame.font.SysFont('Verdana', 60)
FONT_4 = pygame.font.SysFont('Verdana', 25)

score = 0
enem = 0
n = 0
image_index = 0
p = 0

FPS = pygame.time.Clock()
playing = True
n_added = True           

while playing:
    FPS.tick(300)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
             
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
            
        if event.type == CREATE_BOSS:
            bosses.append(create_boss())
            
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
            
        if event.type == CHANGE_IMAGE:
            player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index]))
            image_index += 1
            if image_index >= len(PLAYER_IMAGES):
                image_index = 0
    
    bg_X1 -= bg_move
    bg_X2 -= bg_move
    
    if bg_X1 < -bg.get_width():
        bg_X1 = bg.get_width()
         
    if bg_X2 < -bg.get_width():
        bg_X2 = bg.get_width()
                   
    main_display.blit(bg, (bg_X1, 0))
    main_display.blit(bg, (bg_X2, 0))

    keys = pygame.key.get_pressed()

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])
        if player_rect.colliderect(enemy[1]):
            # print("BOOM!")
            explosion_sound_1.play()
            main_display.blit(FONT_4.render("BOOM!", True, COLOR_RED), (player_rect.x + 210, player_rect.y + 46))
            enemies.remove(enemy)
            encountered_enemies += 1
            enem += 1
        if score % 4 == 0 and n_added == True:
            p += 0.7
            n += 1
            n_added = False
            
        enemy[2] = [random.randint(-11 - n, -2 - n), 0]
        player_move_down = [0, 4 + p]
        player_move_right = [4 + p, 0]
        player_move_top = [0, -4 - p]
        player_move_left = [-4 - p, 0]
        
    for bos in bosses:
        bos[1] = bos[1].move(bos[2])
        main_display.blit(bos[0], bos[1])
        if player_rect.colliderect(bos[1]):
            # print("BOOM!")
            explosion_sound_2.play()
            main_display.blit(FONT_4.render("BOOM!", True, COLOR_RED), (player_rect.x + 210, player_rect.y + 10))
            bosses.remove(bos)
            encountered_enemies += 2
            enem += 2
      
        bos[2] = [random.randint(-11 - n, -2 - n), 0]
        
    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])
        
        for enemy in enemies:
            if enemy[1].colliderect(bonus[1]):
                bonuses.remove(bonus)
                
        for bos in bosses:
            if bos[1].colliderect(bonus[1]):
                bonuses.remove(bonus)
        
        if player_rect.colliderect(bonus[1]):
            explosion_sound_3.play()
            bonuses.remove(bonus)
            score += 1
            n_added = True
         
    if encountered_enemies >= 10:
        # print("GAME OVER !")
        pygame.mixer.music.stop()
        game_over_sound.play()
        main_display.blit(FONT_3.render("GAME OVER!!!!!", True, COLOR_RED), (WIDTH-830, 300))
        pygame.display.update()
        pygame.time.delay(5300)
        playing = False
                       
    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)
        
    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)

    if keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(player_move_top)
         
    if keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)
     
    # Додавання клавіші "SPACE" для прискорення гравця   
    if keys[K_DOWN] and keys[K_SPACE] and player_rect.bottom < HEIGHT:
        player_move_down = [0, 4.5 + p] 
        player_rect = player_rect.move(player_move_down)

    if keys[K_RIGHT] and keys[K_SPACE] and player_rect.right < WIDTH:
        player_move_right = [4.5 + p, 0]
        player_rect = player_rect.move(player_move_right)

    if keys[K_UP] and keys[K_SPACE] and player_rect.top > 0:
        player_move_top = [0, -4.5 - p]
        player_rect = player_rect.move(player_move_top)

    if keys[K_LEFT] and keys[K_SPACE] and player_rect.left > 0:
        player_move_left = [-4.5 - p, 0]
        player_rect = player_rect.move(player_move_left)
               
    main_display.blit(player, player_rect)
    main_display.blit(FONT_1.render("score: " + str(score), True, COLOR_BLUE), (WIDTH-300, 20))
    main_display.blit(FONT_1.render("boom: " + str(enem), True, COLOR_RED), (WIDTH-304, 69))
    
    pygame.display.flip()
    
    for enemy in enemies:
        if enemy[1].left < -300:
            enemies.pop(enemies.index(enemy))
            
    for bos in bosses:
        if bos[1].left < -400:
            bosses.pop(bosses.index(bos))
    
    for bonus in bonuses:
        if bonus[1].bottom > HEIGHT + 150:
            bonuses.pop(bonuses.index(bonus))
  
pygame.mixer.music.stop()
pygame.mixer.quit()

pygame.quit()
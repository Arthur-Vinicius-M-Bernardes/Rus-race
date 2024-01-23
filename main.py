import random
import pygame


pygame.init()

x = 1280
y = 720

screen = pygame.display.set_mode((x,y))
pygame.display.set_caption('RUs Race')

bg = pygame.image.load('sprites/bg.jpg').convert_alpha()
bg = pygame.transform.scale(bg, (x,y))

missile = pygame.image.load('sprites/missile.png')
missile = pygame.transform.scale(missile, (35,35))

food_cheese = pygame.image.load('sprites/cheese.png')
food_cheese = pygame.transform.scale(food_cheese, (55,55))

chefsprite = pygame.image.load('sprites/chef.png')
chefsprite = pygame.transform.scale(chefsprite, (70,120))

rottensprite = pygame.image.load('sprites/rotten.png')
rottensprite = pygame.transform.scale(rottensprite,(60,60))

counter = pygame.image.load('sprites/counter.jpg')
counter = pygame.transform.scale(counter, (124,616))


pos_food_cheese_x = 500
pos_food_cheese_y = 360

pos_chef_x = 150
pos_chef_y = 300

pos_missile_x = 150
pos_missile_y = 300
missile_velocity = 0

pos_rotten_x = 500
pos_rotten_y = 500

font = pygame.font.SysFont('sprites/PressStart2P.tff', 48)
trigger = False

pontos = 0
vidas = 3

chef_rect = chefsprite.get_rect()
cheese_rect = food_cheese.get_rect()
missile_rect = missile.get_rect()
rotten_rect = rottensprite.get_rect()
counter_rect = counter.get_rect()

def respawn():
    x = 1350
    y = random.randint(110,660)
    return [x,y]
def respawn_rotten():
    x = 1350
    y = random.randint(110,700)
    return [x,y]
def reload():
    trigger = False
    respawn_missile_x = pos_chef_x
    respawn_missile_y = pos_chef_y
    missile_velocity = 0
    return [respawn_missile_x,respawn_missile_y, missile_velocity, trigger]

def collision_food():
    global pontos

    if missile_rect.colliderect(cheese_rect):
        pontos -= 1
        return True
    elif cheese_rect.colliderect(counter_rect):
        pontos += 1
        return True
    else:
        return False
def collision_rotten():
    global vidas
    global pontos
    if rotten_rect.colliderect(counter_rect):
        vidas -= 1
        return True
    elif missile_rect.colliderect(rotten_rect):
        pontos += 1
        return True
    else:
        return False

run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.blit(bg, (0, 0))
    rel_x = x % bg.get_rect().width
    screen.blit(bg, (rel_x - bg.get_rect().width,0))
    if rel_x < 1280:
        screen.blit(bg, (rel_x, 0))
    key = pygame.key.get_pressed()
    if key[pygame.K_UP] and pos_chef_y > 1:
        pos_chef_y -= 3
        if not trigger:
            pos_missile_y -=3
    if key[pygame.K_DOWN] and pos_chef_y < 665:
        pos_chef_y += 3
        if not trigger:
            pos_missile_y +=3

    if key[pygame.K_SPACE]:
        trigger = True
        missile_velocity = 5

    if cheese_rect.colliderect(counter_rect):
        pos_food_cheese_y = respawn()[0]
        pos_food_cheese_x = respawn()[1]

    if pos_missile_x == 1300:
        pos_missile_x, pos_missile_y, missile_velocity, trigger = reload()

    if pos_food_cheese_x == 200 or collision_food():
        pos_food_cheese_y = respawn()[0]
        pos_food_cheese_x = respawn()[1]

    if pos_rotten_x == 200 or collision_rotten():
        pos_rotten_y = respawn_rotten()[1]
        pos_rotten_x = respawn_rotten()[0]




    chef_rect.y = pos_chef_y
    chef_rect.x = pos_chef_x

    cheese_rect.x = pos_food_cheese_y
    cheese_rect.y = pos_food_cheese_x

    missile_rect.y = pos_missile_y
    missile_rect.x = pos_missile_x

    rotten_rect.y = pos_rotten_y
    rotten_rect.x = pos_rotten_x

    counter_rect.x = 230
    counter_rect.y = 104


    pos_rotten_x -= 1
    pos_food_cheese_y -= 2
    pos_missile_x += missile_velocity

    pygame.draw.rect(screen,(255,0,0), chef_rect, 4)
    pygame.draw.rect(screen, (255, 0, 0), cheese_rect, 4)
    pygame.draw.rect(screen, (255, 0, 0), missile_rect, 4)
    pygame.draw.rect(screen, (0,255,0), rotten_rect, 4)


    score = font.render(f' SCORE: {int(pontos)} ', True, (255,255,255))
    lives = font.render(f' LIVES: {int(vidas)} ', True, (255, 255, 255))
    screen.blit(score, (50,50))
    screen.blit(lives, (250, 50))


    screen.blit(counter, (230,104))
    screen.blit(missile, (pos_missile_x, pos_missile_y))
    screen.blit(food_cheese, (pos_food_cheese_y, pos_food_cheese_x))
    screen.blit(chefsprite, (pos_chef_x,pos_chef_y))
    screen.blit(rottensprite, (pos_rotten_x,pos_rotten_y))


    pygame.display.update()



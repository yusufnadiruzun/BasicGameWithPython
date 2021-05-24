
import pygame
import os
pygame.font.init()
pygame.mixer.init()
WIDTH, HEIGHT = 900,500
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("First Game")
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW=(255,255,0)
FPS = 60
VEL =5
BULLET_VEL = 7
MAX_BULLETS = 3
BORDER = pygame.Rect(WIDTH//2 -5,0,10,HEIGHT)


HEALTH_FONT = pygame.font.SysFont('comicsans',40)
WINNER_FONT = pygame.font.SysFont('comicsans',100)
RED_HIT = pygame.USEREVENT +1
YELLOW_HIT = pygame.USEREVENT +2

red_bullets=[]
yellow_bullets=[]

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets','space.png')),(WIDTH,HEIGHT))
def handle_bullets(yellow_bullets, red_bullets, yellow,red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x >WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x <0:
            yellow_bullets.remove(bullet)

def draw_window(red,yellow,red_bullets, yellow_bullets,RED_HEALTH, YELLOW_HEALTH  ):
    WIN.blit(SPACE,(0,0))
    pygame.draw.rect(WIN,BLACK,BORDER)
    WIN.blit(YELLOW_SPACESHIP,(yellow.x,yellow.y))
    WIN.blit(RED_SPACESHIP,(red.x,red.y))
    red_health_text = HEALTH_FONT.render("Health :" + str(YELLOW_HEALTH),1,WHITE)
    yellow_health_text = HEALTH_FONT.render("Health :" + str(RED_HEALTH),1,WHITE)
    
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width()-10,10))
    WIN.blit(yellow_health_text,(10,10))
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    pygame.display.update()

def red_handle_movement(key_pressed,red):
        if key_pressed[pygame.K_LEFT] and red.x + VEL - red.width > BORDER.x : #left
            red.x -= VEL
        if key_pressed[pygame.K_RIGHT] and red.x +VEL +red.width < WIDTH: #right
            red.x += VEL
        if key_pressed[pygame.K_UP] and red.y - VEL  >0: #up
            red.y -= VEL
        if key_pressed[pygame.K_DOWN] and red.y +VEL +red.width < HEIGHT-15: #down
            red.y += VEL
def yellow_handle_movement(key_pressed,yellow):
        if key_pressed[pygame.K_a] and yellow.x - VEL >0: #left
            yellow.x -= VEL
        if key_pressed[pygame.K_d] and yellow.x +VEL +yellow.width <BORDER.x: #right
            yellow.x += VEL
        if key_pressed[pygame.K_w] and yellow.y +VEL >0: #up
            yellow.y -= VEL
        if key_pressed[pygame.K_s] and yellow.y +VEL + yellow.height <HEIGHT-15 : #down
            yellow.y += VEL

def draw_winner(text):
    draw_text = WINNER_FONT.render(text,1,WHITE)
    WIN.blit(draw_text,(WIDTH/2- draw_text.get_width()/2,HEIGHT/2- draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    red = pygame.Rect(700,100,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    yellow = pygame.Rect(300,100,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    clock = pygame.time.Clock()
    run = True
    RED_HEALTH = 10
    YELLOW_HEALTH = 10
    while run:
        clock.tick(FPS) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if  event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect( yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    
                if  event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect( red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
            
            if event.type == RED_HIT:
                RED_HEALTH -=1
              
            if event.type == YELLOW_HIT:
                YELLOW_HEALTH -=1
              

        winner_text = ""
        if RED_HEALTH <= 0:
            winner_text = 'Yellow Wins !'
        if YELLOW_HEALTH <=0:
            winner_text = 'Red Wins !'
        if winner_text != "":
            draw_winner(winner_text)
            break
        key_pressed = pygame.key.get_pressed()
        yellow_handle_movement(key_pressed,yellow)
        red_handle_movement(key_pressed,red)
        draw_window(red,yellow,red_bullets,yellow_bullets,RED_HEALTH,YELLOW_HEALTH)
        handle_bullets(yellow_bullets,red_bullets,yellow,red,)
    main()     

if __name__ == "__main__":
    main()      
import pygame, sys
import random
import time
import math
import numpy as np

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        global player_pos, player_counter,lose_life
        super().__init__(group)
        self.size = (700,700)
        self.c_n = 0
        self.cos_ch = 10
        self.pl_dr = "right"
        self.make_image()
        self.rect = self.image.get_rect(center = pos)
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.repeat_ded = 0
    
    def input(self):
        global player_counter
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1

            if self.pl_dr != "back":
                player_counter = 0

            if self.c_n == 2:
                self.c_n = 0

            if player_counter >= self.cos_ch:
                self.c_n += 1
                player_counter = 0

            self.pl_dr = "back"
            player_counter += 1

        elif keys[pygame.K_DOWN]:
            self.direction.y = 1

            if self.pl_dr != "front":
                player_counter = 0

            if self.c_n == 2:
                self.c_n = 0

            if player_counter >= self.cos_ch:
                self.c_n += 1
                player_counter = 0

            self.pl_dr = "front"
            player_counter += 1

        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1

            if self.pl_dr != "right":
                player_counter = 0

            if self.c_n == 2:
                self.c_n = 0

            if player_counter >= self.cos_ch:
                self.c_n += 1
                player_counter = 0

            self.pl_dr = "right"
            player_counter += 1

        elif keys[pygame.K_LEFT]:
            self.direction.x = -1

            if self.pl_dr != "left":
                player_counter = 0

            if self.c_n == 2:
                self.c_n = 0

            if player_counter >= self.cos_ch:
                self.c_n += 1
                player_counter = 0

            self.pl_dr = "left"
            player_counter += 1

        else:
            self.direction.x = 0
       
    def make_image(self):
        global lose_life,dead_ani
        t = str(self.c_n)
        self.image = pygame.image.load('Graphics/player/player_'+ self.pl_dr + '/player_' + self.pl_dr + '_' + t + '.png')
        if lose_life:
            self.image = pygame.image.load('Graphics/player/player_dead/dead_2.png')
            dead_ani += 1
            if dead_ani >= 10:
                lose_life = False
                dead_ani = 0

        self.image = pygame.transform.scale(self.image, self.size)
    
    def restriction(self):

        if self.rect.centerx <= 725:
            self.rect.centerx = 725

        elif self.rect.centerx >= 2580:
            self.rect.centerx = 2580

        if self.rect.centery <= 715:
            self.rect.centery = 715

        elif self.rect.centery >= 2570:
            self.rect.centery = 2570

    def update(self):
        global player_pos, en_pl_pos
        self.input()
        self.make_image()
        self.rect.x += self.direction[0]*self.speed
        self.rect.y += self.direction[1]*self.speed
        self.restriction()
        player_pos = (self.rect.x, self.rect.y)
        en_pl_posx = player_pos[0]+220
        en_pl_posy = player_pos[1]+360
        en_pl_pos = (en_pl_posx, en_pl_posy)

class AllGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        self.display_surface = pygame.display.get_surface()
        self.en_m = 119

        # cam offset
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0]//2
        self.half_h = self.display_surface.get_size()[1]//2

        # ground
        self.ground_surface = pygame.image.load('Graphics/ground.png').convert_alpha()
        self.ground = pygame.transform.scale(self.ground_surface, (3300, 3300))
        self.ground_rect = self.ground.get_rect(topleft = (0,0))

    def camera(self, target):
        global player_offset

        self.offset.x = target.rect.centerx - self.half_h
        self.offset.y = target.rect.centery - self.half_w
        player_offset = (self.offset.x, self.offset.y)

    def custom_draw(self,player,sword):
        global cnt, en_lis_pos, player_pos, move, screen, ens_kill
# enemy var
        enemy_index = 0

# find offset
        self.camera(player)

######### ground 
        ground_offset = self.ground_rect.topleft - self.offset
        self.display_surface.blit(self.ground, ground_offset)

######### elements
        sword.draw(screen)

        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
        


######### generating the enemy
        if cnt > self.en_m:
            en_x = random.randint(680, 2485)
            en_y = random.randint(680, 2460)
            all_enemy.add(Enemy((en_x, en_y)))
            en_lis_pos.append((en_x, en_y))
            cnt = 0
        
        if ens_kill>=10:
            self.en_m-=10
            ens_kill=0

######### moving the enemy
        if all_enemy:
            for enemy in all_enemy:
                en_lis_pos[enemy_index] = self.enemy_move(en_lis_pos[enemy_index])
                en_x = en_lis_pos[enemy_index][0] - self.offset.x
                en_y = en_lis_pos[enemy_index][1] - self.offset.y

                screen.blit(enemy.surf, (en_x, en_y))
                enemy_index += 1

        cnt += 1

    def enemy_move(self, en_pos):
        global player_pos

        en_movex = 0
        en_movey = 0

        if ((player_pos[0]+45) - en_pos[0])+200 < -move:
            en_movex = -move
        elif ((player_pos[0]+45) - en_pos[0])+200 > move:
            en_movex = move
        if ((player_pos[1]+45) - en_pos[1])+200 < -move:
            en_movey = -move
        elif ((player_pos[1]+45) - en_pos[1])+200 > move:
            en_movey = move
        
        return (en_movex+en_pos[0], en_movey+en_pos[1])

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.speed = 0.5
        self.surf = pygame.image.load('Graphics/enemy/enemy.png')
        self.image = pygame.transform.scale(self.surf, (100,100))
        self.rect = self.image.get_rect(center=pos)

class Sword:
    def __init__(self):

        self.x, self.y = 355, 405
        self.xr = self.x
        self.change = self.x
        self.size = (200,200)
        self.att = 0
        self.dir = 1
# 375 out 355 in
        self.image = pygame.image.load("Graphics/sword/sword_right.png")
        self.image = pygame.transform.scale(self.image, self.size)

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            if self.dir == 0:
                self.xr += 10
                self.x = self.xr

            self.dir = 1
        elif keys[pygame.K_LEFT]:
            if self.dir == 1:
                self.xr += -10
                self.x = self.xr

            self.dir = 0

    def make_image(self):
        if self.dir == 0:
            self.image = pygame.image.load("Graphics/sword/sword_left.png")
            self.image = pygame.transform.scale(self.image, self.size)

        if self.dir == 1:
            self.image = pygame.image.load("Graphics/sword/sword_right.png")
            self.image = pygame.transform.scale(self.image, self.size)

    def attack(self):
        global sword_dir
        if self.dir == 1:
            self.x += 21
        else:
            self.x += -21
        
        self.att = 1
    
    def update(self):
        self.input()

        if self.x != self.xr:
            if self.dir == 0:
                self.x += 1
            else:
                self.x += -1
            
            self.att = 1
        
        else:
            self.att = 0
        
        self.change == self.x
                
    def draw(self, screen):
        self.make_image()
        screen.blit(self.image, (self.x, self.y))

def title_update(button_select):
    screen.blit(back_img, (0,0))
    screen.blit(title_img, (500-int(title_img.get_width()/2), 150-int(title_img.get_height()/2)))
    screen.blit(instruct_b, (185, 500))
    if button_select != 0:
        screen.blit(play_not_select, (295, 300))
        screen.blit(help_select, (295, 400))
    else:
        screen.blit(play_select, (295, 300))
        screen.blit(help_not_select, (295, 400))

def buttons_select():
    global button_select, game_start, helps

    keys = pygame.key.get_pressed()
    if button_select == 0:
        if keys[pygame.K_SPACE]:
            game_start = True
            button_select_music.play()
    
    elif button_select == -1:
        if keys[pygame.K_SPACE]:
            helps = True
            button_select_music.play()


    if keys[pygame.K_UP]:
        if button_select == 0:
            button_select = 0

        else:
            button_select = 0
            button_change_music.play()
            
    if keys[pygame.K_DOWN]:
        if button_select == -1:
            button_select = -1

        else:
            button_select = -1
            button_change_music.play()

def player_died(player_pos,sword):
    global dead, tick, player_offset, en_lis_pos, all_enemy, ens_kill,lives, lose_life, tot_dead

    t = []
    x,y=650,650
    e_i = 0
    r = False

    for pos in en_lis_pos:
        if ((player_pos[0]+45) - pos[0])+200 > -45 and ((player_pos[0]+45) - pos[0])+200 < 45:
            if ((player_pos[1]+45) - pos[1])+200 > -45 and ((player_pos[1]+45) - pos[1])+200 < 45:
                if lives == 0:
                    dead = True
                    tick = 0
                    dead_music.play()
                else:
                    lives-=1
                    lose_life=True
                    life_lose_music.play()
                    en_lis_pos.remove(pos)
                    t.append(e_i)
                    r=True
                    

        if sword.att == 1:
            if ((player_pos[0]+45) - pos[0])+200 > -65 and ((player_pos[0]+45) - pos[0])+200 < 65:
                if ((player_pos[1]+45) - pos[1])+200 > -65 and ((player_pos[1]+45) - pos[1])+200 < 65:
                    if ((player_pos[0]+45) - pos[0])+200 < 0 and sword.dir == 1 :
                        if not r:
                            en_lis_pos.remove(pos)
                        t.append(e_i)
                    elif ((player_pos[0]+45) - pos[0])+200 > 0 and sword.dir == 0:
                        if not r:
                            en_lis_pos.remove(pos)
                        t.append(e_i)
        
            e_i += 1


    if lose_life:
        x,y = 650,650
    else:
        x,y= player_pos[0], player_pos[1]

    for i in t:
        e_i = 0
        for enemy in all_enemy:
            if e_i == i:
                enemy.kill()
                ens_kill += 1
                tot_dead += 1
            e_i += 1
    
    return x,y
    

dead = False
# screen variables
FPS = 60
HEIGHT = 900
WIDTH = 1000

# initalize and setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Escape")

# groups
all_enemy = pygame.sprite.Group()
all_group = AllGroup()

# clock
clock = pygame.time.Clock()

# vectors
player_pos = pygame.math.Vector2()

# variable
cnt = 0
button_select = 0

tick = 0
g_m = True
select = 1
helps = False
en_pl_pos = 0
move = 1
player_offset = 0
ens_kill = 0
tot_dead = 0
enemy_cnt = 0
game_start = False
player_counter = 0
dead_ani = 0
lives = 3
lose_life = False
black = (0,0,0)

# lists
bullets = []
bullets_pos = []
en_lis_pos = []
pl_lis_pos = []

# objects
player = Player((1000,1000), all_group)
sword = Sword()

# surf and images

# background
back_surf = pygame.image.load("Graphics/title/background_title.png")
back_img = pygame.transform.scale(back_surf, (1000, 1000))

# title
title_surf = pygame.image.load("Graphics/title/Title.png")
title_img = pygame.transform.scale(title_surf, (700, 700))

# target
mouse_cursor_surf = pygame.image.load("Graphics/mouse_item.png")

# play button
play_surf = pygame.image.load("Graphics/title/button/play/play_not_select.png")
play_not_select = pygame.transform.scale(play_surf, (400, 400))
play_select_surf = pygame.image.load("Graphics/title/button/play/play_select.png")
play_select = pygame.transform.scale(play_select_surf, (400, 400))

# settings button
help_surf = pygame.image.load("Graphics/title/button/help/help_not_select.png")
help_not_select = pygame.transform.scale(help_surf, (400, 400))
help_select_surf = pygame.image.load("Graphics/title/button/help/help_select.png")
help_select = pygame.transform.scale(help_select_surf, (400, 400))

# instructions for buttons
instruct_b = pygame.image.load("Graphics/title/instruct_buttons.png")
instruct_b = pygame.transform.scale(instruct_b, (600, 600))

# help
help = pygame.image.load("Graphics/title/help.png")
help = pygame.transform.scale(help, (1000,900))

# hearts
full_hearts = pygame.image.load("Graphics/hearts/full_hearts.png")
full_hearts = pygame.transform.scale(full_hearts, (400,400))
two_hearts = pygame.image.load("Graphics/hearts/two_hearts.png")
two_hearts = pygame.transform.scale(two_hearts, (400,400))
one_heart = pygame.image.load("Graphics/hearts/one_heart.png")
one_heart = pygame.transform.scale(one_heart, (400,400))
zero_hearts = pygame.image.load("Graphics/hearts/zero_hearts.png")
zero_hearts = pygame.transform.scale(zero_hearts, (400,400))

# win
win_bar_0 = pygame.image.load("Graphics/win_bar/win_bar_0.png")
win_bar_0 = pygame.transform.scale(win_bar_0, (1000,1000))
win_bar_1 = pygame.image.load("Graphics/win_bar/win_bar_1.png")
win_bar_1 = pygame.transform.scale(win_bar_1, (1000,1000))
win_bar_2 = pygame.image.load("Graphics/win_bar/win_bar_2.png")
win_bar_2 = pygame.transform.scale(win_bar_2, (1000,1000))
win_bar_3 = pygame.image.load("Graphics/win_bar/win_bar_3.png")
win_bar_3 = pygame.transform.scale(win_bar_3, (1000,1000))
win_bar_4 = pygame.image.load("Graphics/win_bar/win_bar_4.png")
win_bar_4 = pygame.transform.scale(win_bar_4, (1000,1000))
win_bar_5 = pygame.image.load("Graphics/win_bar/win_bar_5.png")
win_bar_5 = pygame.transform.scale(win_bar_5, (1000,1000))
win_bar_6 = pygame.image.load("Graphics/win_bar/win_bar_6.png")
win_bar_6 = pygame.transform.scale(win_bar_6, (1000,1000))
win_bar_7 = pygame.image.load("Graphics/win_bar/win_bar_7.png")
win_bar_7 = pygame.transform.scale(win_bar_7, (1000,1000))
win_bar_8 = pygame.image.load("Graphics/win_bar/win_bar_8.png")
win_bar_8 = pygame.transform.scale(win_bar_8, (1000,1000))
win_bar_9 = pygame.image.load("Graphics/win_bar/win_bar_9.png")
win_bar_9 = pygame.transform.scale(win_bar_9, (1000,1000))

win = pygame.image.load("Graphics/win.png")
win = pygame.transform.scale(win, (1000,1000))

w = False
# kill count
skull = pygame.image.load("Graphics/skull.png")
skull = pygame.transform.scale(skull, (50,50))

pygame.mouse.set_visible(False)

# music
game_music = pygame.mixer.Sound('Audio/menu_music.wav')
game_music.set_volume(0.5)
game_music.play(loops = -1)
dead_music = pygame.mixer.Sound('Audio/game_over.wav')
dead_music.set_volume(0.5)
button_select_music = pygame.mixer.Sound('Audio/button_select_music.mp3')
button_select_music.set_volume(0.5)
button_change_music = pygame.mixer.Sound('Audio/button_change_music.wav')
button_change_music.set_volume(0.5)
life_lose_music = pygame.mixer.Sound('Audio/life_lose.wav')
life_lose_music.set_volume(0.5)
wi = pygame.mixer.Sound('Audio/win.wav')
wi.set_volume(0.5)
win_m = pygame.mixer.Sound('Audio/win_main.wav')
win_m.set_volume(0.5)

# font
font = pygame.font.Font('freesansbold.ttf', 32)

while True:
    # reset index
    m_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if w == False:
            if not dead:
                if not game_start:
                    if not helps:
                        buttons_select()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        vol = game_music.get_volume()
                        if vol == 0:
                            game_music.set_volume(0.5)
                        
                        else:
                            game_music.set_volume(0)
            
                if game_start:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            if sword.x == sword.xr:
                                sword.attack()
            
        
####### mouse down 
    if w == False:
        if not dead: 

    # menu
            if not game_start:
                if not g_m:
                    g_m = True
                    time.sleep(2)
                    game_music.stop()
                    game_music = pygame.mixer.Sound('Audio/menu_music.wav')
                    game_music.play()

                if not helps:
                    title_update(button_select)

                else:
                    screen.blit(help, (0,0))
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_b]:
                        helps = False

    # real game
            else:
    ###### text update
                tot_str = str(tot_dead)
                text = font.render(tot_str, True, black)

    ##### group update
                if g_m:
                    g_m = False
                    time.sleep(1)
                    game_music.stop()
                    game_music = pygame.mixer.Sound('Audio/game_music.mp3')
                    game_music.play(loops = -1)


                all_group.update()
                all_group.custom_draw(player, sword)
                screen.blit(mouse_cursor_surf, (m_pos[0]-40, m_pos[1]-40))

    ###########  bullet drawing updating and removing and collision
                player.rect.x, player.rect.y = player_died(player_pos, sword)
                sword.update()
                # hearts
                if lives == 3:
                    screen.blit(full_hearts, (-125,-150))
                elif lives == 2:
                    screen.blit(two_hearts, (-125,-150))
                elif lives == 1:
                    screen.blit(one_heart, (-125,-150))
                else:
                    screen.blit(zero_hearts, (-125,-150))
                
                screen.blit(skull, (875,15))
                screen.blit(text, (925,30))
                if tot_dead//5==1:
                    screen.blit(win_bar_1, (0,375))
                elif tot_dead//5==2:
                    screen.blit(win_bar_2, (0,375))
                elif tot_dead//5==3:
                    screen.blit(win_bar_3, (0,375))
                elif tot_dead//5==4:
                    screen.blit(win_bar_4, (0,375))
                elif tot_dead//5==5:
                    screen.blit(win_bar_5, (0,375))
                elif tot_dead//5==6:
                    screen.blit(win_bar_6, (0,375))
                elif tot_dead//5==7:
                    screen.blit(win_bar_7, (0,375))
                elif tot_dead//5==8:
                    screen.blit(win_bar_8, (0,375))
                elif tot_dead//5==9:
                    screen.blit(win_bar_9, (0,375))
                    w = True
                    wi.play()
                    win_m.play(loops = -1)
                else:
                    screen.blit(win_bar_0, (0,375))
    # 14 to win

                
    ######## if dead
        else:
            if tick >= 15:
                all_enemy = pygame.sprite.Group()
                all_group = AllGroup()

                # clock
                clock = pygame.time.Clock()

                # objects


                # vectors
                BULLET_POS = pygame.math.Vector2(460,510)
                player_pos = pygame.math.Vector2()

                # variable
                cnt = 0
                button_select = 0
                tick = 0
                player_offset = 0
                ens_kill = 0
                enemy_cnt = 0
                move = 1
                tot_dead = 0
                lives = 3
                game_start = False
                dead = False

                player = Player((1000,1000), all_group)
                sword = Sword()

                # lists
                bullets = []
                bullets_pos = []
                en_lis_pos = []
                pl_lis_pos = []
    
    else:
        screen.blit(win,(0,0))
        game_music.set_volume(0)

########## check if player died
    tick += 1


    pygame.display.update()
    clock.tick(FPS)

# 69 hrs

# to do
# 7. polish
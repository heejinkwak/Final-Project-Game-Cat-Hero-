import pygame
import random
from os import path

#게임 초기화 
pygame.init()
pygame.mixer.init()

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

#게임창 옵션 설정
WIDTH = 800
HEIGHT = 800
FPS = 40
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("곽희진(20211859)-Cat Hero!")

#게임 내 필요한 설정
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
NAVY = (33,53,85)

clock = pygame.time.Clock()


#Font 설정
font_name = pygame.font.match_font('VCR_OSD_MONO_1.001')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, NAVY)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

#첫 게임 화면
def show_opening_page():
    screen.fill(BLACK)
    back_img = pygame.image.load(path.join(img_dir, "Opening Background(800x800).png")).convert()
    back_img = pygame.transform.scale(back_img,(WIDTH,HEIGHT))
    screen.blit(back_img, (0,0))
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

#룰 설명 화면
def instructions_page():
    screen.fill(BLACK)
    background_image = pygame.image.load(path.join(img_dir, "Instructions2.png")).convert()
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
    screen.blit(background_image, (0, 0))
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

def game_ending():
    pygame.mixer.music.stop()
    screen.fill(BLACK)
    ending_image = pygame.image.load(path.join(img_dir, "Game Ending.png")).convert() 
    ending_image = pygame.transform.scale(ending_image, (WIDTH, HEIGHT))
    screen.blit(ending_image, (0, 0))
    pygame.display.flip()
    win_sound.play()
    pygame.time.wait(6000)

    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                waiting = False
            if event.type == pygame.KEYUP:
                waiting = False

    

#게임오버 화면
def show_game_over():
        pygame.mixer.music.stop()
        screen.fill(BLACK)
        game_over_img = pygame.image.load(path.join(img_dir, "GameOver2.png")).convert()
        game_over_img = pygame.transform.scale(game_over_img, (WIDTH, HEIGHT))
        screen.blit(game_over_img, (0, 0))
        pygame.display.flip()
        game_over_sound.play() 
        pygame.time.wait(3000)
        

        waiting = True
        while waiting:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                    waiting=False
 

def lifebar(surf, x,y,lives,img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)


def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 250
    BAR_HEIGHT = 20
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)

    pygame.draw.rect(surf,NAVY, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.LEFT_KEY, self.RIGHT_KEY, self.FACING_LEFT = False, False, False
        self.load_frames()
        self.rect = self.idle_frames_left[0].get_rect() #Collision detecting 할때 
        self.rect.midbottom = (240, 750)
        self.current_frame = 0
        self.last_updated = 0
        self.velocity = 0
        self.state = 'idle'
        self.image = self.idle_frames_left[0]
        self.radius = int(self.rect.width / 3)
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 250
        self.shield = 100
        self.lives = 2
        self.is_hidden = False
        self.hide_timer = pygame.time.get_ticks()

    def draw(self, display):     
        display.blit(self.image, self.rect)

        if not self.is_hidden:  # Draw only if not hidden
            display.blit(self.image, self.rect)

    def update(self):
        if self.is_hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.is_hidden = False
            self.rect.midbottom = (240, 750)


        self.velocity = 0
        if self.LEFT_KEY:
            self.velocity = -4
        elif self.RIGHT_KEY:
            self.velocity = 4 
        self.rect.x += self.velocity
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        self.set_state()
        self.animate()

    def set_state(self):
        self.state = ' idle'
        if self.velocity > 0:
            self.state = 'moving right'
        elif self.velocity < 0:
            self.state = 'moving left'

    def animate(self):
        now = pygame.time.get_ticks()
        if self.state == ' idle':
            if now - self.last_updated > 200:
                self.last_updated = now
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames_left)
                if self.FACING_LEFT:
                    self.image = self.idle_frames_left[self.current_frame]
                elif not self.FACING_LEFT:
                    self.image = self.idle_frames_right[self.current_frame]
        else:
            if now - self.last_updated > 100:
                self.last_updated = now
                self.current_frame = (self.current_frame + 1) % len(self.walking_frames_left)
                if self.state == 'moving left':
                    self.image = self.walking_frames_left[self.current_frame]
                elif self.state == 'moving right':
                    self.image = self.walking_frames_right[self.current_frame]
    

    def load_frames(self):
        #my_spritesheet = Spritesheet('poppy_sheet.png')
        #pygame.image.load('MY_IMAGE_NAME.png').convert()
        self.idle_frames_left = [pygame.image.load('Girl-cat(still).png').convert_alpha(),
                                 pygame.image.load('Girl-cat(still2).png').convert_alpha()]
        self.walking_frames_left = [pygame.image.load('Walk1.png').convert_alpha(), pygame.image.load('Walk2.png').convert_alpha(),
                           pygame.image.load('Walk3.png').convert_alpha(), pygame.image.load('Walk4.png').convert_alpha(),
                           pygame.image.load('Walk1.png').convert_alpha(), pygame.image.load('Walk2.png').convert_alpha(),
                           pygame.image.load('Walk3.png').convert_alpha(), pygame.image.load('Walk4.png').convert_alpha()]
        self.idle_frames_right = []
        for frame in self.idle_frames_left:
            self.idle_frames_right.append( pygame.transform.flip(frame,True, False) )
        self.walking_frames_right = []
        for frame in self.walking_frames_left:
            self.walking_frames_right.append(pygame.transform.flip(frame, True, False))
        
        
        
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
    
    def hide(self):
        self.is_hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)



class Mob(pygame.sprite.Sprite):
    def __init__(self,food_type):
        pygame.sprite.Sprite.__init__(self)
        self.food_type = food_type
        self.image_orig = random.choice(food_images)
        self.image_orig.set_colorkey(WHITE)
        self.image_orig = pygame.transform.scale(self.image_orig, (55, 55))
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.bottom = random.randrange(-80, -20)
        self.speedy = random.randrange(2, 6)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-5, 5)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -100 or self.rect.right > WIDTH + 100:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
        


def newmob():
    food_type = random.choice(["choco copy.png", "Grape_nnew.png","ONION.png"])
    m = Mob(food_type)
    all_sprites.add(m)
    mobs.add(m)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = rock
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield','shield2'])
        self.image = helper_images[self.type]
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.top > HEIGHT:
            self.kill()

# GAME GRAPHICS
background = pygame.image.load(path.join(img_dir, "Game-background.png")).convert()
background_rect = background.get_rect()

rock = pygame.image.load(path.join(img_dir, "ROCK.png")).convert_alpha()
rock = pygame.transform.scale(rock, (30, 40))

player_live= pygame.image.load(path.join(img_dir, "paw.png")).convert_alpha()

food_images = []
food_list = ["Grape_nnew.png", "choco copy.png","ONION.png"]
for img in food_list:
    food_images.append(pygame.image.load(path.join(img_dir, img)).convert())


explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
for i in range(15):
    filename = 'collide.png'
    filename_ahh = 'AHH.png'
    
    img_collide = pygame.image.load(path.join(img_dir, filename)).convert()
    img_ahh = pygame.image.load(path.join(img_dir, filename_ahh)).convert()
    
    img_collide.set_colorkey(WHITE)
    img_lg = pygame.transform.scale(img_collide, (80, 80))
    explosion_anim['lg'].append(img_lg)
    
    img_ahh.set_colorkey(BLACK)
    img_sm = pygame.transform.scale(img_ahh, (50, 50))
    explosion_anim['sm'].append(img_sm)

helper_images = {}
helper_images['shield'] = pygame.image.load(path.join(img_dir, 'salmon.png')).convert_alpha()
helper_images['shield2'] = pygame.image.load(path.join(img_dir, 'chicken.png')).convert_alpha()
    
# SOUNDS
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'sfx_throw.wav'))
collide_sound = pygame.mixer.Sound(path.join(snd_dir, 'cat-meow.wav'))
game_over_sound = pygame.mixer.Sound(path.join(snd_dir,'Game over- sound.wav'))
win_sound = pygame.mixer.Sound(path.join(snd_dir,'Winner Sound Effect.mp3'))

expl_sounds = []
for snd in ['boom3.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
pygame.mixer.music.load(path.join(snd_dir, 'BACKGROUND BGM.mp3'))
pygame.mixer.music.set_volume(0.4)

pygame.mixer.music.play(loops=-1)

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(10):
    newmob()

def main():

    show_opening_page()
    instructions_page()

    score=0
    start_time = pygame.time.get_ticks()

    #Game Loop
    running = True
    while running:
        clock.tick(FPS)
      
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player.LEFT_KEY, player.FACING_LEFT = True, True
                    elif event.key == pygame.K_RIGHT:
                        player.RIGHT_KEY, player.FACING_LEFT = True, False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        player.LEFT_KEY = False
                    elif event.key == pygame.K_RIGHT:
                        player.RIGHT_KEY = False
                    elif event.key == pygame.K_SPACE:
                        player.shoot()
                        shoot_sound.play()
                        
        # Update
        all_sprites.update()

        # Rock hitting food(mob)
        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for hit in hits:
            score += 20
            random.choice(expl_sounds).play()
            expl = Explosion(hit.rect.center, 'lg')
            all_sprites.add(expl)
            if random.random() > 0.7:
                pow = Pow(hit.rect.center)
                all_sprites.add(pow)
                powerups.add(pow)
            newmob()

        #food(mob) hitting player
        hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
        for hit in hits:
            player.shield -= 25
            collide_sound.play()
            newmob()
            
            expl = Explosion(hit.rect.center, 'sm')
            all_sprites.add(expl)
         
        if player.shield <= 0:
            player.hide()
            player.lives -= 1
            player.shield = 100

        hits = pygame.sprite.spritecollide(player, powerups, True)
        for hit in hits:
            if hit.type == 'shield' or hit.type == 'shield2':
                player.shield += 20
                score += 10
                if player.shield >= 100:
                    player.shield = 100
      
   
    # if the player died and the explosion has finished playing
        if player.lives == 0 :
            show_game_over()
            running = False
            
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        remaining_time = max(0, 45 - elapsed_time)


        if elapsed_time >= 45 or player.lives == 0:
            game_ending()
            running = False

        #Draw
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        
        draw_shield_bar(screen, 10, 5, player.shield)


        # 점수 보드 
        draw_text(screen, f"Score: {score}", 18, WIDTH / 2, 30)

        all_sprites.update()
        player.update()

        # 타이머 보드
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        remaining_time = max(0, 45 - elapsed_time)

        draw_text(screen, f"Time: {remaining_time}", 18, WIDTH / 2, 10)
        player.draw(screen)

        #Live Drawing (PAW)
        lifebar(screen, WIDTH - 820, 0, player.lives, player_live)

    # *after* drawing everything, flip the display
        pygame.display.flip()
    

    pygame.quit()

if __name__ == "__main__":
    main()

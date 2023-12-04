import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

WIDTH = 550
HEIGHT = 600
FPS = 30

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
NAVY = (33,53,85)

def main():
    pygame.init()
    pygame.mixer.init()

    WIDTH = 550
    HEIGHT = 600
    FPS = 30

    BLACK = (0, 0, 0)
    NAVY = (33, 53, 85)

    img_dir = path.join(path.dirname(__file__), 'img')
    snd_dir = path.join(path.dirname(__file__), 'snd')

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("곽희진(20211859)-Cat Hero!")
    clock = pygame.time.Clock()

    font_name = pygame.font.match_font('VCR_OSD_MONO_1.001')

    def draw_text(surf, text, size, x, y):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, NAVY)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)

    def show_opening_page():
        screen.fill(BLACK)
        back_img = pygame.image.load(path.join(img_dir, "Title page.png")).convert()
        back_img = pygame.transform.scale(back_img, (WIDTH, HEIGHT))
        screen.blit(back_img, (0, 0))
        pygame.display.flip()
        waiting = True
        while waiting:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYUP:
                    waiting = False

    def instructions_page():
        screen.fill(BLACK)
        background_image = pygame.image.load(path.join(img_dir, "Instructions_stage1 copy.png")).convert()
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
    
    def show_game_over():
        screen.fill(BLACK)
        game_over_img = pygame.image.load(path.join(img_dir, "Game over copy.png")).convert()
        game_over_img = pygame.transform.scale(game_over_img, (WIDTH, HEIGHT))
        screen.blit(game_over_img, (0, 0))
        pygame.display.flip()
        pygame.time.wait(3000)

    def newmob():
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

    def draw_shield_bar(surf, x, y, pct):
        if pct < 0:
            pct = 0
        BAR_LENGTH = 200
        BAR_HEIGHT = 10
        fill = (pct / 100) * BAR_LENGTH
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
        pygame.draw.rect(surf, GREEN, fill_rect)
        pygame.draw.rect(surf, WHITE, outline_rect, 2)

    class Player(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(player_img, (130, 140))
            self.image.set_colorkey(WHITE)
            self.rect = self.image.get_rect()
            self.radius = 20
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
            self.speedx = 0
            self.shield = 100
            self.shoot_delay = 250
            self.last_shot = pygame.time.get_ticks()

        def update(self):
            self.speedx = 0
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_LEFT]:
                self.speedx = -8
            if keystate[pygame.K_RIGHT]:
                self.speedx = 8
            if keystate[pygame.K_SPACE]:
                self.shoot()
            self.rect.x += self.speedx
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
            if self.rect.left < 0:
                self.rect.left = 0

        def shoot(self):
            now = pygame.time.get_ticks()
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()

    class Mob(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image_orig = random.choice(meteor_images)
            self.image_orig.set_colorkey(WHITE)
            self.image = self.image_orig.copy()
            self.rect = self.image.get_rect()
            self.radius = int(self.rect.width * .75 / 2)
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
            self.speedx = random.randrange(-3, 3)
            self.rot = 0
            self.rot_speed = random.randrange(-8, 8)
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

    class Bullet(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = bullet_img
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.bottom = y
            self.rect.centerx = x
            self.speedy = -10

        def update(self):
            self.rect.y += self.speedy
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

    # Load all game graphics
    background = pygame.image.load(path.join(img_dir, "background.png")).convert()
    background_rect = background.get_rect()
    player_img = pygame.image.load(path.join(img_dir, "character_stage1.png")).convert()
    bullet_img = pygame.image.load(path.join(img_dir, "laser_player.png")).convert()
    bullet_img = pygame.transform.scale(bullet_img, (15, 20))
    meteor_images = []
    meteor_list = ['Grape_nnew.png', 'choco copy.png']
    for img in meteor_list:
        meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())

    explosion_anim = {}
    explosion_anim['lg'] = []
    explosion_anim['sm'] = []
    for i in range(9):
        filename = 'pixilart-drawing-11.png'.format(i)
        img = pygame.image.load(path.join(img_dir, filename)).convert()
        img.set_colorkey(BLACK)
        img_lg = pygame.transform.scale(img, (100, 100)) #맞출때
        explosion_anim['lg'].append(img_lg)
        img_sm = pygame.transform.scale(img, (50, 50)) #맞았을때 
        explosion_anim['sm'].append(img_sm)

    # Load all game sounds
    shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'laser_shooting_sfx.wav'))
    expl_sounds = []
    for snd in ['boom7.wav', 'boom3.wav']:
        expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
    pygame.mixer.music.load(path.join(snd_dir, 'Zander Noriega - Fight Them Until We Cant.wav'))
    pygame.mixer.music.set_volume(0.4)

    all_sprites = pygame.sprite.Group()
    mobs = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)
    for i in range(8):
        newmob()

    pygame.mixer.music.play(loops=-1)

    show_opening_page()
    instructions_page()

    score = 0
    start_time = pygame.time.get_ticks()

    # Game loop
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update
        all_sprites.update()

        # check to see if a bullet hit a mob
        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for hit in hits:
            score += 50 - hit.radius
            random.choice(expl_sounds).play()
            expl = Explosion(hit.rect.center, 'lg')
            all_sprites.add(expl)
            newmob()

        # check to see if a mob hit the player
        hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
        for hit in hits:
            player.shield -= hit.radius
            expl = Explosion(hit.rect.center, 'sm')
            all_sprites.add(expl)
            newmob()
            if player.shield <= 0:
                show_game_over()
                running = False

        # Draw / render
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        #draw_text(screen, str(score), 18, WIDTH / 2, 10)
        draw_shield_bar(screen, 10, 5, player.shield)

        all_sprites.update()

        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        remaining_time = max(0, 45 - elapsed_time)

        # Display timer
        draw_text(screen, f"Time: {remaining_time}", 18, WIDTH / 2, 10)


        # *after* drawing everything, flip the display
        pygame.display.flip()

        if elapsed_time >= 45:
            #나중에 여기에 stage 2로 넘어가는 이미지 넣기
            running = False

        

    pygame.quit()

if __name__ == "__main__":
    main()

import pygame as pg
from random import randint

pg.init()

GREEN = (50, 255, 150)

WIN_SIZE = (800, 600)
x, y = 0, 1




class BaseSprite(pg.sprite.Sprite):
    def __init__(self, filename, x, y, w, h, speed_x=0, speed_y=0):
        super().__init__()
        self.rect = pg.Rect(x, y, w, h)
        self.image = pg.transform.scale(pg.image.load(filename), (w, h))
        self.speed_x = speed_x
        self.speed_y = speed_y

    def draw(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

class Hero(BaseSprite):
    energy = 0
    max_energy = 25
    points = 0
    
    def update(self):
        self.energy += 1
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.rect.x -= self.speed_x
            if self.rect.x < 0:
                self.rect.x = 0
        if keys[pg.K_RIGHT]:
            self.rect.x += self.speed_x
            if self.rect.x > WIN_SIZE[x] - self.rect.width:
                self.rect.x = WIN_SIZE[x] - self.rect.width
        if keys[pg.K_DOWN]:
            self.rect.y += self.speed_y
            if self.rect.y > WIN_SIZE[y] - self.rect.height:
                self.rect.y = WIN_SIZE[y] - self.rect.height
        if keys[pg.K_UP]:
            self.rect.y -= self.speed_y
            if self.rect.y < 0:
                self.rect.y = 0
        if keys[pg.K_SPACE]:
            self.fire()
    
    def fire(self):
        if self.energy >= self.max_energy:
            self.energy = 0
            fire_snd.play()
            bullet = Bullet('asa.png',self.rect.x, self.rect.y,40, 40, 0, -4)
            bullets.add(bullet)

class Bekon(BaseSprite):
    def update(self):
        super().update()
        if self.rect.y > WIN_SIZE[y]:
            bekons.remove(self)

class UFO(BaseSprite):
    def update(self):
        global ufo_missed
        super().update()
        if self.rect.y > WIN_SIZE[y]:
            ufos.remove(self)
            ufo_missed += 1

class Bullet(BaseSprite):
    def update(self):
        super().update()
        if self.rect.y < 0:
            bullets.remove(self)

class Meteor(BaseSprite):
    def update(self):
        super().update()
        if self.rect.y > WIN_SIZE[y]:
            meteors.remove(self)

def make_meteor():
    speed_y = randint(1, 12)
    speed_x = randint(-3, 3)
    size = randint(4, 10) * 10
    xx = randint(-100, WIN_SIZE[x] + 100)
    yy = -200
    meteor = Meteor('qw.png', xx, yy, size, size, speed_x, speed_y)
    meteors.add(meteor)

def make_bekon():
    speed = randint(3, 10)
    size = speed * 5
    bekon = Bekon('ia.png', randint(0, WIN_SIZE[x]), -50, size, size, 0, speed)
    bekons.append(bekon)

def make_ufo():
    speed = randint(3, 5)
    size = 80
    ufo = UFO('jip.png', randint(0, WIN_SIZE[x]-80), -100, 80, 120, 0, speed)
    ufos.add(ufo)

def set_text(text, x, y, color=(123, 12, 1)):
    mw.blit(
        font1.render(text, True, color),(x,y)
    )

font1 = pg.font.Font(None, 36)

# mw = pg.display.set_mode(WIN_SIZE, pg.FULLSCREEN)
mw = pg.display.set_mode(WIN_SIZE)

clock = pg.time.Clock()

fon = pg.image.load('istockphoto-478898532-612x612.jpg')
fon = pg.transform.scale(fon, WIN_SIZE)

hero = Hero('df.png', WIN_SIZE[x]/2, WIN_SIZE[y]-100, 80, 80, 5, 5)

bekons = []

ufos = pg.sprite.Group()
bullets = pg.sprite.Group()
meteors = pg.sprite.Group()

ufo_missed = 0

bekon = Bekon('ia.png', 400, -50, 10, 10, 0, 3)

pg.mixer.music.load('space.ogg')
pg.mixer.music.play()
fire_snd = pg.mixer.Sound('fire.ogg')

play = True 
game = True

ticks = 0

while game:
    for event in  pg.event.get():
        if event.type == pg.QUIT:
            game = False
    
    if play:
        if ticks %15 == 0:
            make_bekon()

        if ticks %60 == 0:
            make_ufo()

        if ticks %40 == 0:
            make_meteor()

        mw.blit(fon, (0, 0))

        hero.update()
        hero.draw()

        meteors.update()
        meteors.draw(mw)

        for ufo in ufos:
            ufo.update()
            ufo.draw()
        
        for bekon in bekons:
            bekon.update()
            bekon.draw()

        for bullet in bullets:
            bullet.update()
            bullet.draw()

        collides = pg.sprite.groupcollide(bullets, ufos, True, True)
        for bullet, ufo in collides.items():
            hero.points += 1

        set_text(f'Пропущено: {ufo_missed}', 30, 30)
        set_text(f'Очки: {hero.points}', 650, 30)

    pg.display.update()
    clock.tick(60)
    ticks += 1
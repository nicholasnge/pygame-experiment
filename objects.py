#objects
import pygame as pg
from random import randint, choice
from os import path
import pygame.gfxdraw

img_dir = path.join(path.dirname(__file__), 'img')


def spawn(s, all_sprites, slowred, bigyellow, homingpurple):
    spawn_sr(s, all_sprites, slowred)
    spawn_by(s, all_sprites, bigyellow)
    spawn_hp(s, all_sprites, homingpurple)

def spawn_sr(s, all_sprites, slowred):
    s.sr_newtime = pg.time.get_ticks()
    if s.sr:
        if s.sr_newtime - s.sr_oldtime > s.sr_spawnfreq:
            s.sr_oldtime = s.sr_newtime
            sr = SlowRed(s)
            sr.add(all_sprites, slowred)

def spawn_by(s, all_sprites, bigyellow):
    s.by_newtime = pg.time.get_ticks()
    if s.by:
        if s.by_newtime - s.by_oldtime > s.by_spawnfreq:
            s.by_oldtime = s.by_newtime
            by = BigYellow(s)
            by.add(all_sprites, bigyellow)

def spawn_hp(s, all_sprites, homingpurple):
    s.hp_newtime = pg.time.get_ticks()
    if s.hp:
        if s.hp_newtime - s.hp_oldtime > s.hp_spawnfreq:
            s.hp_oldtime = s.hp_newtime
            hp = HomingPurple(s)
            hp.add(all_sprites, homingpurple)

class Chrome(pg.sprite.Sprite):

    def __init__(self, screen, s):
        super().__init__()

        self.screen = screen
        self.s = s
        """screen is a surface, get rect gets the dimensions
        of the surface. so here we are storing into a
        separate variable the rect attributes of both surfaces
        default position for chrome should be (0,0)"""
        chrome_img = pg.image.load(
            path.join(img_dir, self.s.chrome_image)).convert_alpha()
        self.orig_image = chrome_img
        self.image = self.orig_image.copy()
        self.rect = self.image.get_rect()
        self.radius = self.s.chrome_radius
        self.screen_rect = screen.get_rect()
        self.lives = self.s.lives

        #for rotate
        self.last_rotate_time = pg.time.get_ticks()
        self.image_angle = 0
        self.do_i_rotate = s.do_i_rotate

        #direction attributes
        self.rightflag = False
        self.leftflag = False
        self.upflag = False
        self.downflag = False

        #acceleration values for momentum
        self.x_acceleration = 0
        self.y_acceleration = 0
        

        """here we are overwriting the center of chrome, which
        is already an existing value, with the center of screen"""
        
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)

    def update(self, chrome):
        #update mask
        self.mask = pg.mask.from_surface(self.image)
        
        #checks if rotate is switched on
        if self.do_i_rotate:
            self.rotate()
        
        """X AXIS MVMT"""
        if self.rightflag and self.screen_rect.right > self.rect.right:
            if 0 <= self.x_acceleration < self.s.max_accel:
                self.x_acceleration += self.s.accel_ratio
            elif self.x_acceleration < 0:
                self.x_acceleration += (self.s.accel_ratio * 3)
            
        if self.leftflag and self.rect.left > 0:
            if -1 * self.s.max_accel < self.x_acceleration <= 0:
                self.x_acceleration -= self.s.accel_ratio
            elif self.x_acceleration > 0:
                self.x_acceleration -= (self.s.accel_ratio * 3)

        #revert acceleration values to 0 when not moving
        elif not (self.rightflag or self.leftflag):
            if self.x_acceleration > 0:
                self.x_acceleration -= (self.s.accel_ratio
                                        * self.s.inertia)
            elif self.x_acceleration < 0:
                self.x_acceleration += (self.s.accel_ratio
                                        * self.s.inertia) 
            #if its near to 0 enough just make it 0
            if -0.05 < self.x_acceleration < 0.05:
                self.x_acceleration = 0
        """Y AXIS MVMT"""  
        if self.upflag and self.rect.top > 0:
            if -1 * self.s.max_accel < self.y_acceleration <= 0:
                self.y_acceleration -= self.s.accel_ratio
            elif self.y_acceleration > 0:
                self.y_acceleration -= (self.s.accel_ratio * 3)
            
        if self.downflag and self.rect.bottom < self.screen_rect.bottom:
            if 0 <= self.y_acceleration < self.s.max_accel:
                self.y_acceleration += self.s.accel_ratio
            elif self.y_acceleration < 0:
                self.y_acceleration += (self.s.accel_ratio * 3)

        #revert acceleration values to 0 when not moving     
        elif not (self.upflag or self.downflag):
            if self.y_acceleration > 0:
                self.y_acceleration -= self.s.accel_ratio
            elif self.y_acceleration < 0:
                self.y_acceleration += self.s.accel_ratio
            #if its near to 0 enough just make it 0
            if -0.05 < self.y_acceleration < 0.05:
                self.y_acceleration = 0
        
                
        #update xy coordinate changes
        self.mvmtratio = 100 * self.s.mvmtratio * self.s.dt * self.s.dt

        if self.rect.left < 0 or (self.screen_rect.right <
                                   self.rect.right):
            self.x_acceleration *= self.s.bounce_accellost
            if self.rect.left < 0:
                self.centerx = self.rect.width /2
            else:
                self.centerx = self.s.screen_size[0] - (
                    self.rect.width / 2)
            
        if self.rect.top < 0 or (self.screen_rect.bottom <
                                   self.rect.bottom):
            self.y_acceleration *= self.s.bounce_accellost
            if self.rect.top < 0:
                self.centery = self.rect.height /2
            else:
                self.centery = self.s.screen_size[1] - (
                    self.rect.height / 2)

        self.centerx += self.mvmtratio * self.x_acceleration
        self.centery += self.mvmtratio * self.y_acceleration
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery
        self.image_angle = (self.image_angle - self.s.chrome_rotate
                    * 0.5* abs(self.y_acceleration + self.x_acceleration)) % 360

    def rotate(self):
        self.now_time = pg.time.get_ticks()
        if self.now_time - self.last_rotate_time > 10:
            self.last_rotate_time = self.now_time
            self.image_angle = (self.s.chrome_rotate +
                                self.image_angle) % 360
            new_image = pg.transform.rotate(
                self.orig_image, self.image_angle)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
            

        
class SlowRed(pg.sprite.Sprite):
    """SlowRed spawns from left/right only and moves slowly"""
    def __init__(self, s):
        super().__init__()
        self.s = s
        firefox_img = pg.image.load(path.join(img_dir, 'firefox.png')
                                   ).convert_alpha()
        self.image = pg.transform.smoothscale(firefox_img, (
            s.sr_size, s.sr_size))
        self.rect = self.image.get_rect()
        self.radius = int(self.s.sr_size / 2) -1
        self.speed = self.s.sr_speed

        #randint spawn attributes, 0 is left, 1 is right
        self.left_right = randint(0, 1)
        self.position = randint(self.s.sr_size,
                    self.s.screen_size[1] - self.s.sr_size)
                                
        #implications of the randint/range
        self.direction = 1
        self.rect.right = 0

        if self.left_right:
            self.direction = -1
            self.rect.left = self.s.screen_size[0]

        self.rect.centery = self.position 

        #float of x coordinate
        self.centerx = float(self.rect.centerx)


    def update(self, chrome):
        #update xy coordinate changes
        self.mvmtratio = self.s.sr_speed * self.s.dt * self.direction
        self.centerx += self.mvmtratio
        self.rect.centerx = self.centerx

        if self.rect.left > self.s.screen_size[0] or (
                            self.rect.right < 0):
            self.kill()
            
class BigYellow(pg.sprite.Sprite):
    """BigYellow spawns from top/bottom only and moves real slowly"""
    def __init__(self, s):
        super().__init__()
        self.s = s
        ie_img = pg.image.load(path.join(img_dir, 'ie.png')
                                   ).convert_alpha()
        self.image = pg.transform.smoothscale(ie_img, (
            s.by_size, s.by_size))
        self.rect = self.image.get_rect()
        self.radius = int(self.s.by_size / 2) -1
        self.speed = self.s.by_speed

        #randint spawn attributes, 0 is up, 1 is down
        self.up_down = randint(0, 1)
        self.position = randint(0, self.s.screen_size[0])
                                
        #implications of the randint/range
        self.direction = 1
        self.rect.bottom = 0

        if self.up_down:
            self.direction = -1
            self.rect.top = self.s.screen_size[1]

        self.rect.centerx = self.position 

        #float of y coordinate
        self.centery = float(self.rect.centery)


    def update(self, chrome):
        #update mask
        self.mask = pg.mask.from_surface(self.image, 127)
        #update xy coordinate changes
        self.mvmtratio = self.s.by_speed * self.s.dt * self.direction
        self.centery += self.mvmtratio
        self.rect.centery = self.centery

        if self.rect.top > self.s.screen_size[1] or (
                            self.rect.bottom < 0):
            self.kill()


class HomingPurple(pg.sprite.Sprite):
    """Homing Purple spawns in a random location and homes towards chrome"""
    def __init__(self, s):
        super().__init__()
        self.s = s
        opera_img = pg.image.load(path.join(img_dir, 'opr.png')
                                   ).convert_alpha()
        self.image = pg.transform.smoothscale(opera_img, (
            s.hp_size, s.hp_size))
        self.rect = self.image.get_rect()
        self.radius = int(self.s.hp_size / 2) -1

        #for movement
        self.accel_rate = self.s.hp_accel_rate
        self.xvel = 0
        self.yvel = 0
        self.update_accel_time = 0
        self.craziness = choice([0.95, 0.97, 0.99])

        #location of hp
        self.choice_position = [(self.s.screen_size[0]+25,
                                 self.s.screen_size[1]/2),
                                (-25,self.s.screen_size[1]/2)]
        self.rect.center = choice(self.choice_position)
        
        #float of xy coordinate
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)

    def update(self, chrome):
        #update mask
        self.mask = pg.mask.from_surface(self.image, 127)
        
        #update xy coordinate changes
        self.get_vector(chrome)
        now = pg.time.get_ticks()
        if now - self.update_accel_time > 50:
            self.update_accel_time = now
            self.xvel = (self.vector.x + self.xvel) * self.craziness
            self.yvel = (self.vector.y + self.yvel) * self.craziness
        self.centerx += (self.xvel + ((self.vector[0]/2)))
        self.centery += (self.yvel + ((self.vector[1]/2)))
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

    def get_vector(self, chrome):
        vector = pg.math.Vector2(chrome.rect.centerx - self.rect.centerx,
                                 chrome.rect.centery - self.rect.centery)
        self.vector = vector.normalize() / self.accel_rate
        
class Coin(pg.sprite.Sprite):
    """Fruit shifts every collision with chrome and awards points"""
    def __init__(self, s, all_sprites, coins_group):
        super().__init__()
        self.s = s
        coin_img = pg.image.load(path.join(img_dir, 'coin.png')
                                   ).convert_alpha()
        self.image = pg.transform.smoothscale(coin_img, (
            s.coin_size, s.coin_size))
        self.rect = self.image.get_rect()
        self.radius = int(self.s.coin_size / 2) -1

        #randrange spawn attributes
        x = randint(10, s.screen_size[0]-10)
        y = randint(10, s.screen_size[1]-10)
        self.position = (x, y)
        self.rect.center = self.position

        #timer
        self.timer = pg.time.get_ticks()
        self.add(all_sprites, coins_group)
        

    def update(self, chrome):
        now = pg.time.get_ticks()
        if now - self.timer >= self.s.coin_timer:
            self.timer = now
            self.move()

    def reset_timer(self):
        self.timer = pg.time.get_ticks()

    def move(self):
        x = randint(10, self.s.screen_size[0]-10)
        y = randint(10, self.s.screen_size[1]-10)
        self.position = (x, y)
        self.rect.center = self.position

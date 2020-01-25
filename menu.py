import pygame as pg
import random


def update_menu(screen, menu_screen, text_color,
                upgrades_group, screen_size, se):

    screen.blit(menu_screen, (0,0))
    screen.fill((220,220,220)) ##
    for i in range(0,3):
        upgrade_rect = pg.Surface((200, 200))
        upgrade_rect.fill((255,255,255))
        rect = upgrade_rect.get_rect()
        rect.center = ((300 + (i * 300)),
                            screen_size[1] / 2)
        screen.blit(upgrade_rect, rect)
    #blit CHOOSE YOUR UPGRADE
    text = write('CHOOSE YOUR UPGRADE', text_color, 40)
    text_rect = text.get_rect()
    text_rect.center = (screen_size[0]/2, screen_size[1]/4 - 50)
    screen.blit(text, text_rect)
    #blit spacebar to select
    text = write('(Spacebar to Select)', text_color, 30)
    text_rect = text.get_rect()
    text_rect.center = (screen_size[0]/2, screen_size[1]/4)
    screen.blit(text, text_rect)
    
    se.show_upgrade_text(screen, upgrades_group,
                         text_color, screen_size)
    upgrades_group.draw(screen)

    for i in range(0,3):
        upgrade_rect = pg.Surface((200, 200))
        rect = upgrade_rect.get_rect()
        rect.center = ((300 + (i * 300)),
                            screen_size[1] / 2)
        pg.draw.rect(screen, (0,0,0), rect, 2)
    pg.draw.rect(screen, (0, 255, 255), se, 5)
    pg.display.flip()


def write(text, text_color, font_size):
    font = pg.font.Font(pg.font.match_font('arial'), font_size)
    text = font.render(str(text), True, text_color)
    return text

def check_menu_events(se, s, upgrades_group):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if len(upgrades_group) == 3:
                if event.key == pg.K_RIGHT:
                    se.move_right()
                elif event.key == pg.K_LEFT:
                    se.move_left()
            if event.key == pg.K_SPACE:
                if not len(upgrades_group) > 1:
                    s.game_start = True
                    break
                    selected = se.position
                for upgrade in upgrades_group:
                    if upgrade.i == se.position:
                        upgrade.effect_effect(s)
                    else: upgrade.kill()

def spawn_upgrades(Upgrade, ug_list, screen_size, upgrade_img,
                   upgrades_group):
    ug_sample = random.sample(ug_list, 3)
    for i in range(0,3):
        upgrade = Upgrade(i, screen_size, upgrade_img,
                                    ug_sample[i])
        upgrade.add(upgrades_group)
        


class Upgrade(pg.sprite.Sprite):

    def __init__(self, i, screen_size, upgrade_img,
                                    ug_type):
        super().__init__()

        self.type = ug_type
        self.i = i
        self.image = upgrade_img[self.type]
        self.rect = self.image.get_rect()
        self.rect.center = ((300 + (self.i * 300)),
                            screen_size[1] / 2)

        self.upgrade_texts = {}
        self.upgrade_texts['acceleration'] = 'Increase Acceleration'
        self.upgrade_texts['size'] = 'Make Chrome Smaller'
        self.upgrade_texts['rotation'] = 'Make Chrome Spin (useless)'
        self.upgrade_texts['inertia'] = 'Better Control (Less Inertia)'
        self.upgrade_texts['life'] = 'Extra Life'
        self.upgrade_texts['life2'] = 'Extra Life'
        self.text = self.upgrade_texts[self.type]

    def effect_effect(self, s):
        if self.type == 'size':
            i = 'size'
            s.chrome_image = 'smallchrome.png'
            s.chrome_radius = 30
            
        elif self.type == 'acceleration':
            i = 'acceleration'
            s.accel_ratio = 0.05

        elif self.type == 'rotation':
            i = 'rotation' 
            s.do_i_rotate = True

        elif self.type == 'inertia':
            i = 'inertia' 
            s.inertia = 3
            
        elif self.type == 'life':
            i = 'life' 
            s.lives += 1

        elif self.type == 'life2':
            i = 'life2' 
            s.lives += 1
            
        self.upgrade_texts[i] = 'Press Spacebar to Begin!'
        s.ug_list.remove(i)


class Selector():
    def __init__(self, screen_size):
        self.screen_size = screen_size
        self.position = 1
        self.rect = pg.Rect((0, 0), (220, 220))
        self.rect.center = ((300 + (self.position * 300)),
                            self.screen_size[1] / 2)

    def move_right(self):
        if self.position <= 1:
            self.position += 1
            self.rect.center = ((300 + (self.position * 300)),
                            self.screen_size[1] / 2)

    def move_left(self):
        if self.position >= 1:
            self.position -= 1
            self.rect.center = ((300 + (self.position * 300)),
                            self.screen_size[1] / 2)

    def show_upgrade_text(self, screen, upgrades_group,
                     text_color, screen_size):
        for upgrade in upgrades_group:
            if self.position == upgrade.i:
                text = upgrade.upgrade_texts[upgrade.type]
                text_rendered = write(text, text_color, 30)
                rect = text_rendered.get_rect()
                rect.center = (300 + (self.position * 300),
                               0.7 * screen_size[1])
                screen.blit(text_rendered, rect)





        
        
        

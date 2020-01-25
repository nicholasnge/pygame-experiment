import sys
import pygame as pg
import settings as sets
import eventchecker
import objects as obj
import menu as m
from os import path


def run_game():
    #make a screen
    pg.init()
    s = sets.Settings()
    screen = pg.display.set_mode(s.screen_size)

    #assets
    img_dir = path.join(path.dirname(__file__), 'img')

    bg_img = pg.image.load(
            path.join(img_dir, 'bg2.png')).convert_alpha()
    
    menu_screen = pg.image.load(
            path.join(img_dir, 'menu.jpg')).convert()
    upgrade_img = {}
    for i in s.ug_list:
        upgrade_img[i] = pg.image.load(path.join(
        img_dir, 'upgrade_' + i + '.png')).convert_alpha()

    #bg_img = pg.transform.scale(bg_img, (s.screen_size))
    pg.display.set_caption("My Amazing Game")

    l = sets.Leveller(s.level_duration)
    all_sprites = pg.sprite.Group()
    slowred = pg.sprite.Group()
    bigyellow = pg.sprite.Group()
    homingpurple = pg.sprite.Group()
    upgrades_group = pg.sprite.Group()
    coins_group = pg.sprite.Group()
    #start sequence
    while True:

        if s.game_start == False:
            m.spawn_upgrades(m.Upgrade, s.ug_list, s.screen_size,
                           upgrade_img, upgrades_group)
            se = m.Selector(s.screen_size)

        while s.game_start == False:
        #upgrade menu/start menu should be right here
            s.dt = s.clock.tick(s.FPS)/1000
            m.check_menu_events(se, s, upgrades_group)
            m.update_menu(screen, menu_screen,
                          s.black, upgrades_group, s.screen_size, se)


        if s.game_start == True:
            #initialise
            upgrades_group.empty()
            eventchecker.restart(all_sprites)
            s.load_level(s.level)
            chrome = obj.Chrome(screen, s)
            coin = obj.Coin(s, all_sprites, coins_group)
            all_sprites.add(chrome)
            l.reset(s.level_duration)

    #main loop
        while s.game_start == True:

            pg.display.set_caption("{:.2f}".format(s.clock.get_fps()))

            s.dt = s.clock.tick(s.FPS)/1000
            l.check_time(s, s.level, s.score)
            obj.spawn(s, all_sprites, slowred, bigyellow, homingpurple)
            eventchecker.check_events(screen, chrome, slowred, bigyellow,
                                      homingpurple, coins_group, s)
            all_sprites.update(chrome)
            eventchecker.update_screen(screen, s.gray, all_sprites,
                s.black, l.second_counter, s.screen_size, bg_img, s.score)
            #leveler check gamestart, if true count, if false break



run_game()

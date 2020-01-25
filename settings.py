import pygame as pg

#apparently lets me do font
pg.init()

class Settings():

    def __init__(self):
        #colors
        self.green = (164,243,89)
        self.gray = (200,200,200)
        self.red = (170, 20, 54)
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)

        #leveller
        self.level = 1
        self.score = 0

        #essentials
        self.screen_size = (1200,650)
        self.dt = 0
        self.clock = pg.time.Clock()
        self.FPS = 120
        self.game_start = False
        self.level_duration = 10
        self.ug_list = ['size','acceleration','rotation',
                        'inertia','life','life2']

        #coin
        self.coin_size = 50
        self.coin_points = 10
        self.coin_timer = 8000

        #chrome
        self.accel_ratio = 0.02
        self.inertia = 1
        self.max_accel = 5
        self.bounce_accellost = -0.75
        self.lives = 1
        self.mvmtratio = 240
        self.chrome_rotate = 3
        self.chrome_image = 'chromeicon.png'
        self.chrome_radius = 50
        self.do_i_rotate = False

        
    def restore_gamestart_defaults(self):
        """restores all variable settings, activate when chrome
            lives == 0"""
        #essentials
        self.game_start = False
        self.level = 1
        self.ug_list = ['size','acceleration','rotation',
                        'inertia','life','life2']
        self.score = 0
        
        #chrome
        self.accel_ratio = 0.02
        self.inertia = 1
        self.max_accel = 5
        self.bounce_accellost = -0.75
        self.lives = 1
        self.mvmtratio = 240
        self.chrome_rotate = 3
        self.chrome_image = 'chromeicon.png'
        self.chrome_radius = 50
        self.do_i_rotate = False

    def load_level(self, level):
        if level == 1:
            #slowred settings
            self.sr = True
            self.sr_size = 40
            self.sr_speed = 120
            self.sr_oldtime = -3000
            self.sr_newtime = 0
            self.sr_spawnfreq = 1000

            self.by = False
            self.hp = False

            #level duration
            self.level_duration = 30
            self.coin_points = 10

        if level == 2:
            #slowred settings
            self.sr = True
            self.sr_size = 40
            self.sr_speed = 120
            self.sr_oldtime = -3000
            self.sr_newtime = 0
            self.sr_spawnfreq = 1000

            #bigyellow settings
            self.by = True
            self.by_size = 200
            self.by_speed = 30
            self.by_oldtime = 0
            self.by_newtime = 0
            self.by_spawnfreq = 5000

            self.hp = False
            
            #level duration
            self.level_duration = 60
            self.coin_points = 20

        if level == 3:
            #slowred settings
            self.sr = False
            self.sr_size = 40
            self.sr_speed = 120
            self.sr_oldtime = -3000
            self.sr_newtime = 0
            self.sr_spawnfreq = 1000

            #bigyellow settings
            self.by = True
            self.by_size = 200
            self.by_speed = 60
            self.by_oldtime = 0
            self.by_newtime = 0
            self.by_spawnfreq = 5000

            #homingpurple settings
            self.hp = True
            self.hp_size = 50
            self.hp_accel_rate = 5 #inverse, ie. 1/5
            self.hp_oldtime = -20000
            self.hp_newtime = 0
            self.hp_spawnfreq = 20000
            
            #level duration
            self.level_duration = 60
            self.coin_points = 30

        if level == 4:
            #slowred settings
            self.sr = True
            self.sr_size = 120
            self.sr_speed = 400
            self.sr_oldtime = -3000
            self.sr_newtime = 0
            self.sr_spawnfreq = 2000

            #bigyellow settings
            self.by = True
            self.by_size = 200
            self.by_speed = 60
            self.by_oldtime = 0
            self.by_newtime = 0
            self.by_spawnfreq = 5000

            #homingpurple settings
            self.hp = True
            self.hp_size = 50
            self.hp_accel_rate = 5 #inverse, ie. 1/5
            self.hp_oldtime = -20000
            self.hp_newtime = 0
            self.hp_spawnfreq = 20000
            
            #level duration
            self.level_duration = 60
            self.coin_points = 40


        

class Leveller():
    def __init__(self, level_duration):
        self.level_duration = level_duration
        self.second_counter = self.level_duration
        self.time = pg.time.get_ticks()
        
        
    def check_time(self, s, Level, score):
        now = pg.time.get_ticks()
        if now - self.time >= 1000:
            self.time = now
            self.second_counter -= 1
            score += 10
            if self.second_counter == 0:
                s.level += 1
                s.game_start = False
                self.second_counter = self.level_duration

    def reset(self, level_duration):
        self.level_duration = level_duration
        self.second_counter = self.level_duration
        self.time = pg.time.get_ticks()
                




        
        

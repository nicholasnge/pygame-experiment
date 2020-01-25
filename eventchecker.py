#event checker
import pygame as pg
import sys

def check_events(screen, chrome, slowred, bigyellow,
                 homingpurple, coins_group, s):
    for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
                
            elif event.type == pg.KEYDOWN:
                check_keydown_events(chrome, event)
                    
            elif event.type == pg.KEYUP:
                check_keyup_events(chrome, event)

    #check collisions
    check_collisions(screen, chrome, slowred, bigyellow,
                     homingpurple, coins_group, s)


def check_keydown_events(chrome, event):
    if event.key == pg.K_RIGHT:
        chrome.rightflag = True
    elif event.key == pg.K_LEFT:
        chrome.leftflag = True
    elif event.key == pg.K_UP:
        chrome.upflag = True
    elif event.key == pg.K_DOWN:
        chrome.downflag = True

def check_keyup_events(chrome, event):
    if event.key == pg.K_RIGHT:
        chrome.rightflag = False
    elif event.key == pg.K_LEFT:
        chrome.leftflag = False
    elif event.key == pg.K_UP:
        chrome.upflag = False
    elif event.key == pg.K_DOWN:
        chrome.downflag = False


def check_collisions(screen, chrome, slowred, bigyellow,
                     homingpurple, coins_group, s):
    collected = pg.sprite.spritecollide(chrome, coins_group,
                False, pg.sprite.collide_circle)
    for coin in collected:
        s.score += s.coin_points
        coin.reset_timer()
        coin.move()
        
    #check sr collisions
    if pg.sprite.spritecollide(chrome, slowred,
                False, pg.sprite.collide_circle):
        chrome.lives -= 1
        if chrome.lives <= 0:
            s.restore_gamestart_defaults()
            pg.time.wait(1000)
        else:
            text = write(str(chrome.lives) + ' lives remaining',
                         s.black, 40)
            text_rect = text.get_rect()
            text_rect.center = (s.screen_size[0] /2,
                                s.screen_size[1] /2)
            screen.fill((220,220,220))
            screen.blit(text, text_rect)
            slowred.draw(screen)
            bigyellow.draw(screen)
            homingpurple.draw(screen)
            pg.display.flip()
            for group in [slowred, bigyellow, homingpurple]:
                for sprite in group:
                    sprite.kill()
            s.lives = 1
            pg.time.wait(1000)
            
    #check by collisions
    elif pg.sprite.spritecollide(chrome,
                                 bigyellow, False):
        real_GG = pg.sprite.spritecollide(chrome, bigyellow,
                                 False, pg.sprite.collide_mask)
        if real_GG:
            chrome.lives -= 1
            if chrome.lives <= 0:
                s.restore_gamestart_defaults()
                pg.time.wait(1000)
            else:
                text = write(str(chrome.lives) + ' lives remaining',
                             s.black, 40)
                text_rect = text.get_rect()
                text_rect.center = (s.screen_size[0] /2,
                                    s.screen_size[1] /2)
                screen.fill((220,220,220))
                screen.blit(text, text_rect)
                slowred.draw(screen)
                bigyellow.draw(screen)
                homingpurple.draw(screen)
                pg.display.flip()
                for group in [slowred, bigyellow, homingpurple]:
                    for sprite in group:
                        sprite.kill()
                s.lives = 1
                pg.time.wait(1000)

    #check hp collisions
    elif pg.sprite.spritecollide(chrome,
                                 homingpurple, False):
        real_GG = pg.sprite.spritecollide(chrome, homingpurple,
                                 False, pg.sprite.collide_mask)
        if real_GG:
            chrome.lives -= 1
            if chrome.lives <= 0:
                s.restore_gamestart_defaults()
                pg.time.wait(1000)
            else:
                text = write(str(chrome.lives) + ' lives remaining',
                             s.black, 40)
                text_rect = text.get_rect()
                text_rect.center = (s.screen_size[0] /2,
                                    s.screen_size[1] /2)
                screen.fill((220,220,220))
                screen.blit(text, text_rect)
                slowred.draw(screen)
                bigyellow.draw(screen)
                homingpurple.draw(screen)
                pg.display.flip()
                for group in [slowred, bigyellow, homingpurple]:
                    for sprite in group:
                        sprite.kill()
                s.lives = 1
                pg.time.wait(1000)
                
def update_screen(screen, bg_color, all_sprites, text_color,
                  time, screen_size, bg_img, score):
    screen.blit(bg_img, (0,0))
    screen.fill((220,220,220)) ##
    all_sprites.draw(screen)
    
    #blit time
    screen.blit(write(time, text_color, 40),
                (10, 10))
    
    #blit score
    text = write('Score: ' + str(score), text_color, 40)
    text_rect = text.get_rect()
    text_rect.center = (screen_size[0] /2,
            50)
    screen.blit(text, text_rect)
    
    pg.display.flip()
    

def restart(all_sprites):
    for sprite in all_sprites:
        sprite.kill()


def write(text, text_color, font_size):
    font = pg.font.Font(pg.font.match_font('arial'), font_size)
    text = font.render(str(text), True, text_color)
    return text
            

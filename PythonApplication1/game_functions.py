import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien

def fire_bullet(ai_settings, screen, ship, bullets):
    #创建一颗子弹并把其加入分组
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets):
    bullets.update()
    #删除已经消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    #如果子弹击中外星人删除相应子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_point * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        #提高等级
        stats.level += 1 
        sb.prep_level()
        #删除现有子弹并新建一群外星人
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings,screen,ship,aliens,stats)

def check_high_score(stats, sb):
    #检查是否诞生了新的最高得分
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def get_number_alien_x(ai_settings, alien_width):
    #计算每行可容纳多少外星人
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_alien_x = int(available_space_x / (2 * alien_width))
    return number_alien_x

def get_number_rows(ai_settings, ship_height, alien_height ,stats):
    #计算屏幕可容纳多少行外星人
    available_space_y = ai_settings.screen_height - (3 * alien_height) - ship_height 
    max_rows = int (available_space_y / (2 * alien_height))
    if stats.level + 2 < max_rows:
        number_rows = (2 + stats.level) % max_rows
    else:
        number_rows = max_rows
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    #创造外星人
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens, stats):
    #外星人间距为外星人的宽度
    alien = Alien(ai_settings, screen)
    number_alien_x = get_number_alien_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height, stats)

    #创建外星人群
    for row_number in range(number_rows):
        for alien_number in range(number_alien_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_fleet_edges(ai_settings, aliens):
    #有外星人到达边缘时采取相应的措施
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    #整体外星人下移并改变他们的方向
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, stats ,screen, sb, ship, aliens, bullets):
    #响应被外星人撞到的飞船
    if stats.ships_left > 0:
        stats.ships_left -= 1 

        #更新记分牌
        sb.prep_ships()
        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        #创建一群新的外星人，并将飞船放到屏幕底部中央
        create_fleet(ai_settings,screen,ship,aliens,stats)
        ship.center_ship()
        #暂停
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_alien_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets):
    #检查是否有外星人到了屏幕底部
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #像飞船被撞倒一样处理
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
            break

def update_aliens(ai_settings,stats,screen,sb,ship,aliens,bullets):
    #检查是否有外星人位于屏幕边缘，整体更新外星人位置
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    #监测外星人和飞船间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings,stats,screen,sb,ship,aliens,bullets)
    check_alien_bottom(ai_settings,stats,screen,sb,ship,aliens,bullets)

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    #响应按键
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)

def check_keyup_events(event, ship):
    #响应松开
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    #每次循环重绘屏幕
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    #点击play按钮更新游戏
    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)

    if button_clicked and not stats.game_active:
        #重置游戏设置
        ai_settings.initialize_dynamic_settings()


        #隐藏光标
        pygame.mouse.set_visible(False)

        stats.reset_stats()
        stats.game_active = True

        #重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        #创建一群新的外星人并让飞船居中
        create_fleet(ai_settings, screen, ship, aliens, stats)
        ship.center_ship()

def update_screen(ai_setting, screen, stats, sb, ship, aliens, bullets, play_button):
    #更新屏幕上的图像，并切换到新屏幕
    #每次更新都重绘屏幕
    screen.fill(ai_setting.bg_color)

    #显示得分
    sb.show_score()

    # 在飞船和外星人后面绘制所以子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)

    #如果游戏处于非活动状态，就绘制 play 按钮
    if not stats.game_active:
        play_button.draw_button()

    #让最近绘制的屏幕可见
    pygame.display.flip()


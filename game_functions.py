# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     game_functions
   Description :    游戏方法模块 -- 游戏所有方法
   Author :       HoleLin
   date：          2019/4/11
-------------------------------------------------
   Change Activity:
                   2019/4/11:
-------------------------------------------------
"""
import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def check_events(ai_settings, screen, ship, bullets):
    # 监视键盘和鼠标事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            chek_keyup_events(event, ship)


def chek_keyup_events(event, ship):
    """ 响应松开 """
    if event.key == pygame.K_RIGHT:
        # 向右移动飞船
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        # 向右移动飞船
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        # 向上移动飞船
        ship.moving_up = False

    elif event.key == pygame.K_DOWN:
        # 向下移动飞船
        ship.moving_down = False


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """ 响应按下 """
    if event.key == pygame.K_RIGHT:
        # 向右移动飞船
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        # 向右移动飞船
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        # 向上移动飞船
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        # 向下移动飞船
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, bullets, screen, ship)
    elif event.key == pygame.K_q:
        sys.exit()


def fire_bullet(ai_settings, bullets, screen, ship):
    """ 如果没到达限制,就发射一颗子弹 """
    if len(bullets) < ai_settings.bullets_allowed:
        # 创建一颗子弹,并将其加入到编组bullets中
        new_bullets = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullets)


def update_screen(ai_setting, screen, ship, aliens, bullets):
    """ 更新屏幕上的图像,并且换到新屏幕 """
    # 每次循环是都重绘屏幕
    screen.fill(ai_setting.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blit_ship()
    # alien.blit_alien()
    aliens.draw(screen)
    # 让最近的绘制的屏幕可见
    pygame.display.flip()


def update_bullets(ai_settings, screen, ship, aliens, bullets):
    bullets.update()
    # 删除已经消失的子弹
    for bullet in bullets:
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, aliens, bullets, screen, ship)


def check_bullet_alien_collisions(ai_settings, aliens, bullets, screen, ship):
    """ 相应子弹和外星人的碰撞 """
    # 检查是否有子弹击中外星人
    # 如果是这样,就删除相应的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if len(aliens) == 0:
        # 删除现有子弹并新建一群外星人
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)


def update_aliens(ai_settings, status, screen, ship, aliens, bullets):
    """更新外星人群所有外星人的位置"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # 检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, status, screen, ship, aliens, bullets)

    check_aliens_bottom(ai_settings, status, screen, ship, aliens, bullets)


def create_fleet(ai_settings, screen, ship, aliens):
    """创建外星人群"""
    # 创建一个外星人,并计算一行可容纳多少个外星人
    # 外星人间距为外星人宽度
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    number_aliens_x = get_number_aliens_x(ai_settings, alien_width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    # 创建第一行外星人
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            # 创建一个外星人并将其加入当前行
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """创建外星人"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def get_number_aliens_x(ai_settings, alien_width):
    """计算一行可以容纳多少外星人"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """计算屏幕可容纳多少外星人"""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def change_fleet_direction(ai_settings, aliens):
    """ 将整个外星人向下一栋"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_fleet_edges(ai_settings, aliens):
    """有外星人到达边缘时采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def ship_hit(ai_settings, status, screen, ship, aliens, bullets):
    """相应被外星人装到的飞船"""
    if status.ships_left > 0:
        status.ships_left -= 1
    else:
        status.game_active = False
    # 清空外星人列表和子弹列表
    aliens.empty()
    bullets.empty()
    # 创建一群新的外星人,并将飞船放到屏幕底端中央
    create_fleet(ai_settings, screen, ship, aliens)
    ship.ship_center()

    # 暂停
    sleep(0.5)


def check_aliens_bottom(ai_settings, status, screen, ship, aliens, bullets):
    """检查是否有外星人到达了屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, status, screen, ship, aliens, bullets)
            break

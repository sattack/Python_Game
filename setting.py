# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     setting
   Description :  游戏设置类 -- 常用初始化游戏外观和飞船速度的属性
   Author :       HoleLin
   date：          2019/4/11
-------------------------------------------------
   Change Activity:
                   2019/4/11:
-------------------------------------------------
"""


class Setting():
    """ 存储<外星人入侵>的所有设置的类 """

    def __init__(self):
        """ 初始化游戏的设置 """
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        # 飞船的设置
        self.ship_speed_factor = 1.5
        self.ship_limit = 3
        # 设置子弹
        self.bullet_speed_factor = 3
        self.bullet_width = 500
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3

        # 外星人设置
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 30
        # fleet_direction为1 表示向右移动,-1表示向左移动
        self.fleet_direction = 1

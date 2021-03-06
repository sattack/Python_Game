# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     game_status
   Description :
   Author :       HoleLin
   date：          2019/4/12
-------------------------------------------------
   Change Activity:
                   2019/4/12:
-------------------------------------------------
"""


class GameStats():
    """跟踪游戏的统计信息"""

    def __init__(self, ai_settings):
        """初始化统计信息"""
        self.ai_setting = ai_settings
        self.reset_status()
        # 游戏刚启动是处于非活动状态
        self.game_active = False
        # 在任何情况下都不应重置最高得分
        self.high_score = 0

    def reset_status(self):
        """初始化在游戏运行期间可能变化的统计信息"""
        self.ship_left = self.ai_setting.ship_limit
        self.score = 0
        self.level = 1

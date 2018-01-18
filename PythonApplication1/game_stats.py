class GameStats():
    #游戏设置

    def __init__(self,ai_settings):
        #游戏基本设置
        self.ai_setttings = ai_settings
        self.reset_stats()
        self.game_active = False
        #在任何情况都不应该重置最高得分
        self.high_score = 0

    def reset_stats(self):
        #初始化游戏进行的可能的设置
        self.ships_left = self.ai_setttings.ship_limit
        self.score = 0
        self.level = 1
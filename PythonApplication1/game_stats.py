class GameStats():
    #������Ϸ��ͳ����Ϣ

    def __init__(self,ai_settings):
        #��ʼ��ͳ����Ϣ
        self.ai_setttings = ai_settings
        self.reset_stats()
        self.game_active = False
    def reset_stats(self):
        #��ʼ����Ϸ�������ڼ�仯��ͳ����Ϣ
        self.ships_left = self.ai_setttings.ship_limit
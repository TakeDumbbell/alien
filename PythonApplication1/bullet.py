import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):

    #�Էɴ������ӵ���Ĺ���
    def __init__(self,  ai_settings, screen, ship):
        #�ڷɴ�����λ�ô���һ���ӵ�����
        super(Bullet, self).__init__()
        self.screen = screen

        #�ڣ�0��0��������һ����ʾ�ӵ��ľ��Σ���������ȷ��λ��
        self.rect = pygame.Rect(0,0,ai_settings.bullet_width,ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        
        #�洢��С����ʾ�ӵ���λ��
        self.y = float(self.rect.y)
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        #�����ƶ��ӵ������±�ʾ�ӵ�λ�õ�С��ֵ
        self.y -= self.speed_factor
        #���±�ʾ�ӵ���rect��λ��
        self.rect.y = self.y

    def draw_bullet(self):
        #����Ļ�����ӵ�
        pygame.draw.rect(self.screen,self.color,self.rect)
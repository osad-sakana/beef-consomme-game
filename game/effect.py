import pygame


class Effect:
    def __init__(self, x, y, color, text=""):
        self.x = x
        self.y = y
        self.color = color
        self.text = text
        self.lifetime = 30  # フレーム数でのエフェクト表示時間
        self.alpha = 255  # 透明度

    def update(self):
        self.lifetime -= 1
        self.alpha = int(255 * (self.lifetime / 30))  # フェードアウト効果
        return self.lifetime > 0

    def draw(self, screen, font):
        if self.text:
            text_surface = font.render(self.text, True, self.color)
            text_surface.set_alpha(self.alpha)
            screen.blit(text_surface, (self.x, self.y))
        else:
            s = pygame.Surface((80, 40), pygame.SRCALPHA)
            pygame.draw.circle(s, (*self.color, self.alpha), (40, 20), 20)
            screen.blit(s, (self.x - 40, self.y - 20))

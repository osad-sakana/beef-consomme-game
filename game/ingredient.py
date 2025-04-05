import random
import pygame
from .constants import WIDTH, INGREDIENT_COLORS


class Ingredient:
    def __init__(self, ingredient):
        self.name = ingredient["name"]
        self.key = ingredient["key"]
        self.x = random.randint(50, WIDTH - 50)
        self.y = -50  # 画面上部から出現
        self.speed = random.randint(3, 6)
        self.width = 60
        self.height = 30
        self.color = INGREDIENT_COLORS[self.name]
        self.hit_effect = False
        self.hit_effect_timer = 0

    def update(self, slowdown_active):
        if slowdown_active:
            self.y += self.speed / 2
        else:
            self.y += self.speed

        if self.hit_effect:
            self.hit_effect_timer += 1
            if self.hit_effect_timer > 30:  # エフェクトは30フレーム表示
                self.hit_effect = False
                self.hit_effect_timer = 0

    def draw(self, screen, font):
        # 当たり判定の可視化
        hitbox = pygame.Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)

        # エフェクトの描画
        if self.hit_effect:
            pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), 30, 2)

        # 食材の描画
        pygame.draw.rect(screen, self.color, hitbox, border_radius=5)
        text = font.render(self.name, True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.x, self.y))
        screen.blit(text, text_rect)

    def is_in_pot_zone(self, pot_zone_y):
        return pot_zone_y - 20 < self.y < pot_zone_y + 20

    def trigger_hit_effect(self):
        self.hit_effect = True
        self.hit_effect_timer = 0

import pygame
import random
from .constants import WIDTH, INGREDIENTS


class Ingredient:
    def __init__(self, ingredient_type):
        self.type = ingredient_type
        self.name = INGREDIENTS[ingredient_type]['name']
        self.color = INGREDIENTS[ingredient_type]['color']
        self.key = INGREDIENTS[ingredient_type]['key']
        self.speed = 3  # 固定の速度
        self.score = 100  # 固定のスコア
        self.y = 0

        # キーに基づいてゾーンを決定
        key_to_zone = {
            100: 0,  # d: 肉、チーズ、魚
            102: WIDTH // 4,  # f: 野菜、果物
            106: WIDTH // 4 * 2,  # j: ハーブ、スパイス
            107: WIDTH // 4 * 3  # k: スープ
        }
        zone_x = key_to_zone[self.key]
        zone_width = WIDTH // 4
        # ゾーン内のランダムな位置に配置
        self.x = zone_x + random.randint(20, zone_width - 20)

    def update(self, slowdown_active):
        if slowdown_active:
            self.y += self.speed * 0.5
        else:
            self.y += self.speed

    def draw(self, screen, font):
        # 食材の円を描画
        pygame.draw.circle(screen, (50, 50, 50),
                           (int(self.x), int(self.y)), 20)

        # 食材名を色付きで描画
        text = font.render(self.name, True, self.color)
        text_rect = text.get_rect(center=(self.x, self.y))
        screen.blit(text, text_rect)

    def is_in_pot_zone(self, pot_zone_y):
        return self.y >= pot_zone_y - 20 and self.y <= pot_zone_y + 20

    def trigger_hit_effect(self):
        self.hit_effect = True
        self.hit_timer = 0

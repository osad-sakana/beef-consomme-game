import pygame
import random
import sys
import time

pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("ビーフコンソメゲーム")

clock = pygame.time.Clock()
pot_zone_y = height - 100  # 鍋の位置

score = 0
start_time = time.time()
game_duration = 30  # ゲーム時間（秒）
multiplier = 1
multiplier_end_time = 0
slowdown_active = False
slowdown_end_time = 0

# 食材の定義（名前と対応キー）
INGREDIENTS = [
    {"name": "肉", "key": pygame.K_m},     # Mキー
    {"name": "野菜", "key": pygame.K_v},     # Vキー
    {"name": "ハーブ", "key": pygame.K_h},   # Hキー
]


class Ingredient:
    def __init__(self, ingredient):
        self.name = ingredient["name"]
        self.key = ingredient["key"]
        self.x = random.randint(50, width - 50)
        self.y = -50  # 画面上部から出現
        self.speed = random.randint(3, 6)

    def update(self):
        if slowdown_active:
            self.y += self.speed / 2
        else:
            self.y += self.speed

    def draw(self, screen, font):
        text = font.render(self.name, True, (255, 255, 255))
        screen.blit(text, (self.x, self.y))


# エフェクトクラスを追加
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


ingredients_list = []
effects_list = []  # エフェクトを格納するリスト
spawn_timer = 0

# フォントファイルを読み込む
try:
    font = pygame.font.Font("PixelMplus12-Regular.ttf", 36)
    small_font = pygame.font.Font("PixelMplus12-Regular.ttf", 24)
except FileNotFoundError:
    print("フォントファイルが見つかりません。システムフォントを使用します。")
    font = pygame.font.SysFont(None, 36)
    small_font = pygame.font.SysFont(None, 24)

running = True
while running:
    dt = clock.tick(60) / 1000  # 秒単位のデルタタイム
    current_time = time.time()
    elapsed_time = current_time - start_time
    remaining_time = max(0, game_duration - elapsed_time)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # 旨味ブースト：Bキー
            if event.key == pygame.K_b:
                multiplier = 2
                multiplier_end_time = current_time + 5  # 5秒間有効
                effects_list.append(
                    Effect(width // 2, height // 2, (255, 255, 0), "旨味ブースト！"))
            # スープ冷却：Cキー
            elif event.key == pygame.K_c:
                slowdown_active = True
                slowdown_end_time = current_time + 5  # 5秒間有効
                effects_list.append(
                    Effect(width // 2, height // 2, (0, 200, 255), "スープ冷却！"))
            else:
                # 鍋ゾーン内にある食材に対して対応キーが押されたら加える
                matched = False
                for ing in ingredients_list:
                    if pot_zone_y - 20 < ing.y < pot_zone_y + 20:
                        if event.key == ing.key:
                            score += 10 * multiplier
                            # 成功エフェクトを追加
                            effects_list.append(
                                Effect(ing.x, ing.y, (0, 255, 0), "Good!"))
                            ingredients_list.remove(ing)
                            matched = True
                            break

                # 対応する食材がなかった場合（ミス）
                if not matched:
                    # ミスエフェクトを追加
                    effects_list.append(
                        Effect(width // 2, pot_zone_y, (255, 0, 0), "Miss!"))

    # 特殊効果の終了処理
    if multiplier != 1 and current_time > multiplier_end_time:
        multiplier = 1
    if slowdown_active and current_time > slowdown_end_time:
        slowdown_active = False

    # 食材を1秒ごとに出現させる
    spawn_timer += dt
    if spawn_timer > 1.0:
        spawn_timer = 0
        ingredients_list.append(Ingredient(random.choice(INGREDIENTS)))

    # 食材の更新処理
    for ing in ingredients_list[:]:
        ing.update()
        if ing.y > height:
            ingredients_list.remove(ing)

    # エフェクトの更新処理
    for effect in effects_list[:]:
        if not effect.update():
            effects_list.remove(effect)

    # 描画処理
    screen.fill((0, 0, 0))
    # 鍋ゾーン（画面下部）を描画
    pygame.draw.rect(screen, (50, 50, 200), (0, pot_zone_y, width, 10))

    for ing in ingredients_list:
        ing.draw(screen, font)

    # エフェクトの描画
    for effect in effects_list:
        effect.draw(screen, small_font)

    score_text = font.render(f"スコア: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    time_text = font.render(
        f"残り: {int(remaining_time)}秒", True, (255, 255, 255))
    screen.blit(time_text, (10, 50))
    if multiplier != 1:
        boost_text = font.render(f"旨味ブースト中 x{multiplier}", True, (255, 255, 0))
        screen.blit(boost_text, (10, 90))

    pygame.display.flip()

    if remaining_time <= 0:
        running = False

# ゲーム終了後、最終スコアを3秒間表示
end_time = time.time()
while time.time() - end_time < 3:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill((0, 0, 0))
    final_text = font.render(f"ゲーム終了! 最終スコア: {score}", True, (255, 255, 255))
    screen.blit(final_text, (width // 2 -
                final_text.get_width() // 2, height // 2))
    pygame.display.flip()

pygame.quit()

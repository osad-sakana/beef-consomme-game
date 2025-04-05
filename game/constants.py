import pygame

# 画面設定
WIDTH = 800
HEIGHT = 600
POT_ZONE_Y = HEIGHT - 100  # 鍋の位置

# ゲーム設定
GAME_DURATION = 30  # ゲーム時間（秒）
SPAWN_INTERVAL = 1.0  # 食材出現間隔（秒）
BOOST_DURATION = 5  # ブースト効果時間（秒）
SLOWDOWN_DURATION = 5  # スローダウン効果時間（秒）

# 食材の定義
INGREDIENTS = [
    {"name": "肉", "key": pygame.K_m},     # Mキー
    {"name": "野菜", "key": pygame.K_v},     # Vキー
    {"name": "ハーブ", "key": pygame.K_h},   # Hキー
]

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 50, 200)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
CYAN = (0, 200, 255)

# 食材の色
INGREDIENT_COLORS = {
    "肉": (200, 50, 50),      # 赤系
    "野菜": (50, 200, 50),     # 緑系
    "ハーブ": (200, 200, 50)    # 黄緑系
}

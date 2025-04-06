import pygame

# 画面設定
WIDTH = 800
HEIGHT = 600
POT_ZONE_Y = 500  # 鍋の位置

# ゲーム設定
GAME_DURATION = 30  # ゲーム時間（秒）
SPAWN_INTERVAL = 1.0  # 食材出現間隔（秒）
BOOST_DURATION = 5  # ブースト効果時間（秒）
SLOWDOWN_DURATION = 5  # スローダウン効果時間（秒）

# 食材の種類とキー
INGREDIENTS = {
    'meat': {
        'name': '肉',
        'color': (255, 100, 100),
        'key': 100  # d
    },
    'cheese': {
        'name': 'チーズ',
        'color': (255, 255, 100),
        'key': 100  # d
    },
    'fish': {
        'name': '魚',
        'color': (100, 100, 255),
        'key': 100  # d
    },
    'vegetable': {
        'name': '野菜',
        'color': (100, 255, 100),
        'key': 102  # f
    },
    'fruit': {
        'name': '果物',
        'color': (255, 100, 255),
        'key': 102  # f
    },
    'herb': {
        'name': 'ハーブ',
        'color': (100, 255, 100),
        'key': 106  # j
    },
    'spice': {
        'name': 'スパイス',
        'color': (255, 100, 100),
        'key': 106  # j
    },
    'soup': {
        'name': 'スープ',
        'color': (100, 100, 255),
        'key': 107  # k
    },
    'chocolate': {
        'name': 'チョコ',
        'color': (139, 69, 19),
        'key': 100  # d
    },
    'ice': {
        'name': '氷',
        'color': (200, 200, 255),
        'key': 102  # f
    },
    'sugar': {
        'name': '砂糖',
        'color': (255, 255, 255),
        'key': 106  # j
    },
    'milk': {
        'name': '牛乳',
        'color': (255, 255, 255),
        'key': 107  # k
    }
}

# ゾーンの定義
ZONES = {
    'left': {'key': pygame.K_d, 'x': 0, 'width': WIDTH // 4},
    'middle_left': {'key': pygame.K_f, 'x': WIDTH // 4, 'width': WIDTH // 4},
    'middle_right': {'key': pygame.K_j, 'x': WIDTH // 2, 'width': WIDTH // 4},
    'right': {'key': pygame.K_k, 'x': 3 * WIDTH // 4, 'width': WIDTH // 4}
}

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
CYAN = (0, 200, 255)

# 食材の色の定義
INGREDIENT_COLORS = {name: data['color'] for name, data in INGREDIENTS.items()}

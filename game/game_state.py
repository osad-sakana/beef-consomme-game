import time
from .constants import GAME_DURATION, BOOST_DURATION, SLOWDOWN_DURATION, INGREDIENTS


class GameState:
    def __init__(self):
        self.score = 0
        self.start_time = time.time()
        self.multiplier = 1
        self.multiplier_end_time = 0
        self.slowdown_active = False
        self.slowdown_end_time = 0
        self.running = True
        self.ingredients_count = {
            ing_type: 0 for ing_type in INGREDIENTS.keys()}
        self.is_normal_end = False

    def update(self, current_time):
        # 特殊効果の終了処理
        if self.multiplier != 1 and current_time > self.multiplier_end_time:
            self.multiplier = 1
        if self.slowdown_active and current_time > self.slowdown_end_time:
            self.slowdown_active = False

        # ゲーム時間のチェック
        elapsed_time = current_time - self.start_time
        if elapsed_time >= GAME_DURATION:
            self.running = False
            self.is_normal_end = True

    def activate_boost(self, current_time):
        self.multiplier = 2
        self.multiplier_end_time = current_time + BOOST_DURATION

    def activate_slowdown(self, current_time):
        self.slowdown_active = True
        self.slowdown_end_time = current_time + SLOWDOWN_DURATION

    def get_remaining_time(self):
        return max(0, GAME_DURATION - (time.time() - self.start_time))

    def add_ingredient(self, ingredient_type):
        if ingredient_type in self.ingredients_count:
            self.ingredients_count[ingredient_type] += 1

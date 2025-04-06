import pygame
import time
import random
import sys
import os
import openai
from dotenv import load_dotenv
from .constants import (
    WIDTH, HEIGHT, POT_ZONE_Y, INGREDIENTS,
    WHITE, BLACK, BLUE, YELLOW, INGREDIENT_COLORS
)
from .ingredient import Ingredient
from .effect import Effect
from .game_state import GameState
from .audio_manager import AudioManager
from .ui_manager import UIManager
from .recipe_generator import RecipeGenerator
from .event_handler import EventHandler

# .envファイルから環境変数を読み込む
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


class GameLoop:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()  # 音声初期化
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("ビーフコンソメゲーム")
        self.clock = pygame.time.Clock()

        # フォントの設定
        try:
            self.font = pygame.font.Font("PixelMplus12-Regular.ttf", 36)
            self.small_font = pygame.font.Font("PixelMplus12-Regular.ttf", 24)
        except FileNotFoundError:
            print("フォントファイルが見つかりません。システムフォントを使用します。")
            self.font = pygame.font.SysFont(None, 36)
            self.small_font = pygame.font.SysFont(None, 24)

        # SEの読み込み
        self.sounds = {}
        try:
            self.sounds = {
                "get_meat": pygame.mixer.Sound("assets/audio/se/get_meat.mp3"),
                "get_vegetable": pygame.mixer.Sound("assets/audio/se/get_vegetable.mp3"),
                "get_herb": pygame.mixer.Sound("assets/audio/se/get_herb.mp3"),
                "fall": pygame.mixer.Sound("assets/audio/se/fall.mp3")
            }
        except FileNotFoundError:
            print("SEファイルが見つかりません。SEは再生されません。")

        # BGMの読み込みと設定
        try:
            pygame.mixer.music.load("assets/audio/bgm/01-sougen.wav")
            pygame.mixer.music.set_volume(0.5)  # BGMの音量を50%に設定
        except FileNotFoundError:
            print("BGMファイルが見つかりません。BGMは再生されません。")

        # クリアBGMの読み込み
        try:
            self.clear_bgm = pygame.mixer.Sound(
                "assets/audio/bgm/03-clear.wav")
        except FileNotFoundError:
            print("クリアBGMファイルが見つかりません。クリアBGMは再生されません。")
            self.clear_bgm = None

        self.game_state = GameState()
        self.ingredients_list = []
        self.effects_list = []
        self.spawn_timer = 0
        self.audio_manager = AudioManager()
        self.ui_manager = UIManager()
        self.event_handler = EventHandler(
            self.game_state,
            self.ingredients_list,
            self.effects_list,
            self.audio_manager,
            self.ui_manager
        )

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state.running = False
            if event.type == pygame.KEYDOWN:
                self._handle_keydown(event)

    def _handle_keydown(self, event):
        current_time = time.time()

        if event.key == pygame.K_b:
            self.game_state.activate_boost(current_time)
            self.effects_list.append(
                Effect(WIDTH // 2, HEIGHT // 2, YELLOW, "旨味ブースト！"))
        elif event.key == pygame.K_c:
            self.game_state.activate_slowdown(current_time)
            self.effects_list.append(
                Effect(WIDTH // 2, HEIGHT // 2, (0, 200, 255), "スープ冷却！"))
        else:
            self._handle_ingredient_input(event)

    def _handle_ingredient_input(self, event):
        matched = False
        for ing in self.ingredients_list:
            if ing.is_in_pot_zone(POT_ZONE_Y) and event.key == ing.key:
                self.game_state.score += 10 * self.game_state.multiplier
                self.game_state.add_ingredient(ing.name)  # 食材の取得数をカウント
                ing.trigger_hit_effect()  # ヒットエフェクトを発動
                self.effects_list.append(
                    Effect(ing.x, ing.y, INGREDIENT_COLORS[ing.name], "Good!"))
                # 食材ごとに異なるSEを再生
                sound_name = f"get_{ing.name.lower()}"
                if sound_name in self.sounds:
                    self.sounds[sound_name].play()
                self.ingredients_list.remove(ing)
                matched = True
                break

        if not matched:
            self.effects_list.append(
                Effect(WIDTH // 2, POT_ZONE_Y, (255, 0, 0), "Miss!"))

    def update(self, dt):
        current_time = time.time()
        self.game_state.update(current_time)

        # 食材の生成
        self.spawn_timer += dt
        if self.spawn_timer > 0.5:  # 0.5秒に1回生成（2秒から0.5秒に変更）
            self.spawn_timer = 0
            # 食材の種類をランダムに選択
            ingredient_type = random.choice(list(INGREDIENTS.keys()))
            self.ingredients_list.append(Ingredient(ingredient_type))

        # 食材の更新
        for ing in self.ingredients_list[:]:
            ing.update(self.game_state.slowdown_active)
            if ing.y > HEIGHT:
                self.ingredients_list.remove(ing)

        # エフェクトの更新
        for effect in self.effects_list[:]:
            if not effect.update():
                self.effects_list.remove(effect)

    def draw(self):
        self.screen.fill(BLACK)

        # 鍋ゾーンの描画（より視覚的に分かりやすく）
        pygame.draw.rect(self.screen, BLUE, (0, POT_ZONE_Y - 20, WIDTH, 40), 2)
        pygame.draw.rect(self.screen, (0, 0, 100),
                         (0, POT_ZONE_Y - 20, WIDTH, 40))

        # 食材の描画
        for ing in self.ingredients_list:
            ing.draw(self.screen, self.font)

        # エフェクトの描画
        for effect in self.effects_list:
            effect.draw(self.screen, self.small_font)

        # UIの描画
        self._draw_ui()

        pygame.display.flip()

    def _draw_ui(self):
        score_text = self.font.render(
            f"スコア: {self.game_state.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        time_text = self.font.render(
            f"残り: {int(self.game_state.get_remaining_time())}秒", True, WHITE)
        self.screen.blit(time_text, (10, 50))

        if self.game_state.multiplier != 1:
            boost_text = self.font.render(
                f"旨味ブースト中 x{self.game_state.multiplier}", True, YELLOW)
            self.screen.blit(boost_text, (10, 90))

    def _generate_recipe(self):
        try:
            ingredients = self.game_state.ingredients_count
            prompt = f"""
            返答は全て日本語で行ってください。
            以下の食材を全て鍋に入れてビーフコンソメを入れます。
            どんな料理になるかを考えてください。その際に素材の偏りがある場合、それも加味して厳しく考えてください。
            肉: {ingredients['meat']}個
            野菜: {ingredients['vegetable']}個
            ハーブ: {ingredients['herb']}個

            またどんな料理の名前が適切かを考えてください。
            """

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "あなたは料理の専門家です。"},
                    {"role": "user", "content": prompt}
                ]
            )

            return response.choices[0].message.content
        except Exception as e:
            print(f"レシピ生成エラー: {e}")
            return "レシピの生成に失敗しました。"

    def show_game_over(self):
        # メインBGMを停止
        self.audio_manager.stop_bgm()

        # 正常終了の場合のみクリア画面を表示
        if not self.game_state.is_normal_end:
            pygame.quit()
            sys.exit()

        # クリアBGMを再生
        self.audio_manager.play_clear_bgm()

        # レシピ生成中の待機画面を表示
        self.ui_manager.draw_loading_screen()
        pygame.display.flip()

        # レシピを生成（非同期で実行）
        recipe = RecipeGenerator.generate_recipe(
            self.game_state.ingredients_count)

        # レシピ生成中は料理中の画面を表示し続ける
        while not recipe:
            self.ui_manager.draw_loading_screen()
            pygame.display.flip()
            pygame.time.delay(100)  # CPU使用率を抑えるため少し待機
            recipe = RecipeGenerator.generate_recipe(
                self.game_state.ingredients_count)

        # ゲームオーバー画面の表示
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # ESCキーで終了
                        pygame.quit()
                        sys.exit()

            self.ui_manager.draw_game_over(self.game_state, recipe)

    def run(self):
        self.audio_manager.play_bgm()

        while self.game_state.running:
            dt = self.clock.tick(60) / 1000
            self.event_handler.handle_events()
            self.update(dt)
            self.ui_manager.draw_game_screen(
                self.ingredients_list,
                self.effects_list,
                self.game_state
            )

        self.show_game_over()
        pygame.quit()

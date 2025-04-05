import pygame
import time
import random
import sys
from .constants import (
    WIDTH, HEIGHT, POT_ZONE_Y, INGREDIENTS,
    WHITE, BLACK, BLUE, YELLOW, INGREDIENT_COLORS
)
from .ingredient import Ingredient
from .effect import Effect
from .game_state import GameState


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
                ing.trigger_hit_effect()  # ヒットエフェクトを発動
                self.effects_list.append(
                    Effect(ing.x, ing.y, INGREDIENT_COLORS[ing.name], "Good!"))
                # 食材ごとに異なるSEを再生
                sound_name = f"get_{ing.name.lower()}"
                if sound_name in self.sounds:
                    try:
                        self.sounds[sound_name].play()
                    except Exception:
                        pass
                self.ingredients_list.remove(ing)
                matched = True
                break

        if not matched:
            self.effects_list.append(
                Effect(WIDTH // 2, POT_ZONE_Y, (255, 0, 0), "Miss!"))
            try:
                self.sounds["fall"].play()  # ミス時のSEを再生
            except Exception:
                pass

    def update(self, dt):
        current_time = time.time()
        self.game_state.update(current_time)

        # 食材の生成
        self.spawn_timer += dt
        if self.spawn_timer > 1.0:
            self.spawn_timer = 0
            self.ingredients_list.append(
                Ingredient(random.choice(INGREDIENTS)))

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

    def show_game_over(self):
        # メインBGMを停止
        try:
            pygame.mixer.music.stop()
        except Exception:
            pass

        # クリアBGMを再生
        if self.clear_bgm:
            try:
                self.clear_bgm.play()
                # BGMの長さを取得（ミリ秒）
                bgm_length = self.clear_bgm.get_length() * 1000
                end_time = time.time() * 1000 + bgm_length
            except Exception:
                end_time = time.time() * 1000 + 3000  # 3秒待機
        else:
            end_time = time.time() * 1000 + 3000  # 3秒待機

        while time.time() * 1000 < end_time:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill(BLACK)
            final_text = self.font.render(
                f"ゲーム終了! 最終スコア: {self.game_state.score}", True, WHITE)
            self.screen.blit(
                final_text, (WIDTH // 2 - final_text.get_width() // 2, HEIGHT // 2))
            pygame.display.flip()

    def run(self):
        try:
            pygame.mixer.music.play(-1)  # BGMをループ再生開始
        except Exception:
            pass
        while self.game_state.running:
            dt = self.clock.tick(60) / 1000
            self.handle_events()
            self.update(dt)
            self.draw()

        self.show_game_over()
        pygame.quit()

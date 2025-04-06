import pygame
import time
from .constants import WIDTH, HEIGHT, POT_ZONE_Y, WHITE, BLACK, BLUE, YELLOW, ZONES, INGREDIENTS


class UIManager:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("ビーフコンソメゲーム")

        # フォントの設定
        try:
            self.font = pygame.font.Font("PixelMplus12-Regular.ttf", 36)
            self.small_font = pygame.font.Font("PixelMplus12-Regular.ttf", 24)
            self.recipe_font = pygame.font.Font(
                "PixelMplus12-Regular.ttf", 20)  # レシピ用の小さめフォント
        except FileNotFoundError:
            print("フォントファイルが見つかりません。システムフォントを使用します。")
            self.font = pygame.font.SysFont(None, 36)
            self.small_font = pygame.font.SysFont(None, 24)
            self.recipe_font = pygame.font.SysFont(None, 20)

        # キー入力状態の追跡
        self.key_states = {
            pygame.K_d: False,
            pygame.K_f: False,
            pygame.K_j: False,
            pygame.K_k: False
        }

    def update_key_state(self, key, state):
        if key in self.key_states:
            self.key_states[key] = state

    def draw_game_screen(self, ingredients, effects, game_state):
        self.screen.fill(BLACK)

        # ゾーンの描画
        zone_width = WIDTH // 4
        zones = {
            'D': 0,
            'F': zone_width,
            'J': zone_width * 2,
            'K': zone_width * 3
        }

        for key, x in zones.items():
            # キーが押されている場合はゾーンをハイライト
            if self.key_states[getattr(pygame, f'K_{key.lower()}')]:
                pygame.draw.rect(self.screen, (100, 100, 100),
                                 (x, 0, zone_width, HEIGHT))
            else:
                pygame.draw.rect(self.screen, (50, 50, 50),
                                 (x, 0, zone_width, HEIGHT), 1)

            # キーの表示
            key_text = self.small_font.render(key, True, (150, 150, 150))
            self.screen.blit(key_text, (x + zone_width //
                             2 - key_text.get_width() // 2, HEIGHT - 30))

        # 鍋ゾーンの描画
        pygame.draw.rect(self.screen, BLUE, (0, POT_ZONE_Y - 20, WIDTH, 40), 2)
        pygame.draw.rect(self.screen, (0, 0, 100),
                         (0, POT_ZONE_Y - 20, WIDTH, 40))

        # 食材の描画
        for ing in ingredients:
            ing.draw(self.screen, self.font)

        # エフェクトの描画
        for effect in effects:
            effect.draw(self.screen, self.small_font)

        # UIの描画
        self._draw_ui(game_state)

        pygame.display.flip()

    def _draw_ui(self, game_state):
        score_text = self.font.render(f"スコア: {game_state.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        time_text = self.font.render(
            f"残り: {int(game_state.get_remaining_time())}秒", True, WHITE)
        self.screen.blit(time_text, (10, 50))

        if game_state.multiplier != 1:
            boost_text = self.font.render(
                f"旨味ブースト中 x{game_state.multiplier}", True, YELLOW)
            self.screen.blit(boost_text, (10, 90))

    def draw_loading_screen(self):
        self.screen.fill(BLACK)

        # 点滅するテキスト
        current_time = time.time()
        if int(current_time * 2) % 2 == 0:
            loading_text = self.font.render("料理中...", True, WHITE)
            self.screen.blit(loading_text, (WIDTH // 2 -
                             loading_text.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()

    def _wrap_text(self, text, max_width):
        words = text.split()
        lines = []
        current_line = []
        current_width = 0

        for word in words:
            word_width = self.recipe_font.size(word + ' ')[0]
            if current_width + word_width <= max_width:
                current_line.append(word)
                current_width += word_width
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_width = word_width

        if current_line:
            lines.append(' '.join(current_line))

        return lines

    def draw_game_over(self, game_state, recipe):
        self.screen.fill(BLACK)

        # 最終スコアの表示
        final_text = self.font.render(
            f"ゲーム終了! 最終スコア: {game_state.score}", True, WHITE)
        self.screen.blit(
            final_text, (WIDTH // 2 - final_text.get_width() // 2, HEIGHT // 4))

        # レシピの表示（折り返し処理）
        recipe_lines = []
        for line in recipe.split('\n'):
            wrapped_lines = self._wrap_text(line, WIDTH - 40)  # 左右に20pxの余白
            recipe_lines.extend(wrapped_lines)

        # レシピの表示位置を調整
        start_y = HEIGHT // 3
        max_lines = 10  # 最大表示行数
        if len(recipe_lines) > max_lines:
            recipe_lines = recipe_lines[:max_lines] + ["..."]  # 行数が多すぎる場合は省略

        for i, line in enumerate(recipe_lines):
            recipe_text = self.recipe_font.render(line, True, WHITE)
            self.screen.blit(recipe_text, (20, start_y + i * 25))  # 行間を25pxに設定

        # 終了メッセージの表示
        exit_text = self.small_font.render("終了するにはウィンドウを閉じてください", True, WHITE)
        self.screen.blit(
            exit_text, (WIDTH // 2 - exit_text.get_width() // 2, HEIGHT - 100))

        pygame.display.flip()

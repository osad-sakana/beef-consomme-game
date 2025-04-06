import pygame
import time
from .constants import WIDTH, HEIGHT, POT_ZONE_Y, INGREDIENT_COLORS, YELLOW
from .effect import Effect


class EventHandler:
    def __init__(self, game_state, ingredients_list, effects_list, audio_manager, ui_manager):
        self.game_state = game_state
        self.ingredients_list = ingredients_list
        self.effects_list = effects_list
        self.audio_manager = audio_manager
        self.ui_manager = ui_manager

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state.running = False
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event)
                # キーが押された状態を更新
                self.ui_manager.update_key_state(event.key, True)
            elif event.type == pygame.KEYUP:
                # キーが離された状態を更新
                self.ui_manager.update_key_state(event.key, False)

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
                self.game_state.add_ingredient(ing.type)
                ing.trigger_hit_effect()
                self.effects_list.append(
                    Effect(ing.x, ing.y, ing.color, "Good!"))

                sound_name = f"get_{ing.type}"
                self.audio_manager.play_sound(sound_name)

                self.ingredients_list.remove(ing)
                matched = True
                break

        if not matched:
            self.effects_list.append(
                Effect(WIDTH // 2, POT_ZONE_Y, (255, 0, 0), "Miss!"))
            self.audio_manager.play_sound("fall")

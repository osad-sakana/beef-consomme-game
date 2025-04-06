import pygame
import os


class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.clear_bgm = None
        self._load_sounds()
        self._load_bgm()

    def _load_sounds(self):
        try:
            self.sounds = {
                "get_meat": pygame.mixer.Sound("assets/audio/se/get_meat.mp3"),
                "get_vegetable": pygame.mixer.Sound("assets/audio/se/get_vegetable.mp3"),
                "get_herb": pygame.mixer.Sound("assets/audio/se/get_herb.mp3"),
                "fall": pygame.mixer.Sound("assets/audio/se/fall.mp3")
            }
        except FileNotFoundError:
            print("SEファイルが見つかりません。SEは再生されません。")

    def _load_bgm(self):
        try:
            pygame.mixer.music.load("assets/audio/bgm/01-sougen.wav")
            pygame.mixer.music.set_volume(0.5)
        except FileNotFoundError:
            print("BGMファイルが見つかりません。BGMは再生されません。")

        try:
            self.clear_bgm = pygame.mixer.Sound(
                "assets/audio/bgm/03-clear.wav")
        except FileNotFoundError:
            print("クリアBGMファイルが見つかりません。クリアBGMは再生されません。")
            self.clear_bgm = None

    def play_sound(self, sound_name):
        if sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except Exception:
                pass

    def play_bgm(self):
        try:
            pygame.mixer.music.play(-1)
        except Exception:
            pass

    def stop_bgm(self):
        try:
            pygame.mixer.music.stop()
        except Exception:
            pass

    def play_clear_bgm(self):
        if self.clear_bgm:
            try:
                self.clear_bgm.play()
            except Exception:
                pass

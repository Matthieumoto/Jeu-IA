import pygame as pg
import threading
from pygame.locals import *
import random
import time
import json
import os
import sys

class Settings:
    def __init__(self,game):
        self.game = game
        self.WIDTH = pg.display.Info().current_w
        self.HEIGHT = pg.display.Info().current_h
        self.SCALE_FACTOR_WIDTH = self.WIDTH / 1920
        self.SCALE_FACTOR_HEIGHT = self.HEIGHT / 1080
        self.music_volume = game.utils.settings_data["musique"]
        self.effect_volume = game.utils.settings_data["effects"]

    def update_settings(self):
        self.game.utils.settings_data["musique"] = self.music_volume
        self.game.utils.settings_data["effects"] = self.effect_volume
        self.game.utils.menu_sound.set_volume(self.music_volume)
        self.game.utils.effect_button_sound.set_volume(self.effect_volume)

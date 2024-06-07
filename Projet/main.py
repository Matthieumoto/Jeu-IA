from utils.settings import os, pg, sys, Settings
from utils.utils import Utils
from game.gamestate import GameState
from game.particles import Particules
from game.menu import Menu
from game.game_simulation import Game_simulation


class Main:
    def __init__(self):
        os.environ['SDL_VIDEO_WINDOW_POS'] = "50,50" # Cette chose étrange permet d'éviter que la fenetre soit bloquée en dehors de l'écran après avoir resize la fenetre dans les paramètres
        pg.init()
        self.screen = pg.display.set_mode((0,0),pg.FULLSCREEN)
        self.utils = Utils(self)
        self.utils.load_ressources()
        self.settings = Settings(self)
        self.settings.update_settings()
        self.particules = Particules(self)
        self.menu = Menu(self)
        self.simulation_game = Game_simulation(self)
        self.state = GameState({
            "main_menu": self.menu.main_menu,
            "parametre_menu": self.menu.settings,
            "audio_menu": self.menu.audio,
            "graphisme_menu" : self.menu.graphismes,
            "credits": self.menu.credits,
            "jeu_jeu": self.simulation_game.play,
            "jeu_win" : self.simulation_game.win
        })
        self.state.modify_state("main_menu")
        pg.mouse.set_visible(False)
        pg.display.set_caption("Simulation de qualité")
        self.FramePerSec = pg.time.Clock()
        self.FPS = 60

    def run(self):
        self.running = True
        while self.running:
            self.state.run()
        pg.quit()
        sys.exit()

if __name__ == "__main__":
    game = Main()
    game.run()
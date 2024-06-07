from utils.settings import pg, sys
from game.ui import Slider, Button, Bandeau

class Menu:
    def __init__(self, game) -> None:
        self.game = game
        self.game.utils.menu_sound.play(-1)

        #ca ca sert à la méthode fadein
        self.istransition = False
        sr = pg.display.get_surface().get_rect()
        self.veil = pg.Surface(sr.size)
        self.veil.fill((0, 0, 0))
    
    def fadein(self):
        #Pour la transition, on vien changer la transparence d'une surface
        clock = pg.time.Clock()

        for alpha in range(0, 90):
            clock.tick(120)
            self.veil.set_alpha(alpha)
            self.game.screen.blit(self.veil, (0, 0))
            pg.display.flip()
 
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
            self.game.utils.get_fps()
    
    def audio(self):
        #L'audio
        self.fadein()

        scale_factor_width = self.game.settings.SCALE_FACTOR_WIDTH
        scale_factor_height = self.game.settings.SCALE_FACTOR_HEIGHT

        menu_font_size = int(40 * scale_factor_width)
        menu_font = pg.font.Font(None, menu_font_size)
        menu_text = menu_font.render("Audio", True, (255, 255, 255))
        menu_rect = menu_text.get_rect(center=(self.game.settings.WIDTH // 2, self.game.settings.HEIGHT // 10))
        slider_width, slider_height = int(500 * scale_factor_width), int(50 * scale_factor_height)
        button_height = int(100 * scale_factor_width)
        button_width = int(25 * scale_factor_width)
        spacing = int(50 * scale_factor_width)

        boutton_retour = Button(self.game, "Retour", (400 * scale_factor_width, button_height - 50), int(50 * scale_factor_width),
                                (self.game.settings.WIDTH // 2 - 300 * scale_factor_width,
                                self.game.settings.HEIGHT // 2 + (button_height + spacing) * 2))
        boutton_sauvegarder = Button(self.game, "Sauvegarder", (400 * scale_factor_width, button_height - 50),
                                    int(50 * scale_factor_width),
                                    (self.game.settings.WIDTH // 2 + 300 * scale_factor_width,
                                    self.game.settings.HEIGHT // 2 + (button_height + spacing) * 2))

        confirm_bandeau = Bandeau(self.game, "Les paramètres ont bien été enregistrés !",
                                (500 * scale_factor_width, 70 * scale_factor_height),
                                int(30 * scale_factor_width), (
                                    (self.game.settings.WIDTH - 500 * scale_factor_width) // 2,
                                    30 * scale_factor_height),
                                (135, 206, 235), 2000)

        slider_volume_music = Slider(self.game.screen, (
        self.game.settings.WIDTH // 2, self.game.settings.HEIGHT // 3), slider_width, slider_height,
                                    button_width, 100, int(self.game.settings.music_volume * 100))
        slider_volume_effect = Slider(self.game.screen, (
        self.game.settings.WIDTH // 2, 2 * self.game.settings.HEIGHT // 3 - 150), slider_width, slider_height,
                                    button_width, 100, int(self.game.settings.effect_volume * 100))

        while True:
            self.game.screen.fill((0, 0, 0))
            self.game.screen.blit(menu_text,menu_rect)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                slider_volume_effect.event(event)
                slider_volume_music.event(event)
                boutton_retour.event(event)
                boutton_sauvegarder.event(event)

            self.game.particules.update_particles()
            slider_volume_music.draw()
            slider_volume_effect.draw()
            boutton_sauvegarder.draw()
            boutton_retour.draw()

            music_volume = slider_volume_music.slider_value
            effect_volume = slider_volume_effect.slider_value

            font_size = int(36 * scale_factor_width)
            font = pg.font.Font(None, font_size)
            music_text = font.render(f"Musique : {music_volume} %", True, (255, 255, 255))
            effect_text = font.render(f"Effets : {effect_volume} %", True, (255, 255, 255))

            music_rect = music_text.get_rect(topleft=(
            slider_volume_music.rect_x + slider_width + int(20 * scale_factor_width), slider_volume_music.rect_y))
            effect_rect = effect_text.get_rect(topleft=(
            slider_volume_effect.rect_x + slider_width + int(20 * scale_factor_width), slider_volume_effect.rect_y))

            self.game.screen.blit(music_text, music_rect)
            self.game.screen.blit(effect_text, effect_rect)

            if boutton_retour.is_clicked:
                self.game.state.lower_state()
                return
            if boutton_sauvegarder.is_clicked:
                confirm_bandeau.draw(3)
                self.game.settings.effect_volume = slider_volume_effect.slider_value / 100
                self.game.settings.music_volume = slider_volume_music.slider_value / 100
                self.game.settings.update_settings()
                self.game.utils.save_settings()
                boutton_sauvegarder.is_clicked = False

            self.game.utils.update_mouse()
            self.game.utils.get_fps()
            pg.display.flip()
            self.game.FramePerSec.tick(self.game.FPS)
    
    def credits(self):
        self.fadein()

        scale_factor_width = self.game.settings.SCALE_FACTOR_WIDTH
        scale_factor_height = self.game.settings.SCALE_FACTOR_HEIGHT

        font = pg.font.Font(None, int(40 * scale_factor_width))
        font2 = pg.font.Font(None, int(120 * scale_factor_width))


        text1 = font.render("Crédits", True, (255, 255, 255))
        rect1 = text1.get_rect(center=(self.game.settings.WIDTH // 2, self.game.settings.WIDTH // 10))

        text_adam = font2.render("Adam - UI, Menus et le jeu", True, (255, 255, 255))
        adam_rect = text_adam.get_rect(center=(self.game.settings.WIDTH // 2, self.game.settings.HEIGHT // 2))

        text_lucas = font2.render("Lucas - L'IA", True, (255, 255, 255))
        lucas_rect = text_lucas.get_rect(center=(self.game.settings.WIDTH // 2, self.game.settings.HEIGHT // 3))

        text_matthieu = font2.render("Matthieu - L'IA", True, (255, 255, 255))
        matthieu_rect = text_matthieu.get_rect(center=(self.game.settings.WIDTH // 2, self.game.settings.HEIGHT // 1.5))

        boutton_retour = Button(self.game, "Retour", (200 * scale_factor_width, 35 * scale_factor_height),
                                int(50 * scale_factor_width), (120 * scale_factor_width, 50 * scale_factor_height))

        while True:
            self.game.screen.fill((0, 0, 0))
            self.game.screen.blit(text1, rect1)
            self.game.screen.blit(text_adam, adam_rect)
            self.game.screen.blit(text_lucas, lucas_rect)
            self.game.screen.blit(text_matthieu, matthieu_rect)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                boutton_retour.event(event)
            boutton_retour.draw()
            if boutton_retour.is_clicked:
                self.game.state.lower_state()
                self.fadein()
                return
            self.game.particules.update_particles()
            self.game.utils.update_mouse()
            self.game.utils.get_fps()
            pg.display.flip()
            self.game.FramePerSec.tick(self.game.FPS)

    def main_menu(self):
        screen_height = self.game.settings.HEIGHT
        screen_width = self.game.settings.WIDTH
        scale_factor_width = self.game.settings.SCALE_FACTOR_WIDTH
        scale_factor_height = self.game.settings.SCALE_FACTOR_HEIGHT

        menu_font_size = int(100 * scale_factor_width)
        menu_font = pg.font.Font(None, menu_font_size)
        menu_text = menu_font.render("Simulation de qualité", True, (255, 255, 255))
        menu_rect = menu_text.get_rect(center=(screen_width // 2, screen_height // 10))

        button_height = int(100 * scale_factor_width)
        spacing = int(50 * scale_factor_width)

        boutton_jouer = Button(self.game, "Jouer", (500 * scale_factor_width, button_height), int(100 * scale_factor_width), (screen_width // 2, screen_height // 2 - 50))
        boutton_parametre = Button(self.game, "Paramètres", (500 * scale_factor_width, button_height), int(100 * scale_factor_width), (screen_width // 2, screen_height // 3 + (button_height + spacing) * 2))
        boutton_quitter = Button(self.game, "Quitter", (500 * scale_factor_width, button_height), int(100 * scale_factor_width), (screen_width // 2, screen_height // 3 + (button_height + spacing) * 3))
        boutton_credits = Button(self.game, "Crédits", (300 * scale_factor_width, int(75 * scale_factor_height)), int(50 * scale_factor_width), (int(screen_width - 170 * scale_factor_width), int(50 * scale_factor_height)))
        
        while True:
            self.game.screen.fill((0, 0, 0))

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                boutton_quitter.event(event)
                boutton_parametre.event(event)
                boutton_credits.event(event)
                boutton_jouer.event(event)

            self.game.particules.update_particles()
            self.game.screen.blit(menu_text, menu_rect)
            boutton_quitter.draw()
            boutton_parametre.draw()
            boutton_credits.draw()
            boutton_jouer.draw()
            if boutton_quitter.is_clicked:
                self.game.running = False
                return
            if boutton_parametre.is_clicked:
                self.game.state.modify_state("parametre_menu")
                return
            if boutton_jouer.is_clicked:
                self.game.state.modify_state("jeu_jeu")
                return
            if boutton_credits.is_clicked:
                self.game.state.modify_state("credits")
                return
            self.game.utils.update_mouse()
            self.game.utils.get_fps()
            pg.display.flip()
            self.game.FramePerSec.tick(self.game.FPS)
  
    def settings(self):
        self.fadein()

        screen_height = self.game.settings.HEIGHT
        screen_width = self.game.settings.WIDTH
        scale_factor_width = self.game.settings.SCALE_FACTOR_WIDTH
        scale_factor_height = self.game.settings.SCALE_FACTOR_HEIGHT

        menu_font_size = int(40 * scale_factor_width)
        menu_font = pg.font.Font(None, menu_font_size)
        menu_text = menu_font.render("Paramètres", True, (255, 255, 255))
        menu_rect = menu_text.get_rect(center=(screen_width // 2, screen_height // 10))

        button_height = int(100 * scale_factor_width)
        spacing = int(50 * scale_factor_width)

        boutton_son = Button(self.game, "Audio", (500 * scale_factor_width, button_height), int(100 * scale_factor_width), (screen_width // 2, screen_height // 3))
        boutton_graphismes = Button(self.game, "Graphismes", (500 * scale_factor_width, button_height), int(100 * scale_factor_width), (screen_width // 2, screen_height // 3 + button_height + spacing))
        boutton_retour = Button(self.game, "Retour", (400 * scale_factor_width, button_height - 50 * scale_factor_height), int(50 * scale_factor_width), (screen_width // 2, screen_height // 2 + (button_height + spacing) * 2))

        while True:
            self.game.screen.fill((0, 0, 0))
            self.game.screen.blit(menu_text, menu_rect)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                boutton_son.event(event)
                boutton_graphismes.event(event)
                boutton_retour.event(event)

            self.game.particules.update_particles()
            boutton_son.draw()
            boutton_graphismes.draw()
            boutton_retour.draw()

            if boutton_son.is_clicked:
                self.game.state.modify_state("audio_menu")
                return
            if boutton_graphismes.is_clicked:
                self.game.state.modify_state("graphisme_menu")
                return
            if boutton_retour.is_clicked:
                self.game.state.lower_state()
                self.fadein()
                return

            self.game.utils.get_fps()
            self.game.utils.update_mouse()
            pg.display.flip()
            self.game.FramePerSec.tick(self.game.FPS)
    
    def graphismes(self):
        self.fadein()

        screen_height = self.game.settings.HEIGHT
        screen_width = self.game.settings.WIDTH
        scale_factor_width = self.game.settings.SCALE_FACTOR_WIDTH
        scale_factor_height = self.game.settings.SCALE_FACTOR_HEIGHT

        menu_font_size = int(40 * scale_factor_width)
        menu_font = pg.font.Font(None, menu_font_size)
        menu_text = menu_font.render("Graphismes - Choix résolution", True, (255, 255, 255))
        menu_rect = menu_text.get_rect(center=(screen_width // 2, screen_height // 10))

        button_height = int(50 * scale_factor_width)
        spacing = int(20 * scale_factor_width)

        resolutions = [
            (1920, 1080),
            (1760, 990),
            (1680, 1050),
            (1600, 900),
            (1366, 768),
            (1280, 1024),
            (1280, 720)
        ]

        buttons = []

        for i, (width, height) in enumerate(resolutions):
            button = Button(self.game, f"{width} x {height}", (300 * scale_factor_width, button_height),
                            int(50 * scale_factor_width), (screen_width // 2, screen_height // 3 + i * (button_height + spacing)))
            buttons.append(button)

        boutton_retour = Button(self.game, "Retour", (200 * scale_factor_width, 35 * scale_factor_height),
                                int(50 * scale_factor_width), (120 * scale_factor_width, 50 * scale_factor_height))

        while True:
            self.game.screen.fill((0, 0, 0))
            self.game.screen.blit(menu_text, menu_rect)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                for button in buttons:
                    button.event(event)
                boutton_retour.event(event)

            self.game.particules.update_particles()

            for button in buttons:
                button.draw()

            boutton_retour.draw()

            for i, button in enumerate(buttons):
                if button.is_clicked and resolutions[i] == resolutions[0]:
                    self.game.settings.WIDTH, self.game.settings.HEIGHT = resolutions[i]
                    self.game.settings.SCALE_FACTOR_WIDTH = self.game.settings.WIDTH / 1920
                    self.game.settings.SCALE_FACTOR_HEIGHT = self.game.settings.HEIGHT / 1080
                    self.game.screen = pg.display.set_mode((self.game.settings.WIDTH, self.game.settings.HEIGHT), pg.FULLSCREEN)
                    return
                elif button.is_clicked:
                    self.game.settings.WIDTH, self.game.settings.HEIGHT = resolutions[i]
                    self.game.settings.SCALE_FACTOR_WIDTH = self.game.settings.WIDTH / 1920
                    self.game.settings.SCALE_FACTOR_HEIGHT = self.game.settings.HEIGHT / 1080
                    self.game.screen = pg.display.set_mode((self.game.settings.WIDTH, self.game.settings.HEIGHT))
                    return

            if boutton_retour.is_clicked:
                self.game.state.lower_state()
                return

            self.game.utils.get_fps()
            self.game.utils.update_mouse()
            pg.display.flip()
            self.game.FramePerSec.tick(self.game.FPS)

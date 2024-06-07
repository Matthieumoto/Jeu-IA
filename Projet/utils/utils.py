from utils.settings import *

class Utils:
    def __init__(self, game) -> None:
        self.game = game
        self.font = pg.font.Font(None, 40)
    
    def load_ressources_thread(self):
        self.avancement = 10
        self.mouse_texture = pg.image.load("ressources/mouse.png").convert_alpha()
        self.mouse_texture.set_colorkey((0, 0, 0, 0))

        self.avancement = 30
        self.effect_button_sound = pg.mixer.Sound("ressources/button_effect.mp3")

        self.avancement = 60
        self.menu_sound = pg.mixer.Sound("ressources/menu_theme.mp3")

        self.avancement = 90
        with open("data/settings.json", "r") as data:
            self.settings_data = json.load(data)

        self.avancement = 101
    
    def load_ressources(self):
        t = threading.Thread(target=self.load_ressources_thread).start()
        loading_bar_rect = pg.Rect((self.game.screen.get_width() - 720) // 2, (self.game.screen.get_height() - 8) // 2, 720, 8)

        while self.avancement < 101:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
            
            loading_bar_width = self.avancement / 100 * 720
            loading_bar_rect.width = int(loading_bar_width)

            percentage_text = self.font.render(f"{int(self.avancement)}%", True, (255, 255, 255))
            percentage_rect = percentage_text.get_rect(center=(self.game.screen.get_width() // 2, (self.game.screen.get_height() - 60) // 2))

            self.game.screen.fill((0, 0, 0))

            pg.draw.rect(self.game.screen, (255, 255, 255), loading_bar_rect)
            self.game.screen.blit(percentage_text, percentage_rect)

            pg.display.update()

    
    def update_mouse(self):
        self.game.screen.blit(self.mouse_texture,pg.mouse.get_pos())
    
    def get_fps(self):
        text1 = self.font.render(f"FPS : {int(self.game.FramePerSec.get_fps())}", True, (255, 255, 255))
        rect1 = text1.get_rect(center=(1810 * self.game.settings.SCALE_FACTOR_WIDTH, 20 * self.game.settings.SCALE_FACTOR_HEIGHT))
        self.game.screen.blit(text1, rect1)
    
    def save_settings(self):
        with open("data/settings.json","w") as data:
            json.dump(self.settings_data,data,indent=2)
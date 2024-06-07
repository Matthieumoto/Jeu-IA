from utils.settings import threading, pg, time

class Slider:
    def __init__(self, screen, pos: tuple, width: int, height: int, button_width: int, max_value: int,current_value : int) -> None:
        self.screen = screen
        self.pos = pos
        self.width = width
        self.height = height
        self.button_width = button_width
        self.max_value = max_value
        self.is_clicked = False
        self.slider_value = current_value

        self.slider_color = (220, 220, 220)
        self.button_color = (255, 255, 255)
        self.button_border_thickness = 1
        self.slider_border_thickness = 0
        self.slider_bar_height = 10

        self.rect_x = self.pos[0] - self.width // 2
        self.rect_y = self.pos[1] - self.height // 2

    def draw(self):
        #C'est très moche même moi j'au du mal à comprendre :/
        pg.draw.rect(self.screen, self.slider_color, [self.rect_x, self.rect_y + self.height/2 - self.slider_bar_height/2, self.width, self.slider_bar_height])
        pg.draw.rect(self.screen, self.button_color, [self.rect_x + self.slider_value * ((self.width - self.button_width) / self.max_value), self.rect_y, self.button_width, self.height],border_radius=50)
        if self.button_border_thickness != 0:
            pg.draw.rect(self.screen, (0, 0, 0), [self.rect_x + self.slider_value * ((self.width - self.button_width) / self.max_value), self.rect_y, self.button_width, self.height], self.button_border_thickness)
        if self.slider_border_thickness != 0:
            pg.draw.rect(self.screen, (0, 0, 0), [self.rect_x, self.rect_y + self.height/2 - self.slider_bar_height/2, self.width, self.slider_bar_height], self.slider_border_thickness)

    def event(self, event):
        mouse = pg.mouse.get_pos()

        if event.type == pg.MOUSEBUTTONDOWN:
            self.is_clicked = self.rect_x <= mouse[0] <= self.rect_x + self.width and self.rect_y <= mouse[1] <= self.rect_y + self.height
        elif event.type == pg.MOUSEBUTTONUP:
            self.is_clicked = False
        if self.is_clicked:
            mouseX = pg.mouse.get_pos()[0] - 5
            if mouseX < self.rect_x:
                mouseX = self.rect_x
            elif mouseX > self.rect_x + self.width - self.button_width:
                mouseX = self.rect_x + self.width - self.button_width
            self.slider_value = int((mouseX - self.rect_x) / ((self.width - self.button_width) / self.max_value))


class Button:
    def __init__(self, game, text: str, size: tuple, font_size: int, pos: tuple) -> None:
        self.game = game
        self.screen = game.screen
        self.is_clicked = False
        self.font = pg.font.Font(None, font_size)
        self.size = size
        self.texte = self.font.render(text, True, (0, 0, 0))
        self.pos = pos
        self.out = pg.Surface((self.size[0], self.size[1]), pg.SRCALPHA)
        self.on = pg.Surface((self.size[0], self.size[1]), pg.SRCALPHA)
        self.rect_x = self.pos[0] - self.size[0] // 2
        self.rect_y = self.pos[1] - self.size[1] // 2

        pg.draw.rect(self.out, (170, 170, 170, 200), [0, 0, self.size[0], self.size[1]], border_radius=20)
        pg.draw.rect(self.on, (100, 100, 100, 170), [0, 0, self.size[0], self.size[1]], border_radius=20)

    def draw(self):
        mouse = pg.mouse.get_pos()

        if self.rect_x <= mouse[0] <= self.rect_x + self.size[0] and self.rect_y <= mouse[1] <= self.rect_y + self.size[1]:
            self.screen.blit(self.on, (self.rect_x, self.rect_y))
        else:
            self.screen.blit(self.out, (self.rect_x, self.rect_y))

        text_width, text_height = self.texte.get_size()
        text_x = self.pos[0] - text_width // 2
        text_y = self.pos[1] - text_height // 2
        self.screen.blit(self.texte, (text_x, text_y))

    def event(self, event):
        mouse = pg.mouse.get_pos()

        if event.type == pg.MOUSEBUTTONDOWN:
            self.is_clicked = self.rect_x <= mouse[0] <= self.rect_x + self.size[0] and self.rect_y <= mouse[1] <= self.rect_y + self.size[1]
            if self.is_clicked:
                self.game.utils.effect_button_sound.play()
        elif event.type == pg.MOUSEBUTTONUP:
            self.is_clicked = False

class TextZone:
    def __init__(self, game, default_text: str, size: tuple, font_size: int, pos: tuple, max_length: int) -> None:
        self.game = game
        self.screen = game.screen
        self.font = pg.font.Font(None, font_size)
        self.size = size
        self.default_text = default_text
        self.text = ""
        self.max_length = max_length
        self.pos = pos
        self.is_writing = False

    def get(self):
        return self.text

    def draw(self):
        rect = pg.Rect(self.pos[0] - self.size[0] // 2, self.pos[1] - self.size[1] // 2, self.size[0], self.size[1])
        color = (0, 255, 0) if self.is_writing else (175, 175, 175)
        pg.draw.rect(self.screen, color, rect, 2)

        if self.text == "":
            text_surface = self.font.render(self.default_text, True, (255, 255, 255))
        else:
            text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.pos[0], self.pos[1]))
        self.screen.blit(text_surface, text_rect)

    def event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = pg.mouse.get_pos()
            if pg.Rect(self.pos[0] - self.size[0] // 2, self.pos[1] - self.size[1] // 2,
                        self.size[0], self.size[1]).collidepoint(mouse_pos):
                self.is_writing = True
            else:
                self.is_writing = False
        elif event.type == pg.KEYDOWN and self.is_writing:
            if event.key == pg.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if len(self.text) < self.max_length:
                    self.text += event.unicode

class Bandeau:
    def __init__(self, game, text: str, size: tuple, font_size: int, pos: tuple, color: tuple, time: int) -> None:
        self.game = game
        self.screen = game.screen
        self.font = pg.font.Font(None, font_size)
        self.size = size
        self.text = text
        self.pos = pos
        self.color = color
        self.affiche = False
    
    def bandeu_thread(self, temps: float):
        self.affiche = True
        deb_time = time.time()
        while (time.time()-deb_time) < temps:
            surf = pg.Surface(self.size, pg.SRCALPHA)
            pg.draw.rect(surf, (self.color[0],self.color[1],self.color[2], 128), (0, 0, *self.size),border_radius=10)

            text_surface = self.font.render(self.text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.size[0] // 2, self.size[1] // 2))
            surf.blit(text_surface, text_rect)

            self.screen.blit(surf, self.pos)
        self.affiche = False

    def draw(self, temps: float):
        if not self.affiche:
            threading.Thread(target=self.bandeu_thread, args=(temps,)).start()
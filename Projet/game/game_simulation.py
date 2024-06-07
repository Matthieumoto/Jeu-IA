from utils.settings import random, pg, sys

class Neurones: 
    def __init__(self, game):
        self.map = game.game.map
        self.weights = [random.uniform(-1,1) for _ in range(8)]
        self.biais = [random.uniform(-0.1, 0.1) for _ in range(8)]
    
    def predict(self,x: int, y: int):
        inputs = [
                self.map[y][x+1],   # droite
                self.map[y+1][x+1], # bas droite
                self.map[y][x-1],   # gauche
                self.map[y+1][x-1], # bas gauche
                self.map[y+1][x],   # bas
                self.map[y-1][x+1], # haut droite
                self.map[y-1][x],   # haut
                self.map[y-1][x-1]  # haut gauche
            ]
        inter = []
        for i in range(len(inputs)):
            inter.append(inputs[i] * self.weights[i] + self.biais[i])
        inter[0] += inter[1] + inter[5]
        inter[2] += inter[7]+inter[3]
        inter[4] += inter[1] + inter[3]
        inter[6] += inter[5] + inter[7]
        res = [inter[0], inter[2], inter[4], inter[6]]
        x = max(res)
        #resultat de la forme[droite, gauche, haut, bas]
        #print("res", res)
        if x == res[0]:
            return pg.K_RIGHT
        if x == res[1]:
            return pg.K_LEFT
        if x == res[2]:
            return pg.K_UP
        if x == res[3]:
            return pg.K_DOWN

class Player:
    def __init__(self, game, color: tuple, parent: Neurones = None):
        self.x = 0
        self.y = 10
        self.game = game
        self.color = color
        self.jump_force = 5
        self.start_time = 0
        self.jump = False
        if parent:
            self.ia = Neurones(self)
            for i in range(len(parent.weights)):
                self.ia.weights[i] = parent.weights[i] + random.uniform(-0.1, 0.1)
                self.ia.biais[i] = parent.biais[i] + random.uniform(-0.1, 0.1)
        else:
            self.ia = Neurones(self)

    def check_collision(self, x: int, y: int):
        return (x, y) not in self.game.worldmap

    def movement(self, event):
        if event == pg.K_RIGHT and self.check_collision(self.x + 1, self.y) and (self.x + 1 <= self.game.x_max) and (self.x + 1 >= 0):
            self.x += 1
        if event == pg.K_LEFT and self.check_collision(self.x - 1, self.y) and (self.x - 1 <= self.game.x_max) and (self.x - 1 >= 0):
            self.x -= 1
        if event == pg.K_DOWN and self.check_collision(self.x, self.y + 1)  and (self.y + 1 <= self.game.y_max) and (self.y + 1 >= 0):
            self.y += 1
        if event == pg.K_UP and not self.jump and self.check_collision(self.x, self.y - 1) and (self.y - 1 <= self.game.y_max) and (self.y - 1 >= 0):
            self.jump = True
            self.start_time = pg.time.get_ticks()

    def update(self):
        if self.x == self.game.x_max:
            return True
        self.movement(self.ia.predict(self.x, self.y))
        if self.jump:
            for i in range(self.jump_force):
                if self.check_collision(self.x, self.y - i) and (self.y - i >= 0):
                    self.y -= 1
                else:
                    self.jump = False
                    break
        else:
            if ((pg.time.get_ticks() - self.start_time) % 7) == 0:
                if self.check_collision(self.x, self.y + 1) and (self.y + 1 <= self.game.y_max):
                    self.y += 1
        self.draw_player()

    def draw_player(self):
        pg.draw.rect(self.game.game.screen, self.color,
                     ((self.x * self.game.case_size) * self.game.game.settings.SCALE_FACTOR_WIDTH,
                      (self.y * self.game.case_size) * self.game.game.settings.SCALE_FACTOR_HEIGHT,
                      self.game.case_size * self.game.game.settings.SCALE_FACTOR_WIDTH,
                      self.game.case_size * self.game.game.settings.SCALE_FACTOR_HEIGHT))

class Game_simulation:
    def __init__(self, main) -> None:
        self.game = main
        self.case_size = min(1920 // 30, 1080 // 30)
        self.map = [[1 for i in range(1920 // self.case_size)] for j in range(1080 // self.case_size)]
        self.worldmap = {}
        self.x_max = len(self.map[0])-1
        self.y_max = len(self.map)-1
        self.frames = 0
        self.generation = 0
        self.generate_random_path()
        self.get_map()
        self.couleurs = [
                (255, 0, 0),
                (0, 255, 0),
                (0, 0, 255),
                (255, 255, 0),
                (255, 0, 255),
                (0, 255, 255),
                (128, 0, 0),
                (0, 128, 0),
                (0, 0, 128),
                (128, 128, 0),
                (128, 0, 128),
                (0, 128, 128),
                (128, 128, 128),
                (192, 192, 192),
                (255, 165, 0),
                (165, 42, 42),
                (128, 128, 0),
                (128, 0, 0),
                (128, 0, 128),
                (0, 128, 0)
            ]
        self.players = [Player(self, self.couleurs[i]) for i in range(20)]

    def draw_map(self):
        for y, ligne in enumerate(self.map):
            for x, case in enumerate(ligne):
                if case == 1:
                    pg.draw.rect(self.game.screen, (0, 0, 0),
                                 ((x * self.case_size) * self.game.settings.SCALE_FACTOR_WIDTH,
                                  (y * self.case_size) * self.game.settings.SCALE_FACTOR_HEIGHT,
                                  self.case_size * self.game.settings.SCALE_FACTOR_WIDTH,
                                  self.case_size * self.game.settings.SCALE_FACTOR_HEIGHT))
                else:
                    pg.draw.rect(self.game.screen, (255, 255, 255),
                                 ((x * self.case_size) * self.game.settings.SCALE_FACTOR_WIDTH,
                                  (y * self.case_size) * self.game.settings.SCALE_FACTOR_HEIGHT,
                                  self.case_size * self.game.settings.SCALE_FACTOR_WIDTH,
                                  self.case_size * self.game.settings.SCALE_FACTOR_HEIGHT))

    def generate_random_path(self):
        current_position = (0, 10)
        self.map[current_position[1]][current_position[0]] = 0
        while current_position[0] < len(self.map[0]) - 1:
            direction = random.choice([(0, 1), (0, -1), (1, 0)])
            new_position = (current_position[0] + direction[0], current_position[1] + direction[1])
            if 0 <= new_position[0] < len(self.map[0]) and 0 <= new_position[1] < len(self.map):
                self.map[new_position[1]][new_position[0]] = 0
                current_position = new_position
        self.exit_pos = new_position

    def play(self):
        font = pg.font.Font(None, int(40 * self.game.settings.SCALE_FACTOR_WIDTH))
        while True:
            if self.frames > (self.x_max * 2):
                best = second_best = self.players[0]
                for player in self.players:
                    if player.x > best.x:
                        second_best = best
                        best = player
                    elif player.x > second_best.x and player!= best:
                        second_best = player
                parent_instance = Player(self, (0,0,0))
                #algo de crossover pour récupérer les gènes des deux meilleurs bot
                for i in range(8):
                    if random.random() > 0.5:
                        parent_instance.ia.weights[i] = best.ia.weights[i]
                        parent_instance.ia.biais[i] = best.ia.biais[i]
                    else:
                        parent_instance.ia.weights[i] = second_best.ia.weights[i]
                        parent_instance.ia.biais[i] = second_best.ia.biais[i]
                self.reset(parent=parent_instance.ia)
                self.frames = 0
                self.generation += 1
            text1 = font.render(f"Génération n°{self.generation}", True, (255, 255, 255))
            rect1 = text1.get_rect(center=(self.game.settings.WIDTH // 2, self.game.settings.WIDTH // 20))
            self.game.screen.fill((255, 0, 0))
            self.draw_map()
            self.game.screen.blit(text1, rect1)
            for player in self.players:
                termine = player.update()
                if termine:
                    self.game.state.modify_state("jeu_win")
                    return
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_r:
                        self.true_reset()
                    if event.key == pg.K_ESCAPE:
                        self.game.state.lower_state()
                        return
            self.frames += 1
            self.game.utils.get_fps()
            pg.display.flip()
            self.game.FramePerSec.tick(144)#changer cette valeur afin d'accélérer la simulation

    def get_map(self):
        for j, row in enumerate(self.map):
            for i, value in enumerate(row):
                if value:
                    self.worldmap[(i, j)] = value
    
    def true_reset(self):
        self.map = [[1 for i in range(1920 // self.case_size)] for j in range(1080 // self.case_size)]
        self.worldmap = {}
        self.x_max = len(self.map[0])-1
        self.y_max = len(self.map)-1
        self.frames = 0
        self.generation = 0
        self.generate_random_path()
        self.get_map()
        self.players = [Player(self, self.couleurs[i]) for i in range(20)]
    
    def reset(self, parent: Neurones):
        self.players = [Player(self, self.couleurs[i],parent=parent) for i in range(20)]
    
    def win(self):

        scale_factor_width = self.game.settings.SCALE_FACTOR_WIDTH

        font = pg.font.Font(None, int(40 * scale_factor_width))
        text1 = font.render(f"Le bot a battu le jeu en {self.generation} generations, appuyez sur une touche pour reset", True, (255, 255, 255))
        rect1 = text1.get_rect(center=(self.game.settings.WIDTH // 2, self.game.settings.HEIGHT // 2))

        while True:
            self.game.screen.fill((0, 0, 0))
            self.game.screen.blit(text1, rect1)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    self.true_reset()
                    self.game.state.lower_state()
                    return
            self.game.particules.update_particles()
            self.game.utils.update_mouse()
            self.game.utils.get_fps()
            pg.display.flip()
            self.game.FramePerSec.tick(self.game.FPS)
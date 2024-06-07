from utils.settings import pg, random

class Particules:
    def __init__(self, game):
        self.game = game
        self.particles = []  # Liste pour stocker les particules
        self.particle_timer = 0  # Timer pour suivre quand la prochaine particule sera créée
        self.particle_interval = 50  # Intervalle entre chaque création de particule

    def circle_surf(self, radius, color):
        surf = pg.Surface((radius * 2, radius * 2))  # Création d'une surface avec un diamètre double du rayon
        pg.draw.circle(surf, color, (radius, radius), radius)
        surf.set_colorkey((0, 0, 0))
        return surf

    def update_particles(self):
        current_time = pg.time.get_ticks()

        if current_time - self.particle_timer >= self.particle_interval:
            self.particles.append([[random.randint(20, self.game.settings.WIDTH - 20), random.randint(20, self.game.settings.HEIGHT - 20)],  # Création d'une nouvelle particule avec une position aléatoire
                                   [random.randint(0, 20) / 10 - 1, -0.5], random.randint(4, 15)])
            self.particle_timer = current_time

        for particle in self.particles:
            particle[0][0] += particle[1][0]  # Ajout de la vitesse horizontale à la position actuelle
            particle[0][1] += particle[1][1]  # Ajout de la vitesse verticale à la position actuelle
            particle[2] -= 0.1  # Diminution de la taille de la particule
            particle[1][1] += 0.02  # Ajustement de la vitesse verticale de la particule

            pg.draw.circle(self.game.screen, (255, 255, 255), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
            radius = particle[2] * 2
            self.game.screen.blit(self.circle_surf(radius, (20, 20, 60)),  # Utilisation de la méthode circle_surf pour obtenir une surface avec un cercle
                                  (int(particle[0][0] - radius), int(particle[0][1] - radius)),  # Positionnement du cercle sur l'écran
                                  special_flags=pg.BLEND_RGB_ADD)  # Utilisation de BLEND_RGB_ADD pour combiner les couleurs
            if particle[2] <= 0:
                self.particles.remove(particle)

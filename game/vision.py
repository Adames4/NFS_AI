from .constants import BACKGROUND, GRASS, WIN, RED
from math import sin, cos, pi
import pygame


class Vision():
    def __init__(self):
        self.visible = False

    def make_points(self, center, angle):
        self.points = list()
        self.distances = list()
        for a in range(-90, 91, 45):
            angle_of_line = angle + a
            x, y = center
            step = 0
            while BACKGROUND.get_at((int(x), int(y))) != GRASS and step < 250:
                step += 1
                x -= cos(angle_of_line / 180 * pi)
                y += sin(angle_of_line / 180 * pi)

            self.distances.append(step)
            self.points.append((x, y))

        if self.visible:
            self.draw(center)

    def draw(self, center):
        for point in self.points:
            pygame.draw.line(WIN, RED, center, point)

    def visible_on(self):
        self.visible = True

    def visible_off(self):
        self.visible = False

    def get_vision(self):
        return self.distances

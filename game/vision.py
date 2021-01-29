from math import sin, cos, pi
import pygame

from .constants import BACKGROUND, GRASS, WIN, RED


class Vision():
    '''
    Vision object represent vision for every single Car object
    '''
    def __init__(self):
        self.visible = False

    def make_points(self, center, angle):
        '''
        determinate distances from front of car to sides of road in 5 
        different angles (-90, -45, 0, 45, 90) and coordinates of sides 
        of road
        center: (x, y) of Car object
        angle:  angle of Car object
        '''
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
        '''
        draw 5 lines from front of car to sides of road
        '''
        for point in self.points:
            pygame.draw.line(WIN, RED, center, point)

    def visible_on(self):
        '''
        turn vision on
        '''
        self.visible = True

    def visible_off(self):
        '''
        turn vision off
        '''
        self.visible = False

    def get_vision(self):
        '''
        return: distance from front of car to the side of road in 5 different
                directions
        '''
        return self.distances

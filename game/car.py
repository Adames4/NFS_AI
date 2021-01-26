import pygame
from .constants import WIN, BACKGROUND, ROAD, GRASS, SPEED, ROTATION
from math import sin, cos, pi
from .checkpoint import Checkpoint
from .vision import Vision


class Car:
    def __init__(self, x, y, car):
        self.x = x
        self.y = y
        self.car = car
        self.angle = 0
        self.surface = True
        self.rect = self.car.get_rect(
                center=self.car.get_rect(topleft=(self.x, self.y)).center)

        self.checkpoint = Checkpoint()
        self.vision = Vision()

    def move(self, speed):
        self.x -= cos(self.angle / 180 * pi) * speed
        self.y += sin(self.angle / 180 * pi) * speed

    def move_forward(self):
        if self.surface:
            self.move(SPEED)
        else:
            self.move(SPEED / 2)

    def move_backward(self):
        if self.surface:
            self.move(- SPEED / 2)
        else:
            self.move(- SPEED / 4)

    def turn_left(self):
        if self.surface:
            self.angle += ROTATION
        else:
            self.angle += ROTATION / 2

    def turn_right(self):
        if self.surface:
            self.angle -= ROTATION
        else:
            self.angle -= ROTATION / 2

    def draw(self):
        self.get_surface()

        rotated_image = pygame.transform.rotate(self.car, self.angle)
        self.rect = rotated_image.get_rect(
                center=self.car.get_rect(topleft=(self.x, self.y)).center)

        WIN.blit(rotated_image, self.rect.topleft)

    def get_surface(self):
        front_x = int(self.rect.center[0] - cos(self.angle / 180 * pi) * 30)
        front_y = int(self.rect.center[1] + sin(self.angle / 180 * pi) * 12)

        if front_x < 0:
            front_x = 0
        elif front_x > 1499:
            front_x = 1499

        if front_y < 0:
            front_y = 0
        elif front_y > 1079:
            front_y = 1079

        current_color = BACKGROUND.get_at((front_x, front_y))

        if current_color == GRASS:
            self.surface = False
        else:
            self.vision.make_points((front_x, front_y), self.angle)
            self.surface = True
            if current_color != ROAD:
                self.checkpoint.set_checkpoint(current_color)

        return self.surface

    def get_checkpoint(self, number):
        return self.checkpoint.get_checkpoint(number)

    def get_current_time(self):
        return self.checkpoint.get_current_time()

    def visible_on(self):
        self.vision.visible_on()

    def visible_off(self):
        self.vision.visible_off()

    def get_vision(self):
        return self.vision.get_vision()

    def get_checkpoint_fitness(self):
        return self.checkpoint.get_checkpoint_fitness()

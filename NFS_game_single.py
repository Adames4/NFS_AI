import pygame
from random import randint
from time import sleep

from game.constants import FPS, BACKGROUND, WIN, CARS, WHITE
from game.car import Car
from game.checkpoint import time_conventor


clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont(None, 60)


def win_blit(car, color, times, time_counter, current_time):
    WIN.blit(BACKGROUND, (0, 0))

    WIN.blit(font.render('Time: ', True, WHITE), (1510, 10))
    for i in range(1, 7):
        WIN.blit(font.render(f'Check{i}: ', True, WHITE), (1510, 10 + i * 60))
    WIN.blit(font.render('Lap time: ', True, WHITE), (1510, 430))

    WIN.blit(font.render(current_time, True, WHITE), (1740, 10))

    if car.get_checkpoint(time_counter):
        times[time_counter] = time_conventor(car.get_checkpoint(time_counter))
        time_counter += 1

    for i in range(time_counter):
        WIN.blit(font.render(times[i], True, color), (1740, 70 + i * 60))

    car.draw()
    pygame.display.update()

    return time_counter


def main():
    random_car = randint(0, 7)
    formula = Car(955, 900, CARS[random_car][0])
    color = CARS[random_car][1]
    times = [None for _ in range(7)]
    time_counter = 0

    WIN.blit(BACKGROUND, (0, 0))
    pygame.display.update()
    sleep(1)

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys_pressed = pygame.key.get_pressed()
        w = keys_pressed[pygame.K_w]
        a = keys_pressed[pygame.K_a]
        s = keys_pressed[pygame.K_s]
        d = keys_pressed[pygame.K_d]
        up = keys_pressed[pygame.K_UP]
        left = keys_pressed[pygame.K_LEFT]
        down = keys_pressed[pygame.K_DOWN]
        right = keys_pressed[pygame.K_RIGHT]
        esc = keys_pressed[pygame.K_ESCAPE]
        v = keys_pressed[pygame.K_v]
        c = keys_pressed[pygame.K_c]

        # forward
        if w or up:
            formula.move_forward()

        # backward
        if s or down:
            formula.move_backward()

        # left
        if ((a or left) and (w or up)) or ((d or right) and (s or down)):
            formula.turn_left()

        # right
        if ((d or right) and (w or up)) or ((a or left) and (s or down)):
            formula.turn_right()

        # vision
        if v:
            formula.visible_on()
        if c:
            formula.visible_off()

        # quit
        if esc:
            run = False

        time_counter = win_blit(
            formula, color, times, time_counter,
            time_conventor(formula.get_current_time()))


if __name__ == "__main__":
    main()

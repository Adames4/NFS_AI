import pygame
from random import randint
import neat
import pickle
import os
from time import sleep

from game.constants import FPS, BACKGROUND, WIN, CARS, WHITE, LIME, RED
from game.car import Car
from game.checkpoint import time_conventor


clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont(None, 60)
font2 = pygame.font.SysFont(None, 100)


def win_blit(cars, colors, times, time_counter, current_time):
    WIN.blit(BACKGROUND, (0, 0))

    WIN.blit(font.render('Time: ', True, WHITE), (1510, 10))
    for i in range(1, 7):
        WIN.blit(font.render(f'Check{i}: ', True, WHITE), (1510, 10 + i * 60))
    WIN.blit(font.render('Lap time: ', True, WHITE), (1510, 430))

    WIN.blit(font.render(current_time, True, WHITE), (1740, 10))

    for car, color in zip(cars, colors):
        if car.get_checkpoint(time_counter):
            times[time_counter] = (
                time_conventor(car.get_checkpoint(time_counter)), color)
            time_counter += 1

    for i in range(time_counter):
        check_time = font.render(times[i][0], True, times[i][1])
        WIN.blit((check_time), (1740, 70 + i * 60))

    if times[6]:
        if times[6][1] == colors[0]:
            WIN.blit(font2.render('YOU WON!', True, LIME), (1510, 1000))
        elif times[6][1] == colors[1]:
            WIN.blit(font2.render('YOU LOST!', True, RED), (1510, 1000))

    for car in cars:
        car.draw()

    pygame.display.update()

    return time_counter


def game(genome, config):
    random_car = randint(0, 7)
    random_AI_car = randint(0, 7)
    while random_car == random_AI_car:
        random_AI_car = randint(0, 7)

    car = Car(955, 900, CARS[random_car][0])
    color = CARS[random_car][1]

    AI_car = Car(955, 900, CARS[random_AI_car][0])
    AI_color = CARS[random_AI_car][1]
    AI_genome = genome[0][1]
    AI_net = neat.nn.FeedForwardNetwork.create(AI_genome, config)

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

        if AI_car.get_surface():
            inputs = AI_car.get_vision()
            output = AI_net.activate(
                (inputs[0], inputs[1], inputs[2], inputs[3], inputs[4]))
            if output[0] > 0:
                AI_car.move_forward()

                if output[1] > 0:
                    AI_car.turn_left()

                if output[2] > 0:
                    AI_car.turn_right()

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
            car.move_forward()

        # backward
        if s or down:
            car.move_backward()

        # left
        if ((a or left) and (w or up)) or ((d or right) and (s or down)):
            car.turn_left()

        # right
        if ((d or right) and (w or up)) or ((a or left) and (s or down)):
            car.turn_right()

        # vision
        if v:
            AI_car.visible_on()
        if c:
            AI_car.visible_off()

        # quit
        if esc:
            run = False

        time_counter = win_blit(
            [car, AI_car], [color, AI_color], times, time_counter,
            time_conventor(car.get_current_time()))


def run(config_file):
    config = neat.config.Config(
        neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
        neat.DefaultStagnation, config_file)
    genome = [(1, pickle.load(open('AI/2166.pickle', 'rb')))]
    AI = game(genome, config)


def main():
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'AI/config-feedforward.txt')
    run(config_path)


if __name__ == "__main__":
    main()

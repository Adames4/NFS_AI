import pygame
import neat
import os
import pickle

from game.constants import WIN_WIDTH, FPS, BACKGROUND, WIN, CARS, WHITE
from game.car import Car
from game.checkpoint import time_conventor


clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont(None, 60)
generation = -1


def win_blit(cars, colors, times, time_counter, current_time, fitness, gen):
    '''
    drawing background, current time, checkpoints, lap time, car objects
    of AI
    return: number of current checkpoint
    '''

    # blitting background
    WIN.blit(BACKGROUND, (0, 0))

    # blitting Time: current time
    WIN.blit(font.render('Time: ', True, WHITE), (1510, 10))
    WIN.blit(font.render(current_time, True, WHITE), (1740, 10))

    # blitting Check_num:
    for i in range(1, 7):
        WIN.blit(font.render(f'Check{i}: ', True, WHITE), (1510, 10 + i * 60))

    # blitting Lap time:
    WIN.blit(font.render('Lap time: ', True, WHITE), (1510, 430))

    # filling times list with checkpoint times and colors of car object
    for car, color in zip(cars, colors):
        if car.get_checkpoint(time_counter):
            times[time_counter] = (
                time_conventor(car.get_checkpoint(time_counter)), color)
            time_counter += 1

    # blitting checkpoint times with color of car
    for i in range(time_counter):
        check_time = font.render(times[i][0], True, times[i][1])
        WIN.blit(check_time, (1740, 70 + i * 60))

    # blitting Gen:
    WIN.blit(font.render('Gen: ', True, WHITE), (1510, 490))

    # blitting Cars:
    WIN.blit(font.render('Cars: ', True, WHITE), (1510, 550))

    # blitting Fitness: in all colors
    for i in range(0, 16, 2):
        fitness_color = font.render('Fitness: ', True, fitness[i])
        WIN.blit(fitness_color, (1510, 610 + i * 30))

    # blitting number of generation
    num_gens = font.render(str(gen), True, WHITE)
    WIN.blit(num_gens, (WIN_WIDTH - num_gens.get_width() - 15, 490))

    # blitting number of car objects left
    num_cars = font.render(str(len(cars)), True, WHITE)
    WIN.blit(num_cars, (WIN_WIDTH - num_cars.get_width() - 15, 550))

    # blitting all fitnesses for car objects
    for i in range(1, 16, 2):
        fitt = font.render(f'{fitness[i]:.2f}', True, WHITE)
        x, y = WIN_WIDTH - fitt.get_width() - 15, 610 + (i - 1) * 30
        WIN.blit(fitt, (x, y))

    # blitting all car objects
    for car in cars:
        car.draw()

    # updating screen
    pygame.display.update()

    return time_counter


def eval_genomes(genomes, config):
    '''
    main loop of "TRAIN AI"
    '''

    # initializing all necessary lists
    nets = []           # neural networks
    cars = []           # car objects
    colors = []         # colors
    ge = []             # genomes
    checkpoints = []    # checkpoints
    fitness = []        # fitnesses

    # filling all lists
    for i, (_, genome) in enumerate(genomes):
        genome.fitness = 0
        nets.append(neat.nn.FeedForwardNetwork.create(genome, config))
        cars.append(Car(955, 900, CARS[i][0]))
        colors.append(CARS[i][1])
        ge.append(genome)
        checkpoints.append(0)
        fitness.append(CARS[i][1])
        fitness.append(0)

    # initializing checkpoints
    times = [None for _ in range(7)]
    time_counter = 0

    global generation
    generation += 1

    # main loop
    run = True
    while run:
        clock.tick(FPS)

        # quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit()
                pygame.quit()
                break

        # fitness function
        for i, car in enumerate(cars):

            # genome loses 5 fitness and is destroyed when hits a grass
            if not car.get_surface():
                ge[i].fitness -= 5

                index = fitness.index(colors[i]) + 1
                fitness[index] = ge[i].fitness

                cars.pop(i)
                colors.pop(i)
                nets.pop(i)
                ge.pop(i)
                checkpoints.pop(i)

            else:
                if checkpoints[i] < 7:
                    check = car.get_checkpoint_fitness()[checkpoints[i]]

                    # genome gains huge fitness when gets checkpoint
                    if check:
                        score = (10 * (checkpoints[i] + 1) - check) * 10
                        ge[i].fitness += score
                        checkpoints[i] += 1

                inputs = car.get_vision()
                output = nets[i].activate(
                    (inputs[0], inputs[1], inputs[2], inputs[3], inputs[4]))

                # genome gains 0.1 fitness when moves forward
                if output[0] > 0:
                    car.move_forward()
                    ge[i].fitness += 0.1

                    if output[1] > 0:
                        car.turn_left()

                    if output[2] > 0:
                        car.turn_right()

        # getting pressed keys
        keys_pressed = pygame.key.get_pressed()
        esc = keys_pressed[pygame.K_ESCAPE]
        v = keys_pressed[pygame.K_v]
        c = keys_pressed[pygame.K_c]

        # vision
        if v:
            for car in cars:
                car.visible_on()
        if c:
            for car in cars:
                car.visible_off()

        # quit
        if esc:
            run = False
            break

        # storing all fitnesses
        for i, color in enumerate(colors):
            index = fitness.index(color) + 1
            fitness[index] = ge[i].fitness

        # ending current generation
        if len(cars) == 0 or cars[0].get_current_time() > 20:
            run = False
            break

        time_counter = win_blit(
            cars, colors, times, time_counter,
            time_conventor(cars[0].get_current_time()), fitness, generation)


def run(config_file):
    '''
    initializing confing for AI and loading best trained AI
    '''

    # initializing config for AI
    config = neat.config.Config(
        neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
        neat.DefaultStagnation, config_file)

    # printing report to console
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    p.add_reporter(neat.StatisticsReporter())

    # running training with max 100 generation
    winner = p.run(eval_genomes, 100)

    # saving best trained AI
    pickle.dump(winner, open('AI/best_car.pickle', 'wb'))

    # printing neural network of best AI to console
    print(f'\n Best AI:')
    print(winner)


def main():
    '''
    finding path for AI config
    '''
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'AI/config-feedforward.txt')
    run(config_path)


if __name__ == "__main__":
    main()

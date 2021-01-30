import pygame

import NFS_game_single
import NFS_game_with_AI
import NFS_training_AI
from game.constants import BACKGROUND_MENU, FPS, WIN_MENU

pygame.init()
pygame.display.set_caption('Need For Speed')
clock = pygame.time.Clock()


def main():
    '''
    main game loop of menu
    '''

    # main loop
    run = True
    while run:
        clock.tick(FPS)

        # qiut
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        # getting mouse position when is pressed
        if pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            if x > 767 and x < 1151:

                # starting "GAME ALONE"
                if y > 269 and y < 359:
                    NFS_game_single.main()

                # starting "GAME WITH AI"
                elif y > 419 and y < 509:
                    NFS_game_with_AI.main()

                # starting "TRAIN AI"
                elif y > 569 and y < 659:
                    NFS_training_AI.main()

                # quit
                elif y > 719 and y < 809:
                    run = False
                    pygame.quit()

        # blitting background
        WIN_MENU.blit(BACKGROUND_MENU, (0, 0))

        # updating screen
        pygame.display.update()


if __name__ == "__main__":
    main()

import pygame

import NFS_game_single
import NFS_game_with_AI
import NFS_training_AI
from game.constants import BACKGROUND_MENU, FPS, WIN_MENU

pygame.init()
pygame.display.set_caption('Need For Speed')
clock = pygame.time.Clock()


def main():
    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            if x > 767 and x < 1151:
                if y > 269 and y < 359:
                    NFS_game_single.main()
                elif y > 419 and y < 509:
                    NFS_game_with_AI.main()
                elif y > 569 and y < 659:
                    NFS_training_AI.main()
                elif y > 719 and y < 809:
                    run = False

        WIN_MENU.blit(BACKGROUND_MENU, (0, 0))
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()

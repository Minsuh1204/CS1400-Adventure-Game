# Images are mostly created by the Copilot of Microsoft unless the source is written
# Written by Minsuh Chang
import pygame


def display_loss_screen():
    """
    Display the loss screen
    :return: None
    """
    pygame.init()
    clock = pygame.time.Clock()
    showing = True

    screen = pygame.display.set_mode((1200, 800))

    reddish_sky = pygame.image.load("./assets/reddish_grass.png")
    reddish_sky = pygame.transform.scale2x(reddish_sky)
    reddish_sky_rect = reddish_sky.get_rect()

    tombstone = pygame.image.load("./assets/game_over_tombstone.png")
    tombstone = pygame.transform.smoothscale(tombstone, (218, 250))
    tombstone_rect = tombstone.get_rect()
    tombstone_rect.center = (600, 300)

    while showing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                showing = False

        screen.blit(reddish_sky, reddish_sky_rect)
        screen.blit(tombstone, tombstone_rect)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()


def display_win_screen():
    """
    Display the win screen.
    :return: None
    """
    pygame.init()
    clock = pygame.time.Clock()
    showing = True

    screen = pygame.display.set_mode((1018, 500))

    game_font = pygame.font.SysFont("monospace", 40)
    win_message = game_font.render("YOU WIN!", True, (0, 0, 0))

    # image from: https://www.vectorstock.com/royalty-free-vectors/game-sky-vectors
    win_sky = pygame.image.load("./assets/win_sky.jpg").convert_alpha()
    win_sky_rect = win_sky.get_rect()

    win_cat = pygame.image.load("./assets/win_cat.png").convert_alpha()
    win_cat = pygame.transform.smoothscale(win_cat, (200, 200))
    win_cat_rect = win_cat.get_rect()
    win_cat_rect.center = (509, 300)

    while showing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                showing = False

        screen.blit(win_sky, win_sky_rect)
        screen.blit(win_cat, win_cat_rect)
        screen.blit(win_message, (409, 100))

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

# Images are mostly created by the Copilot of Microsoft unless the source is written
# Written by Minsuh Chang

from components import *
from training import training


def level2():
    """

    :return:
    """
    pygame.init()
    clock = pygame.time.Clock()

    is_playing = True
    level_started = False
    show_communicate_message = False
    show_class_choose_message = False
    show_classes = False
    training_started = False

    # image from: https://www.pinterest.com/pin/636696466057621686/
    grass_field = pygame.image.load("./assets/green_grass_map.jpg")
    grass_field = pygame.transform.smoothscale(grass_field, (1472, 828))
    grass_field_rect = grass_field.get_rect()
    grass_field_size = grass_field.get_size()

    screen = pygame.display.set_mode(grass_field_size)

    start_button = StartButton()
    start_button.rect.center = (750, 400)

    cat = Cat()
    cat.rect.center = (750, 700)

    advisor = Advisor()
    advisor.rect.center = (1300, 600)

    wizard_hat = WizardHat()
    wizard_hat.rect.center = (200, 700)

    crossbow = Crossbow()
    crossbow.rect.center = (600, 700)

    training_room_portal = LevelOnePortal()
    training_room_portal.image = pygame.transform.smoothscale(
        training_room_portal.image, (200, 200)
    )
    training_room_portal.rect.center = (500, 700)

    game_font = pygame.font.SysFont("monospace", 24)
    communicate_message = game_font.render("Press E to communicate.", True, (0, 0, 0))
    choose_your_class_message = game_font.render(
        "Select your class.", True, (0, 255, 0)
    )
    training_entrance_message = game_font.render(
        "Enter training field.", True, (0, 0, 0)
    )
    bigger_font = pygame.font.SysFont("monospace", 27)
    magicat_message = bigger_font.render("MagiCat", True, (255, 0, 255))
    huntercat_message = bigger_font.render("HunterCat", True, (192, 192, 192))

    while is_playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_playing = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if start_button.rect.collidepoint(pos[0], pos[1]):
                    level_started = True
                    show_communicate_message = True

        # check for pressed keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            cat.rect.move_ip((5, 0))
        if keys[pygame.K_a]:
            cat.rect.move_ip((-5, 0))
        if keys[pygame.K_e]:
            # check if cat is met with the advisor
            if pygame.sprite.collide_mask(cat, advisor):
                show_communicate_message = False
                show_class_choose_message = True
                show_classes = True

                if cat.subclass is not None:
                    training_started = True
                    show_classes = False
                    show_class_choose_message = False

            if pygame.sprite.collide_mask(cat, training_room_portal):
                return training(cat.subclass), cat.subclass

            # class selection
            if show_classes:
                cur_pos = cat.rect.center
                if pygame.sprite.collide_mask(cat, wizard_hat):
                    cat.change_class("MagiCat")
                    cat.rect.center = cur_pos
                elif pygame.sprite.collide_mask(cat, crossbow):
                    cat.change_class("HunterCat")
                    cat.rect.center = cur_pos

        # always on screen
        screen.blit(grass_field, grass_field_rect)
        screen.blit(advisor.image, advisor.rect)
        screen.blit(cat.image, cat.rect)

        if not level_started:
            screen.blit(start_button.image, start_button.rect)

        if show_communicate_message:
            screen.blit(communicate_message, (300, 300))

        if show_class_choose_message:
            screen.blit(choose_your_class_message, (1000, 300))

        if show_classes:
            screen.blit(wizard_hat.image, wizard_hat.rect)
            screen.blit(crossbow.image, crossbow.rect)

            if pygame.sprite.collide_mask(cat, wizard_hat):
                screen.blit(magicat_message, (160, 750))

            if pygame.sprite.collide_mask(cat, crossbow):
                screen.blit(huntercat_message, (540, 750))

        if training_started:
            screen.blit(training_room_portal.image, training_room_portal.rect)

            if pygame.sprite.collide_mask(cat, training_room_portal):
                screen.blit(training_entrance_message, (500, 500))

        pygame.display.update()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    level2()

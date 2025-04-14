# Written by Minsuh Chang

from components import *


def training(subclass: MagiCat | HunterCat):
    """
    Training course for level 2
    :param subclass: class of the cat.
    :return: True / False
    """
    pygame.init()
    clock = pygame.time.Clock()

    is_training = True
    show_attack_tutorial_message = True
    wave_2_started = False
    wave_clear_count = 0
    wave_3_started = False
    boss_portal_unlocked = False

    # image from: https://www.pinterest.com/pin/789255903419721384/
    training_field = pygame.image.load("./assets/training_field.png")
    training_field_rect = training_field.get_rect()
    training_field_size = training_field.get_size()
    training_field_size = training_field_size[0], training_field_size[1] - 56

    screen = pygame.display.set_mode(training_field_size)

    cat = Cat()
    if subclass.class_name == "MagiCat":
        cat.change_class("MagiCat")
    else:
        cat.change_class("HunterCat")
    cat.rect.center = (300, 300)

    game_font = pygame.font.SysFont("monospace", 24)
    bigger_font = pygame.font.SysFont("monospace", 30)
    attack_tutorial_message = game_font.render(
        "Mouse left-click to attack.", True, (0, 0, 0)
    )
    to_boss_message = bigger_font.render("PROCEED TO BOSS", True, (255, 0, 0))

    dummy_1 = DummyBot()
    dummy_1.rect.center = (250, 100)
    dummy_2 = DummyBot()
    dummy_2.rect.center = (100, 700)
    dummy_group: list[DummyBot] = pygame.sprite.Group(dummy_1)
    final_wave_dummies = [DummyBot() for i in range(10)]

    boss_portal = LevelOnePortal()
    boss_portal.rect.center = (250, 100)

    wall_1 = Wall(0, -5, 564, 1, "down")
    wall_2 = Wall(640, 0, 1, 846, "left")
    wall_3 = Wall(0, 800, 564, 1, "up")
    wall_4 = Wall(-35, 0, 1, 846, "right")
    # micro control for better wall
    if subclass == "HunterCat":
        wall_2 = Wall(600, 0, 1, 846, "left")
    elif subclass == "GladiaCat":
        wall_1 = Wall(0, -50, 564, 1, "down")
        wall_2 = Wall(590, 0, 1, 846, "left")
        wall_3 = Wall(0, 790, 564, 1, "up")
    wall_group: list[Wall] = pygame.sprite.Group(wall_1, wall_2, wall_3, wall_4)

    while is_training:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_training = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # https://stackoverflow.com/questions/34287938/how-to-distinguish-left-click-right-click-mouse-clicks-in-pygame
                match event.button:
                    case 1:
                        # left click
                        mouse_pos = pygame.mouse.get_pos()
                        cat.left_click_attack(mouse_pos)
                        show_attack_tutorial_message = False
                    case 2:
                        # right click
                        pass

        # block cat from being outside screen
        wall_collide_list = pygame.sprite.spritecollide(
            cat, wall_group, False, pygame.sprite.collide_rect
        )
        for wall in wall_collide_list:
            bounce = wall.bounce()
            cat.rect.move_ip(bounce)

        # save us from ourselves
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            cat.rect.move_ip(0, -5)
        if keys[pygame.K_s]:
            cat.rect.move_ip(0, 5)
        if keys[pygame.K_a]:
            cat.rect.move_ip(-5, 0)
        if keys[pygame.K_d]:
            cat.rect.move_ip(5, 0)
        if (
            keys[pygame.K_e]
            and pygame.sprite.collide_mask(cat, boss_portal)
            and boss_portal_unlocked
        ):
            return True

        # always on display
        screen.blit(training_field, training_field_rect)
        screen.blit(cat.image, cat.rect)

        if show_attack_tutorial_message:
            screen.blit(attack_tutorial_message, (100, 300))

        skill_onboard: list[Lightning, HunterArrow] = cat.subclass.skill_onboard
        for skill in skill_onboard:
            skill.move()
            if not skill.hit:
                screen.blit(skill.image, skill.rect)
                if pygame.sprite.spritecollide(
                    skill, dummy_group, True, pygame.sprite.collide_mask
                ):
                    skill.hit = True

        for dummy in dummy_group:
            screen.blit(dummy.image, dummy.rect)

        if len(dummy_group) == 0 and not wave_2_started and wave_clear_count == 0:
            wave_2_started = True
            wave_clear_count += 1

        if wave_2_started and wave_clear_count == 1:
            dummy_1.rect.center = (200, 300)
            dummy_group: list[DummyBot] = pygame.sprite.Group(dummy_1, dummy_2)
            wave_2_started = False

        if wave_clear_count == 1 and len(dummy_group) == 0:
            wave_clear_count += 1

        if wave_clear_count == 2 and not wave_3_started:
            diff_y = 150
            original_pos = (100, 100)
            for i in range(5):
                final_wave_dummies[i].rect.center = (
                    original_pos[0],
                    original_pos[1] + diff_y * i,
                )
            original_pos = (500, 100)
            for i in range(5):
                final_wave_dummies[i + 5].rect.center = (
                    original_pos[0],
                    original_pos[1] + diff_y * i,
                )
            dummy_group: list[DummyBot] = pygame.sprite.Group(*final_wave_dummies)
            wave_3_started = True

        if wave_clear_count == 2 and len(dummy_group) == 0:
            boss_portal_unlocked = True

        if boss_portal_unlocked:
            screen.blit(boss_portal.image, boss_portal.rect)

            if pygame.sprite.collide_mask(cat, boss_portal):
                screen.blit(to_boss_message, (170, 300))

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    training(HunterCat())

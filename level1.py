# Images are mostly created by the Copilot of Microsoft unless the source is written
# Written by Minsuh Chang

from components import *


def level1():
    """
    Level 1 of the game. Avoid fireballs and arrows.
    :return: True / False
    """
    # https://stackoverflow.com/questions/56502113/how-to-show-text-for-5-seconds-then-disappear-and-display-buttons
    show_message_event = pygame.USEREVENT + 1
    wave_4_end_event = pygame.USEREVENT + 2
    ending_event = pygame.USEREVENT + 3
    pygame.init()
    clock = pygame.time.Clock()
    frame_number = 0
    show_message = False
    is_playing = True
    level_started = False
    wave_1_started = False
    wave_2_started = False
    wave_3_started = False
    wave_4_started = False
    wave_5_started = False
    fence_broken = False
    portal_unlocked = False

    # map image from: https://stablediffusionweb.com/prompts/grass-map-for-games
    game_map = pygame.image.load("./assets/map3.png")
    game_map_rect = game_map.get_rect()
    game_map_size = game_map.get_size()
    screen = pygame.display.set_mode(game_map_size)

    wall_1 = Wall(600, 0, 10, 100, "left")
    wall_2 = Wall(660, 100, 10, 185, "left")
    wall_3 = Wall(845, 290, 10, 70, "left")
    wall_4 = Wall(660, 115, 100, 10, "down")
    wall_5 = Wall(765, 300, 100, 10, "down")
    wall_6 = Wall(822, 440, 80, 10, "up")
    wall_7 = Wall(777, 446, 10, 70, "left")
    wall_8 = Wall(776, 545, 100, 10, "down")
    wall_9 = Wall(854, 559, 10, 90, "left")
    wall_10 = Wall(782, 643, 150, 10, "up")
    wall_11 = Wall(752, 661, 10, 150, "left")
    wall_12 = Wall(395, 0, 10, 150, "right")
    wall_13 = Wall(330, 165, 10, 220, "right")
    wall_14 = Wall(258, 410, 10, 80, "right")
    wall_15 = Wall(273, 400, 10, 10, "down")
    wall_16 = Wall(277, 491, 10, 130, "right")
    wall_17 = Wall(193, 625, 80, 10, "down")
    wall_18 = Wall(192, 640, 10, 120, "right")
    wall_19 = Wall(202, 790, 170, 10, "up")
    wall_20 = Wall(374, 816, 10, 150, "right")
    wall_21 = Wall(409, 0, 200, 10, "down")
    wall_22 = Wall(386, 905, 500, 10, "up")

    wall_group = pygame.sprite.Group(
        wall_1,
        wall_2,
        wall_3,
        wall_4,
        wall_5,
        wall_6,
        wall_7,
        wall_8,
        wall_9,
        wall_10,
        wall_11,
        wall_12,
        wall_13,
        wall_14,
        wall_15,
        wall_16,
        wall_17,
        wall_18,
        wall_19,
        wall_20,
        wall_21,
        wall_22,
    )
    fence_up = Fence()
    fence_up.rect.center = (500, 40)
    fence_down = Fence()
    fence_down.rect.center = (500, 914)

    start_button = StartButton()

    heart_1 = Heart()
    heart_1.rect.center = (50, 50)
    heart_2 = Heart()
    heart_2.rect.center = (125, 50)
    heart_3 = Heart()
    heart_3.rect.center = (200, 50)
    heart_4 = Heart()
    heart_4.is_able = False
    heart_4.rect.center = (275, 50)
    heart_5 = Heart()
    heart_5.is_able = False
    heart_5.rect.center = (350, 50)
    heart_group: list[Heart] = pygame.sprite.Group(
        heart_1, heart_2, heart_3, heart_4, heart_5
    )

    obstacle_group = pygame.sprite.Group()
    arrow_1 = Arrow("up")
    arrow_1.rect.center = (500, -300)
    obstacle_group.add(arrow_1)

    fireball_1 = AdvancedFireball((650, 550), (1150, 50), 1)
    fireball_2 = AdvancedFireball((500, 400), (1200, -300), 2)
    fireball_3 = AdvancedFireball((500, 500), (1400, -400), 3)
    fireball_4 = AdvancedFireball((500, 600), (1600, -500), 4)
    fireball_5 = AdvancedFireball((500, 700), (1800, -600), 5)
    fireball_6 = AdvancedFireball((600, 700), (1400, -100), 6)
    fireball_7 = AdvancedFireball((400, 600), (-500, -300), 7)
    fireball_8 = AdvancedFireball((500, 600), (1400, -300), 8)
    fireball_9 = AdvancedFireball((600, 600), (-300, -300), 9)
    fireball_10 = AdvancedFireball((700, 600), (1600, -300), 10)
    fireball_11 = AdvancedFireball((400, 500), (-600, -500), 11)
    fireball_12 = AdvancedFireball((500, 500), (1500, -500), 12)
    fireball_13 = AdvancedFireball((600, 500), (-400, -500), 13)
    fireball_14 = AdvancedFireball((700, 500), (1700, -500), 14)
    fireball_15 = AdvancedFireball((400, 400), (-700, -700), 15)
    fireball_16 = AdvancedFireball((500, 400), (1600, -700), 16)
    fireball_17 = AdvancedFireball((600, 400), (-500, -700), 17)
    fireball_18 = AdvancedFireball((700, 400), (1800, -700), 18)
    fireball_19 = AdvancedFireball((400, 300), (-800, -900), 19)
    fireball_20 = AdvancedFireball((500, 300), (1700, -900), 20)
    fireball_21 = AdvancedFireball((600, 300), (-600, -900), 21)
    fireball_22 = AdvancedFireball((400, 200), (1700, -1100), 22)
    fireball_23 = AdvancedFireball((500, 200), (-800, -1100), 23)
    fireball_24 = AdvancedFireball((600, 200), (1900, -1100), 24)
    fireball_25 = AdvancedFireball((400, 100), (-1000, -1300), 25)
    fireball_26 = AdvancedFireball((500, 100), (1900, -1300), 26)
    fireball_27 = AdvancedFireball((600, 100), (-800, -1300), 27)
    fireball_group: list[AdvancedFireball] = pygame.sprite.Group(
        fireball_1, fireball_2, fireball_3, fireball_4, fireball_5
    )

    cat = Cat()

    portal = LevelOnePortal()
    portal.rect.center = (500, 40)

    game_font = pygame.font.SysFont("monospace", 24)
    message = game_font.render("Save the cat!", True, (0, 0, 0))

    while is_playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_playing = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # https://stackoverflow.com/questions/10990137/pygame-mouse-clicking-detection
                pos = pygame.mouse.get_pos()
                if start_button.rect.collidepoint(pos):
                    level_started = True
                    wave_1_started = True
                    show_message = True
                    pygame.time.set_timer(show_message_event, 1000)
            if event.type == show_message_event:
                show_message = False
                pygame.event.clear(show_message_event)

            if event.type == wave_4_end_event:
                wave_4_started = False
                wave_5_started = True
                pygame.event.clear(wave_4_end_event)
                # be ready for wave 5 (final wave)
                # initialize fireball 1
                fireball_1.adjust_location((500, 850), (-200, 150))
                fireball_1.init_stat()
                pygame.time.set_timer(fireball_1.warning_event, 1200)
                # initialize fireball 2
                fireball_2.adjust_location((600, 850), (1300, 150))
                fireball_2.init_stat()
                pygame.time.set_timer(fireball_2.warning_event, 1200)
                # fireball 3
                fireball_3.adjust_location((300, 700), (-500, -100))
                fireball_3.init_stat()
                pygame.time.set_timer(fireball_3.warning_event, 1200)
                # fireball 4
                fireball_4.adjust_location((400, 700), (1200, -100))
                fireball_4.init_stat()
                pygame.time.set_timer(fireball_4.warning_event, 1200)
                # fireball 5
                fireball_5.adjust_location((500, 700), (-300, -100))
                fireball_5.init_stat()
                pygame.time.set_timer(fireball_5.warning_event, 1200)
                # fireball 6 and after
                pygame.time.set_timer(fireball_6.warning_event, 1200)
                pygame.time.set_timer(fireball_7.warning_event, 1200)
                pygame.time.set_timer(fireball_8.warning_event, 1200)
                pygame.time.set_timer(fireball_9.warning_event, 1200)
                pygame.time.set_timer(fireball_10.warning_event, 1200)
                pygame.time.set_timer(fireball_11.warning_event, 1200)
                pygame.time.set_timer(fireball_12.warning_event, 1200)
                pygame.time.set_timer(fireball_13.warning_event, 1200)
                pygame.time.set_timer(fireball_14.warning_event, 1200)
                pygame.time.set_timer(fireball_15.warning_event, 1200)
                pygame.time.set_timer(fireball_16.warning_event, 1200)
                pygame.time.set_timer(fireball_17.warning_event, 1200)
                pygame.time.set_timer(fireball_18.warning_event, 1200)
                pygame.time.set_timer(fireball_19.warning_event, 1200)
                pygame.time.set_timer(fireball_20.warning_event, 1200)
                pygame.time.set_timer(fireball_21.warning_event, 1200)
                pygame.time.set_timer(fireball_22.warning_event, 1200)
                pygame.time.set_timer(fireball_23.warning_event, 1200)
                pygame.time.set_timer(fireball_24.warning_event, 1200)
                pygame.time.set_timer(fireball_25.warning_event, 1200)
                pygame.time.set_timer(fireball_26.warning_event, 1200)
                pygame.time.set_timer(fireball_27.warning_event, 1200)

                # group
                fireball_group = pygame.sprite.Group(
                    fireball_1,
                    fireball_2,
                    fireball_3,
                    fireball_4,
                    fireball_5,
                    fireball_6,
                    fireball_7,
                    fireball_8,
                    fireball_9,
                    fireball_10,
                    fireball_11,
                    fireball_12,
                    fireball_13,
                    fireball_14,
                    fireball_15,
                    fireball_16,
                    fireball_17,
                    fireball_18,
                    fireball_19,
                    fireball_20,
                    fireball_21,
                    fireball_22,
                    fireball_23,
                    fireball_24,
                    fireball_25,
                    fireball_26,
                    fireball_27,
                )
                pygame.time.set_timer(ending_event, 1400)
            if event.type == ending_event:
                fence_broken = True
                portal_unlocked = True

            if event.type == fireball_1.warning_event_type:
                fireball_1.show_warning = False
            if event.type == fireball_1.effect_event_type:
                fireball_1.show_effect = False

            if event.type == fireball_2.warning_event_type:
                fireball_2.show_warning = False
            if event.type == fireball_2.effect_event_type:
                fireball_2.show_effect = False

            if event.type == fireball_3.warning_event_type:
                fireball_3.show_warning = False
            if event.type == fireball_3.effect_event_type:
                fireball_3.show_effect = False

            if event.type == fireball_4.warning_event_type:
                fireball_4.show_warning = False
            if event.type == fireball_4.effect_event_type:
                fireball_4.show_effect = False

            if event.type == fireball_5.warning_event_type:
                fireball_5.show_warning = False
            if event.type == fireball_5.effect_event_type:
                fireball_5.show_effect = False

            if event.type == fireball_6.warning_event_type:
                fireball_6.show_warning = False
            if event.type == fireball_6.effect_event_type:
                fireball_6.show_effect = False

            if event.type == fireball_7.warning_event_type:
                fireball_7.show_warning = False
            if event.type == fireball_7.effect_event_type:
                fireball_7.show_effect = False

            if event.type == fireball_8.warning_event_type:
                fireball_8.show_warning = False
            if event.type == fireball_8.effect_event_type:
                fireball_8.show_effect = False

            if event.type == fireball_9.warning_event_type:
                fireball_9.show_warning = False
            if event.type == fireball_9.effect_event_type:
                fireball_9.show_effect = False

            if event.type == fireball_10.warning_event_type:
                fireball_10.show_warning = False
            if event.type == fireball_10.effect_event_type:
                fireball_10.show_effect = False

            if event.type == fireball_11.warning_event_type:
                fireball_11.show_warning = False
            if event.type == fireball_11.effect_event_type:
                fireball_11.show_effect = False

            if event.type == fireball_12.warning_event_type:
                fireball_12.show_warning = False
            if event.type == fireball_12.effect_event_type:
                fireball_12.show_effect = False

            if event.type == fireball_13.warning_event_type:
                fireball_13.show_warning = False
            if event.type == fireball_13.effect_event_type:
                fireball_13.show_effect = False

            if event.type == fireball_14.warning_event_type:
                fireball_14.show_warning = False
            if event.type == fireball_14.effect_event_type:
                fireball_14.show_effect = False

            if event.type == fireball_15.warning_event_type:
                fireball_15.show_warning = False
            if event.type == fireball_15.effect_event_type:
                fireball_15.show_effect = False

            if event.type == fireball_16.warning_event_type:
                fireball_16.show_warning = False
            if event.type == fireball_16.effect_event_type:
                fireball_16.show_effect = False

            if event.type == fireball_17.warning_event_type:
                fireball_17.show_warning = False
            if event.type == fireball_17.effect_event_type:
                fireball_17.show_effect = False

            if event.type == fireball_18.warning_event_type:
                fireball_18.show_warning = False
            if event.type == fireball_18.effect_event_type:
                fireball_18.show_effect = False

            if event.type == fireball_19.warning_event_type:
                fireball_19.show_warning = False
            if event.type == fireball_19.effect_event_type:
                fireball_19.show_effect = False

            if event.type == fireball_20.warning_event_type:
                fireball_20.show_warning = False
            if event.type == fireball_20.effect_event_type:
                fireball_20.show_effect = False

            if event.type == fireball_21.warning_event_type:
                fireball_21.show_warning = False
            if event.type == fireball_21.effect_event_type:
                fireball_21.show_effect = False

            if event.type == fireball_22.warning_event_type:
                fireball_22.show_warning = False
            if event.type == fireball_22.effect_event_type:
                fireball_22.show_effect = False

            if event.type == fireball_23.warning_event_type:
                fireball_23.show_warning = False
            if event.type == fireball_23.effect_event_type:
                fireball_23.show_effect = False

            if event.type == fireball_24.warning_event_type:
                fireball_24.show_warning = False
            if event.type == fireball_24.effect_event_type:
                fireball_24.show_effect = False

            if event.type == fireball_25.warning_event_type:
                fireball_25.show_warning = False
            if event.type == fireball_25.effect_event_type:
                fireball_25.show_effect = False

            if event.type == fireball_26.warning_event_type:
                fireball_26.show_warning = False
            if event.type == fireball_26.effect_event_type:
                fireball_26.show_effect = False

            if event.type == fireball_27.warning_event_type:
                fireball_27.show_warning = False
            if event.type == fireball_27.effect_event_type:
                fireball_27.show_effect = False

        wall_list: list[Wall] = pygame.sprite.spritecollide(
            cat, wall_group, False, pygame.sprite.collide_rect
        )
        for wall in wall_list:
            pos = wall.bounce()
            cat.rect.move_ip(pos)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            cat.rect.move_ip((0, -5))
        if keys[pygame.K_a]:
            cat.rect.move_ip((-5, 0))
        if keys[pygame.K_s]:
            cat.rect.move_ip((0, 5))
        if keys[pygame.K_d]:
            cat.rect.move_ip((5, 0))

        screen.blit(game_map, game_map_rect)
        if not fence_broken:
            screen.blit(fence_up.image, fence_up.rect)
        screen.blit(fence_down.image, fence_down.rect)
        screen.blit(cat.image, cat.rect)

        if portal_unlocked:
            screen.blit(portal.image, portal.rect)
            if pygame.sprite.collide_mask(cat, portal):
                return True
                pygame.quit()

        for heart in heart_group:
            if heart.is_able:
                screen.blit(heart.image, heart.rect)

        if show_message and wave_1_started:
            screen.blit(message, (470, 480))

        if not level_started:
            screen.blit(start_button.image, start_button.rect)

        if wave_1_started:
            if not arrow_1.hit:
                screen.blit(arrow_1.image, arrow_1.rect)
            arrow_1.move("down", 10)
            if frame_number % 3 == 0:
                collide_list = pygame.sprite.spritecollide(
                    cat, obstacle_group, True, pygame.sprite.collide_mask
                )
                if collide_list:
                    arrow_1.hit = True
                    heart_3.damage()
            # arrow is outside the screen
            if arrow_1.rect.y >= 1024:
                wave_2_started = True
                wave_1_started = False
                # be ready for wave 2
                # initialize the arrow 1
                arrow_1.hit = False
                arrow_1.rect.center = (500, -300)
                if not arrow_1 in obstacle_group:
                    obstacle_group.add(arrow_1)
                # initialize the arrow 2
                arrow_2 = Arrow(135)
                arrow_2.rect.center = (800, 200)
                obstacle_group.add(arrow_2)

        if wave_2_started:
            if not arrow_1.hit:
                screen.blit(arrow_1.image, arrow_1.rect)
            if not arrow_2.hit:
                screen.blit(arrow_2.image, arrow_2.rect)
            arrow_1.move("down", 10)
            arrow_2.move("down", 12)
            arrow_2.move("left", 12)
            collide_list = pygame.sprite.spritecollide(
                cat, obstacle_group, True, pygame.sprite.collide_mask
            )
            for arrow in collide_list:
                arrow.hit = True
                if heart_3.filled:
                    heart_3.damage()
                elif heart_2.filled:
                    heart_2.damage()
                else:
                    # lose every heart
                    # you lost
                    return False
                    pygame.quit()

            if arrow_1.rect.y >= 1024:
                # be ready for wave 3
                wave_2_started = False
                wave_3_started = True
                obstacle_group.add(fireball_1)
                pygame.time.set_timer(fireball_1.warning_event, 1200)
                pygame.event.clear(show_message_event)
                add_heart_potion = AddHeartPotion()
                add_heart_potion.rect.center = (500, 300)

        if wave_3_started:
            if fireball_1.show_warning:
                screen.blit(fireball_1.warning_img, fireball_1.warning_rect)
            if fireball_1.rect.center == fireball_1.dest:
                fireball_1.hit = True
                pygame.time.set_timer(fireball_1.effect_event, 800)
                screen.blit(fireball_1.effect.image, fireball_1.effect.rect)
                fireball_1.show_effect = True
                if pygame.sprite.collide_mask(cat, fireball_1.effect):
                    if heart_3.filled and heart_2.filled:
                        heart_3.damage()
                        heart_2.damage()
                    else:
                        return False
                        pygame.quit()
                fireball_1.rect.center = (0, 0)
            else:
                fireball_1.move("down", 5)
                fireball_1.move("left", 5)
            if fireball_1.show_effect:
                screen.blit(fireball_1.effect.image, fireball_1.effect.rect)
            if not fireball_1.hit:
                screen.blit(fireball_1.image, fireball_1.rect)
            elif add_heart_potion.filled:
                screen.blit(add_heart_potion.image, add_heart_potion.rect)
                if pygame.sprite.collide_mask(cat, add_heart_potion):
                    add_heart_potion.filled = False
                    if heart_3.filled:
                        heart_4.is_able = True
                    elif heart_2.filled:
                        heart_3.restore()
                    elif heart_1.filled:
                        heart_2.restore()
            else:
                # be ready for wave 4
                wave_3_started = False
                wave_4_started = True

                # fireball 1
                fireball_1.adjust_location((500, 300), (1000, -200))
                fireball_1.init_stat()
                pygame.time.set_timer(fireball_1.warning_event, 1200)

                # fireball 2
                pygame.time.set_timer(fireball_2.warning_event, 1200)

                # fireball 3
                pygame.time.set_timer(fireball_3.warning_event, 1200)

                # fireball 4
                pygame.time.set_timer(fireball_4.warning_event, 1200)

                # fireball 5
                pygame.time.set_timer(fireball_5.warning_event, 1200)

        if wave_4_started:
            # fireball group code
            for fireball in fireball_group:
                if fireball.show_warning:
                    screen.blit(fireball.warning_img, fireball.warning_rect)
                if fireball.rect.center == fireball.dest:
                    fireball.hit = True
                    pygame.time.set_timer(fireball.effect_event, 800)
                    screen.blit(fireball.effect.image, fireball.effect.rect)
                    fireball.show_effect = True
                    if pygame.sprite.collide_mask(cat, fireball.effect):
                        if heart_4.is_able and heart_4.filled:
                            # ❤️❤️❤️❤️
                            heart_4.damage()
                            heart_3.damage()
                        elif heart_3.filled:
                            # ❤️❤️❤️🤍 or ❤️❤️❤️
                            heart_3.damage()
                            heart_2.damage()
                        else:
                            # game over
                            return False
                            pygame.quit()
                    fireball.rect.center = (0, 0)
                else:
                    fireball.move("down", 10)
                    fireball.move("left", 10)
                if not fireball.hit:
                    screen.blit(fireball.image, fireball.rect)
                if fireball.show_effect:
                    screen.blit(fireball.effect.image, fireball.effect.rect)
            if fireball_5.rect.center == (0, 0):
                pygame.time.set_timer(wave_4_end_event, 2500)

        if wave_5_started:
            # fireball group code
            for fireball in fireball_group:
                if fireball.show_warning:
                    screen.blit(fireball.warning_img, fireball.warning_rect)
                if fireball.rect.center == fireball.dest:
                    fireball.hit = True
                    pygame.time.set_timer(fireball.effect_event, 800)
                    screen.blit(fireball.effect.image, fireball.effect.rect)
                    fireball.show_effect = True
                    if pygame.sprite.collide_mask(cat, fireball.effect):
                        if heart_4.is_able and heart_4.filled:
                            # ❤️❤️❤️❤️
                            heart_4.damage()
                            heart_3.damage()
                        elif heart_3.filled:
                            # ❤️❤️❤️🤍 or ❤️❤️❤️
                            heart_3.damage()
                            heart_2.damage()
                        else:
                            # game over
                            return False
                            pygame.quit()
                    fireball.rect.center = (0, 0)
                elif fireball.obj_id % 2 == 0:
                    fireball.move("down", 10)
                    fireball.move("left", 10)
                else:
                    fireball.move("down", 10)
                    fireball.move("right", 10)
                if not fireball.hit:
                    screen.blit(fireball.image, fireball.rect)
                if fireball.show_effect:
                    screen.blit(fireball.effect.image, fireball.effect.rect)

        frame_number += 0.5
        pygame.display.update()
        clock.tick(60)
    pygame.quit()

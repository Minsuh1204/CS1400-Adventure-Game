# Images are mostly created by the Copilot of Microsoft unless the source is written
# Written by Minsuh Chang
import random

from components import *


def level3(subclass: MagiCat | HunterCat):
    """
    Final level of the game with boss fight.
    :param subclass: The class of the cat
    :return: True / False
    """
    pygame.init()
    clock = pygame.time.Clock()

    is_playing = True
    game_started = False
    dragon_alive = True

    screen = pygame.display.set_mode((1200, 800))

    # font from: https://www.1001fonts.com/lodeh-regular-font.html
    # https://stackoverflow.com/questions/34575639/how-to-use-other-fonts-in-pygame
    lodeh_regular_font = pygame.font.Font("./assets/Lodeh Regular.ttf", 30)

    class CriticalMessage:
        def __init__(self, frame: int):
            self.message = lodeh_regular_font.render("Critical", True, (255, 255, 0))
            self.show = True
            self.frame_number = frame
            self.location = None

    critical_message_list = []

    # original image from: https://www.vecteezy.com/free-vector/green-grass-field
    # reddish version of green field image using custom filter from A5
    reddish_field = pygame.image.load("./assets/reddish_grass.png")
    reddish_field = pygame.transform.smoothscale(
        reddish_field, (1200, 800)
    ).convert_alpha()
    reddish_field_rect = reddish_field.get_rect()

    wall_1 = Wall(0, -30, 1200, 7, "down")
    wall_2 = Wall(1240, 0, 7, 800, "left")
    wall_3 = Wall(0, 820, 1200, 7, "up")
    wall_4 = Wall(-20, 0, 7, 800, "right")
    wall_group = pygame.sprite.Group(wall_1, wall_2, wall_3, wall_4)

    start_button = StartButton()
    start_button.rect.center = (620, 500)

    final_portal = LevelOnePortal()
    final_portal.rect.center = (620, 300)

    dragon = EvilDragon()
    dragon.rect.center = (600, 100)
    evil_group = pygame.sprite.Group(dragon)
    dragon_fireball_group: pygame.sprite.Group[AdvancedFireball] = pygame.sprite.Group()

    cat = Cat()
    cat.change_class(subclass.class_name)
    cat.rect.center = (620, 700)

    cat_hearts_group_1: pygame.sprite.Group[Heart] = pygame.sprite.Group(
        *[Heart() for i in range(4)]
    )
    cat_hearts_group_2: pygame.sprite.Group[Heart] = pygame.sprite.Group(
        *[Heart() for i in range(4)]
    )

    frame_number = 0

    while is_playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_playing = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button.rect.collidepoint(mouse_pos):
                    game_started = True

                if game_started:
                    cat.left_click_attack(mouse_pos)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            cat.rect.move_ip(0, -5)
        if keys[pygame.K_a]:
            cat.rect.move_ip(-5, 0)
        if keys[pygame.K_s]:
            cat.rect.move_ip(0, 5)
        if keys[pygame.K_d]:
            cat.rect.move_ip(5, 0)

        wall_collide: list[Wall] = pygame.sprite.spritecollide(
            cat, wall_group, False, pygame.sprite.collide_rect
        )
        for wall in wall_collide:
            cat.rect.move_ip(wall.bounce())

        dragon_health_bar_text = f"{round(dragon.current_hp,1)} / {dragon.MAX_HP}"
        dragon_health = lodeh_regular_font.render(
            dragon_health_bar_text, True, (255, 0, 0)
        )

        screen.blit(reddish_field, reddish_field_rect)
        screen.blit(cat.image, cat.rect)
        if dragon_alive:
            screen.blit(dragon.image, dragon.rect)
            screen.blit(dragon_health, (520, 400))
        else:
            screen.blit(final_portal.image, final_portal.rect)
            if pygame.sprite.collide_mask(cat, final_portal):
                return True

        # show cat heart
        heart_x = 20
        heart_y = 20
        heart_x_diff = 80
        i = 0
        for heart in cat_hearts_group_1:
            screen.blit(heart.image, (heart_x + heart_x_diff * i, heart_y))
            i += 1
        heart_y = 100
        i = 0
        for heart in cat_hearts_group_2:
            screen.blit(heart.image, (heart_x + heart_x_diff * i, heart_y))
            i += 1

        if not game_started:
            screen.blit(start_button.image, start_button.rect)

        # dragon fireball movement
        # fireball is always from right-up side
        for fireball in dragon_fireball_group:
            fireball.move("left", 5)
            fireball.move("down", 5)
            if frame_number - fireball.frame_number == 20:
                # 1200ms, 1.2s
                fireball.turn_off_warning()
            if fireball.show_warning:
                screen.blit(fireball.warning_img, fireball.warning_rect)
            if fireball.show_effect:
                screen.blit(fireball.effect.image, fireball.effect.rect)
                # check if it collides with our precious cat
                if pygame.sprite.collide_mask(cat, fireball.effect):
                    cat_hearts_full_list: list[Heart] = (
                        cat_hearts_group_1.sprites()[::-1]
                        + cat_hearts_group_2.sprites()[::-1]
                    )
                    # turn off its effect to prevent duplication of damage
                    if not fireball.damage_applied:
                        for heart in cat_hearts_full_list:
                            # after damage just 1 heart, break the for loop
                            if heart.filled:
                                heart.damage()
                                fireball.flip_damage_applied()
                                if not cat_hearts_full_list[-1].filled:
                                    return False
                                break

            if not fireball.hit:
                screen.blit(fireball.image, fireball.rect)
            if fireball.rect.center == fireball.dest:
                fireball.change_hit()
                fireball.turn_on_effect(frame_number)
            if (
                fireball.hit_frame is not None
                and frame_number - fireball.hit_frame == 15
            ):
                # 900ms, 0.9s
                fireball.turn_off_effect()

        # cat skill onboard
        skill_onboard: pygame.sprite.Group[Lightning, HunterArrow] = (
            cat.subclass.skill_onboard
        )
        for skill in skill_onboard:
            skill.move()
            if not skill.hit:
                screen.blit(skill.image, skill.rect)
                if pygame.sprite.spritecollide(
                    skill, evil_group, False, pygame.sprite.collide_mask
                ):
                    skill.hit = True
                    random_for_critical = random.random()
                    damage = skill.DAMAGE
                    if random_for_critical <= skill.CRITICAL_POSSIBILITY:
                        damage *= skill.CRITICAL_RATIO
                        critical_message_list.append(CriticalMessage(frame_number))
                    dragon.current_hp -= damage
                    if dragon.current_hp <= 0:
                        dragon_alive = False

        # show critical message
        start_x = 550
        start_y = 180
        y_diff = 50
        for i in range(len(critical_message_list)):
            message = critical_message_list[i]
            if message.location is None:
                location = (start_x, start_y + y_diff * i)
                critical_message_list[i].location = location
                message.location = location
            if message.show:
                screen.blit(message.message, message.location)
            if frame_number - message.frame_number == 10:
                # 10 x 60 = 600, 0.6s elapsed
                critical_message_list[i].show = False
        # remove old critical messages
        critical_message_list = [
            message for message in critical_message_list if message.show
        ]
        frame_number += 1

        # initialize dragon's attack
        # screen: 1200 x 800
        if frame_number % 150 == 0 and game_started and dragon_alive:
            dragon_fireball_group.empty()
            # 60 x 150 = 9000, 9s elapsed
            for i in range(7):
                dest_collide_with_dragon = True
                while dest_collide_with_dragon:
                    random_dest_x = random.randint(50, 1150)
                    random_dest_y = random.randint(50, 750)
                    dest_collide_with_dragon = dragon.rect.collidepoint(
                        random_dest_x, random_dest_y
                    )
                fireball = AdvancedFireball(
                    (random_dest_x, random_dest_y),
                    (random_dest_x + 500, random_dest_y - 500),
                    i,
                    frame_number,
                )
                dragon_fireball_group.add(fireball)

        # initialize health potion
        if frame_number % 500 == 0 and dragon_alive:
            # 60 * 500 = 30000 / 30000ms = 30s
            potion_location_not_decided = True
            while potion_location_not_decided:
                random_x = random.randint(50, 1150)
                random_y = random.randint(50, 750)
                potion_location_not_decided = cat.rect.collidepoint(
                    random_x, random_y
                ) or dragon.rect.collidepoint(random_x, random_y)
            potion = AddHeartPotion()
            potion.rect.center = random_x, random_y

        # show it to screen
        if frame_number >= 500 and potion.filled:
            screen.blit(potion.image, potion.rect)
            if pygame.sprite.collide_mask(cat, potion):
                potion.drink()
                cat_hearts_full_list: list[Heart] = (
                    cat_hearts_group_1.sprites()[::-1]
                    + cat_hearts_group_2.sprites()[::-1]
                )[::-1]
                for heart in cat_hearts_full_list:
                    if not heart.filled:
                        heart.restore()
                        break

        pygame.display.update()
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    level3(HunterCat())

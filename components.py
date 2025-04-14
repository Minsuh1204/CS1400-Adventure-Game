# Written by Minsuh Chang

import math
import pygame


# https://stackoverflow.com/questions/41986383/pygame-what-is-the-difference-between-an-image-and-a-sprite
class Heart(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.filled = True
        self.is_able = True
        # heart image from: https://opengameart.org/content/heart-pixel-art
        original_img = pygame.image.load("./assets/heart.png")
        self.image = pygame.transform.smoothscale(original_img, (70, 70))
        self.rect = self.image.get_rect()

    def damage(self):
        """
        Damage the heart and change it to blank heart.
        :return: None
        """
        blank_heart = pygame.image.load("./assets/blank heart.png")
        self.image = pygame.transform.smoothscale(blank_heart, (70, 70))
        self.filled = False

    def restore(self):
        """
        Restore the heart and change it to the filled heart.
        :return: None
        """
        original_img = pygame.image.load("./assets/heart.png")
        self.image = pygame.transform.smoothscale(original_img, (70, 70))
        self.filled = True


class Arrow(pygame.sprite.Sprite):
    def __init__(self, side_from: str | float):
        super().__init__()
        self.hit = False
        # arrow image from: https://opengameart.org/content/arrow-0
        original_img = pygame.image.load("./assets/Arrow.png")
        resized = pygame.transform.smoothscale(original_img, (20, 180))
        match side_from:
            case "up":
                final = pygame.transform.flip(resized, False, True)
            case "down":
                final = resized
            case "right":
                final = pygame.transform.rotate(resized, -90)
            case "left":
                final = pygame.transform.rotate(resized, 90)
            case _:
                # custom angle
                final = pygame.transform.rotate(resized, float(side_from))
        self.image = final
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def move(self, side: str, length: int):
        """
        Move the arrow with given side and length.
        :param side: up / down / left / right
        :param length: distance of the movement
        :return: None
        """
        match side:
            case "up":
                self.rect.move_ip(0, -length)
            case "down":
                self.rect.move_ip(0, length)
            case "right":
                self.rect.move_ip(length, 0)
            case "left":
                self.rect.move_ip(-length, 0)


# old fireball
class Fireball(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.surface.Surface):
        super().__init__()
        self.hit = False
        self.screen = screen
        original_img = pygame.image.load("./assets/fireball.png")
        self.image = pygame.transform.smoothscale(original_img, (200, 200))
        self.rect = self.image.get_rect()
        self.effect = ExplosionEffect()
        # warning image from: https://www.freepik.com/premium-vector/red-exclamation-mark-triangle-shape-with-pixel-art-style_19580734.htm
        warning = pygame.image.load("./assets/warning.png")
        self.warning_img = pygame.transform.smoothscale(warning, (100, 100))
        self.warning_rect = self.warning_img.get_rect()

    def move(self, side: str, length: int):
        """
        Move the fireball with given side and length.
        :param side: up / down / left / right
        :param length: distance for the movement
        :return: None
        """
        match side:
            case "up":
                self.rect.move_ip(0, -length)
            case "down":
                self.rect.move_ip(0, length)
            case "right":
                self.rect.move_ip(length, 0)
            case "left":
                self.rect.move_ip(-length, 0)


class AdvancedFireball(pygame.sprite.Sprite):
    def __init__(
        self,
        dest: tuple[int, int],
        departure: tuple[int, int],
        obj_id: int,
        frame: int = -1,
    ):
        super().__init__()
        self.EVENT_START_ID = 33000
        self.hit = False
        self.show_warning = True
        self.show_effect = False
        self.dest = dest
        self.departure = departure
        self.obj_id = obj_id
        original_img = pygame.image.load("./assets/fireball.png")
        self.image = pygame.transform.smoothscale(original_img, (200, 200))
        self.rect = self.image.get_rect()
        self.effect = ExplosionEffect()
        # warning image from: https://www.freepik.com/premium-vector/red-exclamation-mark-triangle-shape-with-pixel-art-style_19580734.htm
        warning = pygame.image.load("./assets/warning.png")
        self.warning_img = pygame.transform.smoothscale(warning, (100, 100))
        self.warning_rect = self.warning_img.get_rect()
        # adjust location
        self.adjust_location(dest, departure)
        # make event
        self.warning_event_type = self.EVENT_START_ID + obj_id * 2
        self.warning_event = pygame.event.Event(self.warning_event_type)
        self.effect_event_type = self.warning_event_type + 1
        self.effect_event = pygame.event.Event(self.effect_event_type)
        self.frame_number = frame
        self.hit_frame = None
        self.damage_applied = False

    def move(self, side: str, length: int):
        """
        Move the fireball with given side and length.
        :param side: up / down / left / right
        :param length: distance for the movement
        :return: None
        """
        match side:
            case "up":
                self.rect.move_ip(0, -length)
            case "down":
                self.rect.move_ip(0, length)
            case "right":
                self.rect.move_ip(length, 0)
            case "left":
                self.rect.move_ip(-length, 0)

    def adjust_location(self, dest: tuple[int, int], departure: tuple[int, int]):
        """
        Adjust the location of the fireball's destination and departure.
        :param dest: destination of the fireball
        :param departure: departure of the fireball
        :return: None
        """
        self.dest = dest
        self.departure = departure
        self.warning_rect.center = dest
        self.effect.rect.center = dest
        self.rect.center = departure

    def init_stat(self):
        """
        Initialize the essential status.
        :return: None
        """
        self.show_warning = True
        self.show_effect = False
        self.hit = False

    def turn_on_effect(self, frame: int):
        """
        Turn on the explosion effect.
        :param frame: frame number of when the fireball hit.
        :return: None
        """
        self.show_effect = True
        self.hit_frame = frame

    def turn_off_effect(self):
        """
        Turn off the explosion effect.
        :return: None
        """
        self.show_effect = False

    def change_hit(self):
        """
        Flip the value of hit.
        :return: None
        """
        if self.hit:
            self.hit = False
        else:
            self.hit = True

    def flip_damage_applied(self):
        """
        Flip the value of damage_applied.
        :return: None
        """
        if not self.damage_applied:
            self.damage_applied = True

    def turn_off_warning(self):
        """
        Turn off the warning.
        :return: None
        """
        self.show_warning = False


class ExplosionEffect(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        explosion_effect = pygame.image.load("./assets/explosion_effect.png")
        self.image = pygame.transform.smoothscale(explosion_effect, (200, 120))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)


class Cat(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        cat = pygame.image.load("./assets/cat.png")
        self.image = pygame.transform.smoothscale(cat, (100, 100)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (500, 400)
        self.mask = pygame.mask.from_surface(self.image)
        self.subclass = None

    def change_class(self, subclass: str):
        """
        Change class to MagiCat / HunterCat
        :param subclass: name of the class.
        :return: None
        """
        self.subclass = subclass
        match subclass:
            case "MagiCat":
                magicat = pygame.image.load("./assets/magicat.png")
                self.image = pygame.transform.smoothscale(magicat, (200, 200))
                # self.rect.move_ip(0, 30)
                self.subclass = MagiCat()
            case "HunterCat":
                huntercat = pygame.image.load("./assets/huntercat.png")
                self.image = pygame.transform.smoothscale(huntercat, (180, 180))
                # self.rect.move_ip(0, -10)
                self.subclass = HunterCat()

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def left_click_attack(self, cursor_pos: tuple[int, int]):
        """
        Call the subclasses' left_click_attack function with the position of mouse.
        :param cursor_pos: the position of the mouse
        :return: None
        """
        self.subclass.left_click_attack(self.rect.center, cursor_pos)


class MagiCat:
    def __init__(self):
        self.class_name = "MagiCat"
        self.RANGE = 1000
        self.BASE_DAMAGE = 5
        self.skill_onboard = pygame.sprite.Group()

    def left_click_attack(self, cat_pos: tuple[int, int], target_pos: tuple[int, int]):
        """
        Represent the left click attack of the MagiCat
        :param cat_pos: position of the cat
        :param target_pos: position of the target
        :return: None
        """
        if self.in_range(cat_pos, target_pos):
            lightning = Lightning(target_pos, cat_pos)
            self.skill_onboard.add(lightning)

    def in_range(self, cat_pos: tuple[int, int], target_pos: tuple[int, int]):
        """
        Check if the target is in range.
        :param cat_pos: position of the cat
        :param target_pos: position of the target
        :return: None
        """
        return calculate_distance(cat_pos, target_pos) <= self.RANGE


class HunterCat:
    def __init__(self):
        self.class_name = "HunterCat"
        self.RANGE = 1000
        self.BASE_DAMAGE = 3
        self.skill_onboard = pygame.sprite.Group()

    def left_click_attack(self, cat_pos: tuple[int, int], target_pos: tuple[int, int]):
        """
        Represent the left click attack of the HunterCat
        :param cat_pos: position of the cat
        :param target_pos: position of the target
        :return: None
        """
        if self.in_range(cat_pos, target_pos):
            hunter_arrow = HunterArrow(target_pos, cat_pos)
            self.skill_onboard.add(hunter_arrow)

    def in_range(self, cat_pos: tuple[int, int], target_pos: tuple[int, int]):
        """
        Check if the target is in range
        :param cat_pos: position of the cat
        :param target_pos: position of the target
        :return: None
        """
        return calculate_distance(cat_pos, target_pos) <= self.RANGE


class HunterArrow(pygame.sprite.Sprite):
    def __init__(self, dest: tuple[int, int], departure: tuple[int, int]):
        super().__init__()
        # basically same image from Arrow class...
        arrow = pygame.image.load("./assets/arrow_rotated.png")
        arrow = pygame.transform.smoothscale(arrow, (180, 20))
        angle = calculate_angle(departure, dest)
        if departure[1] < dest[1]:
            angle *= -1

        self.image = pygame.transform.rotate(arrow, angle)
        self.angle = angle
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = departure
        self.dest = dest
        self.departure = departure
        self.MAX_VELOCITY = 10
        self.DAMAGE = 5
        self.CRITICAL_POSSIBILITY = 0.2
        self.CRITICAL_RATIO = 1.9
        self.hit = False

    def move(self):
        """
        Automatically move the arrow toward the target.
        :return: None
        """
        try:
            slope = (self.dest[1] - self.departure[1]) / (
                self.dest[0] - self.departure[0]
            )
        except ZeroDivisionError:
            slope = self.MAX_VELOCITY
        distance = calculate_distance(self.departure, self.dest)
        divider = distance / self.MAX_VELOCITY
        velocity = distance / divider
        x_velocity = velocity
        y_velocity = velocity * slope

        if self.dest[0] - self.departure[0] < 0:
            x_velocity *= -1
            y_velocity *= -1
        while (x_velocity**2 + y_velocity**2) ** (1 / 2) > 5:
            x_velocity *= 0.9
            y_velocity *= 0.9
        self.rect.move_ip(x_velocity, y_velocity)


class Lightning(pygame.sprite.Sprite):
    def __init__(self, dest: tuple[int, int], departure: tuple[int, int]):
        super().__init__()
        # image from: https://www.vectorstock.com/royalty-free-vector/lightning-pixel-art-vector-43632837
        lightning = pygame.image.load("./assets/lightning_effect.png")
        lightning = pygame.transform.smoothscale(lightning, (125, 135)).convert_alpha()
        angle = calculate_angle(departure, dest)
        self.angle = angle
        if departure[1] < dest[1]:
            angle *= -1
        self.image = pygame.transform.rotate(lightning, angle)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = departure
        self.dest = dest
        self.departure = departure
        self.MAX_VELOCITY = 5
        self.DAMAGE = 6
        self.CRITICAL_POSSIBILITY = -1
        self.CRITICAL_DAMAGE_RATIO = 0
        self.hit = False

    def move(self):
        """
        Automatically move the lightning toward the target.
        :return: None
        """
        try:
            slope = (self.dest[1] - self.departure[1]) / (
                self.dest[0] - self.departure[0]
            )
        except ZeroDivisionError:
            slope = self.MAX_VELOCITY
        distance = calculate_distance(self.departure, self.dest)
        divider = distance / self.MAX_VELOCITY
        velocity = distance / divider
        x_velocity = velocity
        y_velocity = velocity * slope

        if self.dest[0] - self.departure[0] < 0:
            x_velocity *= -1
            y_velocity *= -1
        while (x_velocity**2 + y_velocity**2) ** (1 / 2) > 5:
            x_velocity *= 0.9
            y_velocity *= 0.9
        self.rect.move_ip(x_velocity, y_velocity)


class Wall(pygame.sprite.Sprite):
    def __init__(
        self, left: int, top: int, width: int, height: int, bounce_direction: str
    ):
        self.bounce_direction = bounce_direction
        super().__init__()
        self.rect = pygame.Rect(left, top, width, height)

    def bounce(self) -> tuple[int, int]:
        """
        Make the effect of bouncing with it.
        :return: position to move
        """
        match self.bounce_direction:
            case "left":
                return -7, 0
            case "right":
                return 7, 0
            case "down":
                return 0, 7
            case "up":
                return 0, -7


class Fence(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # fence image from: https://www.freepik.com/premium-vector/pixel-art-wooden-fence-vector-icon-8bit-game-white-background_27462093.htm
        original_img = pygame.image.load("./assets/wooden_fence.png")
        self.image = pygame.transform.smoothscale(original_img, (124, 70))
        self.rect = self.image.get_rect()


class AddHeartPotion(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.filled = True
        original_img = pygame.image.load("assets/add_heart_potion.png")
        self.image = pygame.transform.smoothscale(original_img, (125, 125))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def drink(self):
        """
        Change the filled value to False.
        :return: None
        """
        self.filled = False


class LevelOnePortal(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # portal image from: https://idleslayer.fandom.com/wiki/Portals_and_Dimensions
        portal = pygame.image.load("./assets/purple_portal.webp")
        self.image = pygame.transform.smoothscale(portal, (170, 170))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)


class StartButton(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        start_button = pygame.image.load("./assets/start-btn.png")
        self.image = pygame.transform.smoothscale(start_button, (200, 200))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (500, 450)


class Advisor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # image from https://pngtree.com/freepng/flat-old-man-with-white-beard-free-of-charge_14083338.html
        advisor = pygame.image.load("./assets/advisor_image2.png")
        self.image = pygame.transform.smoothscale(advisor, (300, 300))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)


class WizardHat(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # image from: https://depositphotos.com/vectors/pixel-art-wizard-hat.html
        wizard_hat = pygame.image.load("./assets/wizard_hat.png")
        self.image = pygame.transform.smoothscale(wizard_hat, (100, 100))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)


class Crossbow(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # image from: https://no.pinterest.com/pin/crossbow-clipart-transparent-background--627407791859399347/
        crossbow = pygame.image.load("./assets/crossbow.png")
        self.image = pygame.transform.smoothscale(crossbow, (100, 100))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)


class DummyBot(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # image from: https://www.artstation.com/artwork/e0lr8P?album_id=984741
        dummy = pygame.image.load("./assets/training_dummy.png")
        self.image = pygame.transform.smoothscale(
            dummy, (125.25 * 1.5, 148.21 * 1.5)
        ).convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)


class EvilDragon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # image from:https://www.freepik.com/premium-ai-image/sinister-wings-unleashed-roaring-evil-dragon-rpg-sprite_63655077.htm
        dragon = pygame.image.load("./assets/evil_dragon.png")
        self.image = pygame.transform.smoothscale(dragon, (600, 600)).convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.MAX_HP = 2000.0
        self.current_hp = self.MAX_HP


def calculate_angle(cat_loc: tuple[int, int], target_loc: tuple[int, int]):
    """
    Calculate the angle between cat and the target to rotate the skill image.
    :param cat_loc: position of the cat
    :param target_loc: position of the target
    :return: angle value in degree
    """
    x_diff = target_loc[0] - cat_loc[0]
    d = calculate_distance(cat_loc, target_loc)
    # acos()-> radian
    # so change it to degree
    return math.acos(x_diff / d) * 180 / math.pi


def calculate_distance(cat_loc: tuple[int, int], target_loc: tuple[int, int]):
    """
    Calculate the distance between cat and the target.
    :param cat_loc: position of the cat
    :param target_loc: position of the target
    :return: distance (float)
    """
    x_diff = target_loc[0] - cat_loc[0]
    y_diff = target_loc[1] - cat_loc[1]
    return (x_diff**2 + y_diff**2) ** (1 / 2)

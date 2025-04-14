import pygame

# Starter code for an adventure game. Written by David Johnson for CS 1400 University of Utah.

# Finished game authors:
#
#


def pixel_collision(mask1, rect1, mask2, rect2):
    """
    Check if the non-transparent pixels of one mask contacts the non-transparent pixels of another.
    """
    offset_x = rect2[0] - rect1[0]
    offset_y = rect2[1] - rect1[1]
    # See if the two masks at the offset are overlapping.
    overlap = mask1.overlap(mask2, (offset_x, offset_y))
    return overlap is not None


def example_level1():
    """
    An example level of an adventure game with a key to find and door to open.

    :return:
    """

    # Initialize pygame
    pygame.init()

    map = pygame.image.load("assets/map.png")
    # Store window width and height in a tuple.
    map_size = map.get_size()
    map_rect = map.get_rect()

    # create the window based on the map size
    screen = pygame.display.set_mode(map_size)
    map = map.convert_alpha()

    # Change white pixels in the map to transparent. If your map already has
    # a transparent path, you should not do this.
    map.set_colorkey((255, 255, 255))
    map_mask = pygame.mask.from_surface(map)

    # You must replace these images with your own.
    # Create the player data
    player = pygame.image.load("assets/alien1.png").convert_alpha()
    player = pygame.transform.smoothscale(player, (25, 25))
    player_rect = player.get_rect()
    player_mask = pygame.mask.from_surface(player)

    # Create the key
    key = pygame.image.load("assets/key.png").convert_alpha()
    key = pygame.transform.smoothscale(key, (40, 40))
    key_rect = key.get_rect()
    key_rect.center = (300, 450)
    key_mask = pygame.mask.from_surface(key)

    # Create the door
    door = pygame.image.load("assets/door.png").convert_alpha()
    door = pygame.transform.smoothscale(door, (200, 200))
    door_rect = door.get_rect()
    door_rect.center = (550, 150)
    door_mask = pygame.mask.from_surface(door)

    # The frame tells which sprite frame to draw
    frame_count = 0

    # The clock helps us manage the frames per second of the animation
    clock = pygame.time.Clock()

    # Get a font to use to write on the screen.
    message_font = pygame.font.SysFont("monospace", 24)

    # The started variable records if the start color has been clicked and the level started
    started = False

    key_found = False
    # The is_alive variable records if anything bad has happened (off the path, touch guard, etc.)
    is_alive = True

    # Hide the arrow cursor and replace it with a sprite.
    pygame.mouse.set_visible(False)

    # This is the main game loop. In it, we must:
    # - check for events
    # - update the scene
    # - draw the scene
    while is_alive:
        # Check events by looping over the list of events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_alive = False

        # Update the game state in this region.
        # Position the player to the mouse location
        pos = pygame.mouse.get_pos()
        player_rect.center = pos

        # See if we touch the maze walls
        if pixel_collision(player_mask, player_rect, map_mask, map_rect):
            print("colliding", frame_count)  # Don't leave this in the game

        # Check for collision with the door if it is not opened by the key.
        if not key_found and pixel_collision(
            player_mask, player_rect, door_mask, door_rect
        ):
            print("colliding with door")  # Don't leave this in the game
            return False  # return False to show level fail

        if not key_found and pixel_collision(
            player_mask, player_rect, key_mask, key_rect
        ):
            key_found = True
            print("colliding with key")  # Don't leave this in the game

        # Draw game characters here.
        # Do not intermingle updates and drawing.
        # Do updates above and drawing below.
        # Draw the background
        screen.fill(
            (150, 150, 150)
        )  # This helps check if the image path is transparent
        screen.blit(map, map_rect)

        # Draw the player character
        screen.blit(player, player_rect)

        # Draw the key and door only if the key has not been found.
        if not key_found:
            screen.blit(key, key_rect)
            screen.blit(door, door_rect)

        # Write some text to the screen. You can do something like this to show some hints or whatever you want.
        label = message_font.render("By David!", True, (255, 255, 0))
        screen.blit(label, (20, 20))

        # Every time through the loop, increase the frame count.
        frame_count += 1

        # Bring drawn changes to the front
        pygame.display.update()

        # This tries to force the loop to run at 30 fps
        clock.tick(30)

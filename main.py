import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame, sys
from pygame.locals import QUIT

WIDTH, HEIGHT = 768, 432
color = (0, 0, 0)
bg_color = (135, 206, 250)
rotation_speed = 0
rotation_angle = 6.5
gravity = 1
y_velocity = 0
x_velocity = 0
y_pos = 340-30
x_pos = 0

pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(bg_color)
sprite1 = pygame.image.load("plane1.png").convert_alpha()
sprite2 = pygame.image.load("plane2.png").convert_alpha()
terrain = pygame.image.load("terrain_1.png").convert_alpha()
mouse_image = pygame.image.load("mouse.png").convert_alpha()
sprite1 = pygame.transform.smoothscale(sprite1, (939/4, 424/4))
sprite2 = pygame.transform.smoothscale(sprite2, (939/4, 424/4))
mouse_image = pygame.transform.smoothscale(mouse_image, (20, 20))

pygame.mouse.set_visible(False)

# Get masks for objects
sprite_mask = pygame.mask.from_surface(sprite1)
terrain_mask = pygame.mask.from_surface(terrain)

font = pygame.font.SysFont('corbel', 35)
current_sprite = sprite1
sprite_timer = 0  # Timer to alternate sprites
sprite_interval = 5  # Frames to wait before switching

pygame.display.set_caption('Flyby')

# Gameloop
gameloop = True
while gameloop:
    screen.fill((135, 206, 250))  # Fill screen with background color

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(terrain, (x_pos, 0))

    throttle_percent = -round(5 * sprite_interval - 25)
    text1 = font.render(f'Throttle: {throttle_percent}%', True, color)
    screen.blit(text1, (8, 8))

    # # Rotate sprite based on mouse position and speed
    rotation_speed = (pygame.mouse.get_pos()[1]/50)-(216/50)
    rotation_angle += rotation_speed
    rotated_sprite = pygame.transform.rotate(current_sprite, rotation_angle)
    rotation_angle = rotation_angle % 360
    rotated_sprite_rect = rotated_sprite.get_rect(center = (167, y_pos))

    # Alternate sprites based on the timer
    if sprite_interval >= 5:
        sprite_interval = 5
        sprite_timer = 0
       
    if sprite_interval <= -15:
        sprite_interval = -15
       
    sprite_timer += 1
    if sprite_timer >= sprite_interval:
        current_sprite = sprite2 if current_sprite == sprite1 else sprite1
        sprite_timer = 0  # Reset the timer

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE] or keys[pygame.K_q]:
        gameloop = False
   
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        sprite_interval -= 0.5
        if sprite_interval <= -15:
            sprite_interval = -15

    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        sprite_interval += 0.5
        if sprite_interval >= 5:
            sprite_interval = 5

    if keys[pygame.K_b]:
        if x_velocity > 0:
            x_velocity -= 2

        if x_velocity < 1:
            x_velocity = 0

    if terrain_mask.overlap(sprite_mask, (x_pos, y_pos - 57)):
        y_velocity = 0
        gravity = 0
    else:
        gravity = 1

    screen.blit(rotated_sprite, rotated_sprite_rect) # Draw current sprite
    mouse_pos = pygame.mouse.get_pos()
    screen.blit(mouse_image, mouse_pos)
 
    y_velocity += gravity
    y_pos += y_velocity
    x_velocity += throttle_percent/100
    x_pos -= x_velocity

# Parameters
    if x_velocity > 15:
        x_velocity = 15

    if x_velocity > 0:
        x_velocity -= 1/10
    else:
        x_velocity = 0
        
    if x_velocity < 0:
        x_velocity = 0

    print(x_velocity)

    clock.tick(30)
    pygame.display.update()

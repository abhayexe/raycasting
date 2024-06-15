import pygame
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pseudo 3D Ray Tracing")

# Define map (1 = wall, 0 = empty space)
world_map = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1]
]

# Player settings
player_x, player_y = 4, 4
player_angle = 0
player_speed = 0.05

# Ray tracing settings
FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = WIDTH // 2
MAX_DEPTH = 20
DELTA_ANGLE = FOV / NUM_RAYS
DIST = NUM_RAYS / (2 * math.tan(HALF_FOV))
PROJ_COEFF = 3 * DIST * 50
SCALE = WIDTH // NUM_RAYS

def ray_casting(screen, player_x, player_y, player_angle):
    start_angle = player_angle - HALF_FOV
    for ray in range(NUM_RAYS):
        for depth in range(MAX_DEPTH):
            target_x = player_x + depth * math.cos(start_angle)
            target_y = player_y + depth * math.sin(start_angle)
            if world_map[int(target_y)][int(target_x)] == 1:
                depth *= math.cos(player_angle - start_angle)
                wall_height = min(HEIGHT, PROJ_COEFF / (depth + 0.0001))
                color = (255 / (1 + depth * depth * 0.0001), 0, 0)
                pygame.draw.rect(screen, color, 
                    (ray * SCALE, HEIGHT // 2 - wall_height // 2, SCALE, wall_height))
                break
        start_angle += DELTA_ANGLE

def main():
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_x += player_speed * math.cos(player_angle)
            player_y += player_speed * math.sin(player_angle)
        if keys[pygame.K_s]:
            player_x -= player_speed * math.cos(player_angle)
            player_y -= player_speed * math.sin(player_angle)
        if keys[pygame.K_a]:
            player_angle -= 0.03
        if keys[pygame.K_d]:
            player_angle += 0.03

        screen.fill((0, 0, 0))
        ray_casting(screen, player_x, player_y, player_angle)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()

import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Sheepish Crossing")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (100, 100, 100)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# Sheep properties
sheep_size = 30
sheep_step = sheep_size  # Set the step size to the sheep size for grid-like movement

# Vehicle properties
vehicle_width = 60
vehicle_height = 30
vehicle_speed_base = 3
vehicle_list = []

# Game variables
level = 1
sheep_crossed = 0
total_sheep = 3  # Changed from 5 to 3
score = 0
sheep_at_top = []
game_over = False
game_completed = False

def reset_game():
    global sheep_x, sheep_y, vehicle_list, level, sheep_crossed, score, sheep_at_top, game_over, game_completed
    sheep_x = width // 2
    sheep_y = height - sheep_size - 10
    vehicle_list = []
    for i in range(4):
        vehicles_in_row = 1 + (level - 1)  # Increase vehicles per row based on level
        for j in range(vehicles_in_row):
            vehicle_x = random.randint(0, width - vehicle_width)
            vehicle_y = 100 + i * 100
            vehicle_color = random.choice([RED, BLUE, YELLOW, PURPLE])
            vehicle_list.append([vehicle_x, vehicle_y, random.choice([-1, 1]), vehicle_color])
    if level > 100:
        game_completed = True
    else:
        sheep_crossed = 0
        sheep_at_top = []
        game_over = False

def draw_text(text, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def draw_sheep(x, y):
    pygame.draw.ellipse(screen, WHITE, (x, y, sheep_size, sheep_size))
    eye_size = 4
    pygame.draw.circle(screen, BLACK, (x + sheep_size // 4, y + sheep_size // 3), eye_size)
    pygame.draw.circle(screen, BLACK, (x + 3 * sheep_size // 4, y + sheep_size // 3), eye_size)

reset_game()

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not game_over and not game_completed:
            # Move the sheep one step at a time
            if event.key == pygame.K_LEFT and sheep_x > 0:
                sheep_x -= sheep_step
            elif event.key == pygame.K_RIGHT and sheep_x < width - sheep_size:
                sheep_x += sheep_step
            elif event.key == pygame.K_UP and sheep_y > 0:
                sheep_y -= sheep_step
            elif event.key == pygame.K_DOWN and sheep_y < height - sheep_size:
                sheep_y += sheep_step

    if not game_over and not game_completed:
        # Move the vehicles
        vehicle_speed = vehicle_speed_base + (level - 1)
        for vehicle in vehicle_list:
            vehicle[0] += vehicle_speed * vehicle[2]
            if vehicle[0] > width:
                vehicle[0] = -vehicle_width
            elif vehicle[0] < -vehicle_width:
                vehicle[0] = width

        # Check for collisions
        sheep_rect = pygame.Rect(sheep_x, sheep_y, sheep_size, sheep_size)
        for vehicle in vehicle_list:
            vehicle_rect = pygame.Rect(vehicle[0], vehicle[1], vehicle_width, vehicle_height)
            if sheep_rect.colliderect(vehicle_rect):
                game_over = True

        # Check for win condition
        if sheep_y < 50:
            sheep_crossed += 1
            score += level * 100
            sheep_at_top.append(len(sheep_at_top))  # Add index instead of coordinates
            if sheep_crossed < total_sheep:
                sheep_x = width // 2
                sheep_y = height - sheep_size - 10
            else:
                level += 1
                reset_game()  # Reset the game with increased difficulty

    # Clear the screen
    screen.fill(GREEN)

    # Draw the road
    for i in range(4):
        pygame.draw.rect(screen, GRAY, (0, 100 + i * 100, width, 60))

    # Draw the sheep
    draw_sheep(sheep_x, sheep_y)

    # Draw game information
    draw_text(f"Level: {level}", 30, 50, 20)
    draw_text(f"Sheep: {len(sheep_at_top)}/{total_sheep}", 30, width - 100, 20)
    draw_text(f"Score: {score}", 30, width // 2, 20)

    # Draw the sheep that have crossed in a row
    for i, _ in enumerate(sheep_at_top):
        draw_sheep(10 + i * (sheep_size + 5), 50)

    # Draw the vehicles
    for vehicle in vehicle_list:
        pygame.draw.rect(screen, vehicle[3], (vehicle[0], vehicle[1], vehicle_width, vehicle_height))

    if game_over:
        draw_text("Game Over!", 50, width // 2, height // 2 - 50)
        draw_text(f"Final Score: {score}", 40, width // 2, height // 2 + 20)
        draw_text("Press R to Retry or Q to Quit", 30, width // 2, height // 2 + 80)
    elif game_completed:
        draw_text("No more sheeps left to cross", 50, width // 2, height // 2 - 50)
        draw_text(f"Final Score: {score}", 40, width // 2, height // 2 + 20)
        draw_text("Press Q to Quit", 30, width // 2, height // 2 + 80)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

    # Retry or quit option
    keys = pygame.key.get_pressed()
    if game_over:
        if keys[pygame.K_r]:
            level = 1
            score = 0
            reset_game()
        elif keys[pygame.K_q]:
            running = False
    elif game_completed:
        if keys[pygame.K_q]:
            running = False

# Quit the game
pygame.quit()

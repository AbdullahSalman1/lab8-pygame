from __future__ import annotations

import random

import pygame


def calculate_distance(pos1: tuple[float, float], pos2: tuple[float, float]) -> float:
    """Calculate the distance between two positions."""
    dx = pos1[0] - pos2[0]
    dy = pos1[1] - pos2[1]
    return (dx**2 + dy**2) ** 0.5
    


    


def should_flee(small_square: dict, big_square: dict, flee_radius: float) -> bool:
    """Determine if the small square should flee from the big square."""

    small_pos = (small_square["x"] + small_square["size"] / 2, small_square["y"] + small_square["size"] / 2)
    big_pos = (big_square["x"] + big_square["size"] / 2, big_square["y"] + big_square["size"] / 2)

    distance = calculate_distance(small_pos, big_pos)
    return distance < flee_radius

   

    
    
    


def flee_away(small_square: dict, big_square: dict) -> None:
    """
    Update the small square's velocity to move away from the big square.
    TODO: Change small_square's direction away from big_square.
    """
    small_pos = (small_square["x"] + small_square["size"] / 2, small_square["y"] + small_square["size"] / 2)
    big_pos = (big_square["x"] + big_square["size"] / 2, big_square["y"] + big_square["size"] / 2)

    dx = small_pos[0] - big_pos[0]
    dy = small_pos[1] - big_pos[1]

    # Normalize the direction vector
    distance = calculate_distance(small_pos, big_pos)
    if distance == 0:
        return  # Avoid division by zero

    norm_dx = dx / distance
    norm_dy = dy / distance

    # Scale by the small square's speed
    speed = ((MAX_SIZE - small_square["size"]) / (MAX_SIZE - MIN_SIZE)) * (MAX_SPEED - 1) + 1
    small_square["vx"] = norm_dx * speed
    small_square["vy"] = norm_dy * speed
    
"""Dictionary-based Pygame demo: 10 squares move randomly on a canvas.

This version uses dictionaries instead of classes/dataclasses.
"""

def is_expired(square: dict) -> bool:
    current_time = pygame.time.get_ticks()
    return current_time - square["created_at"] > SQUARE_LIFESPAN


# Window and simulation constants
WIDTH = 800
HEIGHT = 600
FPS = 100
SQUARE_COUNT = 25
MIN_SIZE = 20
MAX_SIZE = 80
MAX_SPEED = 8  # Increase max speed for small boxes
BACKGROUND_COLOR = (25, 25, 35)
SQUARE_LIFESPAN = 1000


def random_color() -> tuple[int, int, int]:
    """Return a random RGB color.

    TODO: Replace random colors with a selected color theme.
    """
    return (
        random.randint(80, 255),
        random.randint(80, 255),
        random.randint(80, 255),
    )


def create_square() -> dict:
    """Create one square as a dictionary.

    Expected keys:
    - x, y: current position
    - vx, vy: velocity
    - size: side length in pixels
    - color: RGB color tuple

    TODO: Prevent squares from spawning on top of each other.
    """
    size = random.randint(MIN_SIZE, MAX_SIZE)
    created_at = pygame.time.get_ticks()


    x = random.uniform(0, WIDTH - size)
    y = random.uniform(0, HEIGHT - size)
    # Speed inversely proportional to size (smaller = faster, bigger = slower)
    # Scale so min size gets MAX_SPEED, max size gets min speed (e.g., 1)
    speed = ((MAX_SIZE - size) / (MAX_SIZE - MIN_SIZE)) * (MAX_SPEED - 1) + 1
    vx = random.choice([-1, 1]) * speed
    vy = random.choice([-1, 1]) * speed

    return {
        "x": x,
        "y": y,
        "vx": vx,
        "vy": vy,
        "size": size,
        "color": random_color(),
        "created_at": created_at,
    }


def create_squares(count: int) -> list[dict]:
    """Create a list of square dictionaries.

    TODO: Read count from CLI arguments or keyboard input.
    """
    return [create_square() for _ in range(count)]


def update_square(square: dict) -> None:
    """Update position and bounce square on window bounds.

    TODO: Add optional random direction changes every N frames.
    """
    square["x"] += square["vx"]
    square["y"] += square["vy"]

    # Horizontal bounceclesr
    if square["x"] <= 0:
        square["x"] = 0
        square["vx"] *= -1
    elif square["x"] + square["size"] >= WIDTH:
        square["x"] = WIDTH - square["size"]
        square["vx"] *= -1

    # Vertical bounce
    if square["y"] <= 0:
        square["y"] = 0
        square["vy"] *= -1
    elif square["y"] + square["size"] >= HEIGHT:
        square["y"] = HEIGHT - square["size"]
        square["vy"] *= -1


def draw_square(screen: pygame.Surface, square: dict) -> None:
    """Draw one square dictionary.

    TODO: Draw labels or IDs on squares for debugging.
    """
    pygame.draw.rect(
        screen,
        square["color"],
        pygame.Rect(
            int(square["x"]),
            int(square["y"]),
            int(square["size"]),
            int(square["size"]),
        ),
    )


def handle_events() -> bool:
    """Handle window events. Return False when user quits.

    TODO: Add keyboard controls (pause/reset/speed changes).
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True


def run() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("10 Random Moving Squares (Dictionary Version)")
    clock = pygame.time.Clock()

    squares = create_squares(SQUARE_COUNT)

    running = True
    while running:
        running = handle_events()

       
        new_squares = []
        for square in squares:
            if not is_expired(square):
                new_squares.append(square)

       
        while len(new_squares) < SQUARE_COUNT:
            new_squares.append(create_square())

        squares = new_squares

      
        for small in squares:
            for big in squares:
                if small is big:
                    continue

                if small["size"] < big["size"]:
                    if should_flee(small, big, flee_radius=120):
                        flee_away(small, big)

    
        for square in squares:
            update_square(square)

    
        screen.fill(BACKGROUND_COLOR)
        for square in squares:
            draw_square(screen, square)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    run()

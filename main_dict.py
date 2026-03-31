"""Dictionary-based Pygame demo: 10 squares move randomly on a canvas.

This version uses dictionaries instead of classes/dataclasses.
"""

from __future__ import annotations

import random

import pygame


# Window and simulation constants
WIDTH = 800
HEIGHT = 600
FPS = 60
SQUARE_COUNT = 15
MIN_SIZE = 20
MAX_SIZE = 80
MAX_SPEED = 8  # Increase max speed for small boxes
BACKGROUND_COLOR = (25, 25, 35)


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

    # Horizontal bounce
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
    """Run the main animation loop.

    TODO: Extract game loop pieces into separate module files.
    """
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("10 Random Moving Squares (Dictionary Version)")
    clock = pygame.time.Clock()

    squares = create_squares(SQUARE_COUNT)

    running = True
    while running:
        running = handle_events()

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

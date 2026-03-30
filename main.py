"""Simple Pygame demo: 10 squares move randomly on a canvas.

This file intentionally uses a "stubs + TODO" style so it is easy to extend.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

import pygame


# Window and simulation constants
WIDTH = 800
HEIGHT = 600
FPS = 60
SQUARE_COUNT = 10
SQUARE_SIZE = 25
MAX_SPEED = 4
BACKGROUND_COLOR = (25, 25, 35)


@dataclass
class Square:
	"""Represents a moving square on the canvas."""

	x: float
	y: float
	vx: float
	vy: float
	size: int
	color: tuple[int, int, int]


def random_color() -> tuple[int, int, int]:
	"""Return a random RGB color.

	TODO: Add a palette system (e.g., pastel-only or high-contrast colors).
	"""
	return (
		random.randint(80, 255),
		random.randint(80, 255),
		random.randint(80, 255),
	)


def create_square() -> Square:
	"""Create one square with random position and velocity.

	TODO: Avoid initial overlap between squares.
	"""
	size = SQUARE_SIZE
	x = random.uniform(0, WIDTH - size)
	y = random.uniform(0, HEIGHT - size)

	# Ensure non-zero velocity to avoid static squares.
	vx = random.choice([-1, 1]) * random.uniform(1, MAX_SPEED)
	vy = random.choice([-1, 1]) * random.uniform(1, MAX_SPEED)

	return Square(x=x, y=y, vx=vx, vy=vy, size=size, color=random_color())


def create_squares(count: int) -> list[Square]:
	"""Create a list of moving squares.

	TODO: Accept parameters for count/size/speed from user input.
	"""
	return [create_square() for _ in range(count)]


def update_square(square: Square) -> None:
	"""Update position and bounce on window edges.

	TODO: Add acceleration, friction, or randomized direction changes over time.
	"""
	square.x += square.vx
	square.y += square.vy

	# Horizontal bounce
	if square.x <= 0:
		square.x = 0
		square.vx *= -1
	elif square.x + square.size >= WIDTH:
		square.x = WIDTH - square.size
		square.vx *= -1

	# Vertical bounce
	if square.y <= 0:
		square.y = 0
		square.vy *= -1
	elif square.y + square.size >= HEIGHT:
		square.y = HEIGHT - square.size
		square.vy *= -1


def draw_square(screen: pygame.Surface, square: Square) -> None:
	"""Draw a square to the screen.

	TODO: Add optional border/shadow to improve visual style.
	"""
	pygame.draw.rect(
		screen,
		square.color,
		pygame.Rect(int(square.x), int(square.y), square.size, square.size),
	)


def handle_events() -> bool:
	"""Process events. Return False to quit.

	TODO: Add controls (pause/resume, reset, speed up/down).
	"""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			return False
	return True


def run() -> None:
	"""Run the animation loop.

	TODO: Split setup and loop into separate modules for larger projects.
	"""
	pygame.init()
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption("10 Random Moving Squares")
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

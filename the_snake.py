"""Игра «Змейка» на Pygame.

Реализация классической игры «Змейка» на принципах ООП.
Змейка проходит сквозь границы поля, ест яблоки и растёт,
при самоукусе сбрасывается в начальное состояние.
"""

from random import choice, randint

import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

DIRECTIONS = (UP, DOWN, LEFT, RIGHT)

ALL_CELLS = {
    (x * GRID_SIZE, y * GRID_SIZE)
    for x in range(GRID_WIDTH)
    for y in range(GRID_HEIGHT)
}

BOARD_BACKGROUND_COLOR = (0, 0, 0)

BORDER_COLOR = (93, 216, 228)

APPLE_COLOR = (255, 0, 0)

SNAKE_COLOR = (0, 255, 0)

SPEED = 8

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pygame.display.set_caption('Змейка')

clock = pygame.time.Clock()


class GameObject:

    def __init__(self, position=CENTER, body_color=(0, 0, 0)):
        self.position = position
        self.body_color = body_color

    def draw_cell(self, position, color):
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        pass


class Apple(GameObject):

    def __init__(self, occupied=()):
        super().__init__(CENTER, APPLE_COLOR)
        self.randomize_position(occupied)

    def randomize_position(self, occupied=()):
        free_cells = tuple(ALL_CELLS - set(occupied))
        if not free_cells:
            self.position = CENTER
            return
        self.position = choice(free_cells)

    def draw(self):
        self.draw_cell(self.position, self.body_color)


class Snake(GameObject):

    def __init__(self):
        super().__init__(CENTER, SNAKE_COLOR)
        self._reset_state()

    def _reset_state(self):
        self.length = 1
        self.positions = [CENTER]
        self.direction = choice(DIRECTIONS)
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        return self.positions[0]

    def move(self):
        head = self.get_head_position()
        new_head = (
            (head[0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (head[1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT,
        )

        self.positions.insert(0, new_head)
        self.last = None

        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def reset(self):
        self._reset_state()

    def draw(self):
        if self.last:
            self.draw_cell(self.last, BOARD_BACKGROUND_COLOR)

        for position in self.positions:
            self.draw_cell(position, self.body_color)


def handle_keys(game_object):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit
            elif event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    pygame.init()

    snake = Snake()
    apple = Apple(occupied=snake.positions)

    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(occupied=snake.positions)

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position(occupied=snake.positions)

        apple.draw()
        snake.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
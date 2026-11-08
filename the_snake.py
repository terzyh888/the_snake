from random import choice
import pygame

# Инициализация PyGame:
pygame.init()

# Константы размеров и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -GRID_SIZE)
DOWN = (0, GRID_SIZE)
LEFT = (-GRID_SIZE, 0)
RIGHT = (GRID_SIZE, 0)

# Цвета:
BOARD_BACKGROUND_COLOR = (0, 0, 0)  # Черный (фон)
APPLE_COLOR = (255, 0, 0)          # Красный (яблоко)
SNAKE_COLOR = (0, 255, 0)          # Зеленый (змейка)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')

# Настройка часов:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, body_color=None):
        """Инициализирует базовые атрибуты объекта."""
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = body_color

    def draw(self, surface):
        """Абстрактный метод для отрисовки объекта на поверхности."""
        pass

    def draw_cell(self, surface, position, color):
        """Вспомогательный метод для отрисовки одной ячейки (квадрата)."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, color, rect)
        pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, rect, 1)


class Apple(GameObject):
    """Класс, описывающий яблоко и действия с ним."""

    def __init__(self, occupied_cells=None):
        """Инициализирует яблоко, задавая ему цвет и случайную позицию."""
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position(occupied_cells if occupied_cells else [])

    def randomize_position(self, occupied_cells):
        """Устанавливает случайное положение яблока, избегая занятых клеток."""
        all_cells = [
            (x * GRID_SIZE, y * GRID_SIZE)
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
        ]
        free_cells = [cell for cell in all_cells if cell not in occupied_cells]
        if free_cells:
            self.position = choice(free_cells)
        else:
            self.position = (0, 0)

    def draw(self, surface):
        """Отрисовывает яблоко на игровой поверхности."""
        self.draw_cell(surface, self.position, self.body_color)


class Snake(GameObject):
    """Класс, описывающий змейку и её поведение."""

    def __init__(self):
        """Инициализирует начальное состояние змейки."""
        super().__init__(body_color=SNAKE_COLOR)
        self.reset()

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки на один шаг."""
        head_x, head_y = self.get_head_position()
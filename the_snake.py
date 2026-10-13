"""Игра «Змейка» на библиотеке Pygame."""

import random

import pygame as pg

# Константы игрового поля.
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Цвета.
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки.
SPEED = 10

# Направления движения.
UP = pg.math.Vector2(0, -1)
DOWN = pg.math.Vector2(0, 1)
LEFT = pg.math.Vector2(-1, 0)
RIGHT = pg.math.Vector2(1, 0)

DIRECTION_BY_KEY = {
    ((-1, 0), pg.K_UP): UP,
    ((1, 0), pg.K_UP): UP,
    ((-1, 0), pg.K_DOWN): DOWN,
    ((1, 0), pg.K_DOWN): DOWN,
    ((0, -1), pg.K_LEFT): LEFT,
    ((0, 1), pg.K_LEFT): LEFT,
    ((0, -1), pg.K_RIGHT): RIGHT,
    ((0, 1), pg.K_RIGHT): RIGHT,
}

# Игровое окно и часы доступны на уровне модуля.
pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pg.time.Clock()


class GameObject:
    """Базовый класс игровых объектов."""

    def __init__(self, body_color=SNAKE_COLOR):
        """Инициализирует игровой объект."""
        self.position = (
            SCREEN_WIDTH // 2 // GRID_SIZE * GRID_SIZE,
            SCREEN_HEIGHT // 2 // GRID_SIZE * GRID_SIZE,
        )
        self.body_color = body_color

    def draw_cell(self, position, color, draw_border=True):
        """Отрисовывает одну клетку игрового поля."""
        rectangle = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rectangle)
        if draw_border:
            pg.draw.rect(screen, BORDER_COLOR, rectangle, 1)

    def draw(self):
        """Отрисовывает игровой объект."""
        raise NotImplementedError(
            'В дочернем классе нужно определить draw().',
        )


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self, occupied_positions=None):
        """Создаёт яблоко вне занятых клеток."""
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position(occupied_positions or [])

    def randomize_position(self, occupied_positions):
        """Выбирает случайную свободную позицию."""
        available_positions = [
            (x * GRID_SIZE, y * GRID_SIZE)
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
            if (x * GRID_SIZE, y * GRID_SIZE)
            not in occupied_positions
        ]
        if available_positions:
            self.position = random.choice(available_positions)

    def draw(self):
        """Отрисовывает яблоко."""
        self.draw_cell(self.position, self.body_color)


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self):
        """Создаёт змейку и задаёт начальное состояние."""
        super().__init__(body_color=SNAKE_COLOR)
        self.reset()
        self.direction = RIGHT

    def update_direction(self):
        """Применяет новое направление движения."""
        if self.next_direction is not None:
            if self.next_direction != -self.direction:
                self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Перемещает змейку на одну клетку."""
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction
        self.position = (
            int((head_x + direction_x * GRID_SIZE) % SCREEN_WIDTH),
            int((head_y + direction_y * GRID_SIZE) % SCREEN_HEIGHT),
        )
        self.positions.insert(0, self.position)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Отрисовывает змейку и стирает последний сегмент."""
        if self.last:
            self.draw_cell(
                self.last,
                BOARD_BACKGROUND_COLOR,
                draw_border=False,
            )
        for position in self.positions:
            self.draw_cell(position, self.body_color)

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает состояние змейки."""
        self.length = 1
        self.positions = [self.position]
        self.direction = random.choice((UP, DOWN, LEFT, RIGHT))
        self.next_direction = None
        self.last = None


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш и закрытие окна."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit

        if event.type == pg.KEYDOWN:
            new_direction = DIRECTION_BY_KEY.get(
                (tuple(game_object.direction), event.key),
            )
            if new_direction is not None:
                game_object.next_direction = new_direction


def main():
    """Запускает основной игровой цикл."""
    pg.display.set_caption('Змейка')
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        elif snake.get_head_position() in snake.positions[1:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
            apple.randomize_position(snake.positions)

        snake.draw()
        apple.draw()
        pg.display.update()


if __name__ == '__main__':
    main()

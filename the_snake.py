from random import randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета:
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
WHITE_COLOR = (255, 255, 255)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('Змейка')
clock = pg.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов с позицией и цветом."""

    def __init__(self, body_color=WHITE_COLOR):
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = body_color

    def draw(self):
        """Отрисовывает объект на экране."""
        pass


class Apple(GameObject):
    """Класс для создания яблока на игровом поле."""

    def __init__(self, body_color=APPLE_COLOR, occupied_positions=[]):
        super().__init__(body_color)
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions=[]):
        """
        Устанавливает яблоко в случайную позицию,
        не совпадающую с занятыми.
        """
        while True:
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if self.position not in occupied_positions:
                break

    def draw(self):
        """Отрисовывает яблоко на игровом поле."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для управления змейкой."""

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(body_color)
        self.reset()

    def reset(self):
        """Сбрасывает состояние змейки до начального."""
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.grew = False

    def update_direction(self, new_direction):
        """Обновляет направление движения змейки, избегая движения назад."""
        if new_direction and (new_direction[0] * -1,
                              new_direction[1] * -1) != self.direction:
            self.direction = new_direction

    def move(self):
        """
        Перемещает змейку, добавляя новый сегмент головы и удаляя хвост,
        если змейка не растёт.
        """
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_x = (head_x + dx * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        new_head_position = (new_x, new_y)

        # Проверяем столкновение с собой
        if new_head_position in self.positions[1:]:
            self.reset()
        else:
            self.positions.insert(0, new_head_position)
            if not self.grew:
                self.positions.pop()
            self.grew = False

    def grow(self):
        """Увеличивает длину змейки после поедания яблока."""
        self.grew = True

    def draw(self):
        """Отрисовывает змейку на игровом поле."""
        for position in self.positions:
            rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def get_head_position(self):
        """Возвращает текущую позицию головы змейки."""
        return self.positions[0]


def handle_keys(snake):
    """Обрабатывает нажатия клавиш для управления змейкой."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                snake.update_direction(UP)
            elif event.key == pg.K_DOWN:
                snake.update_direction(DOWN)
            elif event.key == pg.K_LEFT:
                snake.update_direction(LEFT)
            elif event.key == pg.K_RIGHT:
                snake.update_direction(RIGHT)


def main():
    """Основной игровой цикл."""
    snake = Snake()
    apple = Apple(occupied_positions=snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)

        # Перемещение змейки
        snake.move()

        # Проверка на поедание яблока
        if snake.get_head_position() == apple.position:
            snake.grow()
            apple.randomize_position(occupied_positions=snake.positions)

        # Очистка экрана, отрисовка объектов и обновление экрана
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()

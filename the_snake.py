import pygame
from random import randint

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

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов с позицией и цветом."""

    def __init__(self):
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = None

    def draw(self):
        """Абстрактный метод для отрисовки объекта на экране."""
        pass


class Apple(GameObject):
    """Класс для создания яблока на игровом поле."""

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает яблоко в случайную позицию на игровом поле."""
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self):
        """Отрисовывает яблоко на игровом поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для управления змейкой."""

    def __init__(self):
        super().__init__()
        self.body_color = SNAKE_COLOR
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
        """Перемещает змейку, добавляя новый сегмент головы и удаляя хвост,
        если змейка не растёт."""
        head_x, head_y = self.positions[0]
        new_x = (head_x + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        new_head_position = (new_x, new_y)

        # Проверяем столкновение с собой
        if new_head_position in self.positions[1:]:
            self.reset()
        else:
            self.positions.insert(0, new_head_position)

            # Проверка на рост змейки
            if not self.grew:
                self.positions.pop()
            self.grew = False

    def grow(self):
        """Увеличивает длину змейки после поедания яблока."""
        self.grew = True

    def draw(self):
        """Отрисовывает змейку на игровом поле."""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def reset(self):
        """Сбрасывает состояние змейки до начального."""
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.grew = False

    def get_head_position(self):
        """Возвращает текущую позицию головы змейки."""
        return self.positions[0]


def handle_keys(snake):
    """Обрабатывает нажатия клавиш для управления змейкой."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """Основной игровой цикл."""
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)

        # Обновление направления и перемещение змейки
        if snake.next_direction:
            snake.update_direction(snake.next_direction)
            snake.next_direction = None
        snake.move()

        # Проверка на поедание яблока
        if snake.positions[0] == apple.position:
            snake.grow()
            apple.randomize_position()

        # Очистка экрана, отрисовка объектов и обновление экрана
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()

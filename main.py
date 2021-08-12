import random
import time
import pygame
from pygame.locals import KEYDOWN, K_ESCAPE, QUIT, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_RETURN


SIZE = 40
BACKGROUND_COLOR = (110, 110, 5)


class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.fruit = pygame.image.load("resources/apple.jpg").convert()
        self.x = SIZE * random.randint(2, 15)
        self.y = SIZE * random.randint(2, 15)

    def draw(self):
        self.parent_screen.blit(self.fruit, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1, 19) * SIZE
        self.y = random.randint(1, 14) * SIZE


class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.x = [SIZE] * length
        self.y = [SIZE] * length
        self.direction = "down"

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def move_up(self):
        self.direction = "up"

    def move_down(self):
        self.direction = "down"

    def move_left(self):
        self.direction = "left"

    def move_right(self):
        self.direction = "right"

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == "up":
            self.y[0] -= SIZE
        if self.direction == "down":
            self.y[0] += SIZE
        if self.direction == "left":
            self.x[0] -= SIZE
        if self.direction == "right":
            self.x[0] += SIZE

        self.draw()


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        # self.play_background_music()
        self.surface = pygame.display.set_mode((1200, 600))
        self.surface.fill((23, 173, 63))
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.fruit = Apple(self.surface)
        self.fruit.draw()

    @staticmethod
    def is_collision(x1, y1, x2, y2):
        if x2 <= x1 < (x2 + SIZE) and y2 <= y1 < (y2 + SIZE):
            return True
        else:
            return False

    @staticmethod
    def play_background_music():
        pygame.mixer.music.load("resources/bg_music.mp3")
        pygame.mixer.music.play()

    @staticmethod
    def play_sound(sound):
        pygame.mixer.Sound.play(pygame.mixer.Sound(f"resources/{sound}.mp3"))

    def render_background(self):
        background = pygame.image.load("resources/background.jpg")
        self.surface.blit(background, (0, 0))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.fruit.draw()
        self.display_score()
        pygame.display.flip()

        # Snake colliding with an apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.fruit.x, self.fruit.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.fruit.move()

        # Snake colliding with itself
        for i in range(1, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("crash")
                raise "Game Over"

        # Snake colliding with the boundaries of the window
        if not (0 <= self.snake.x[0] <= 1180 and 0 <= self.snake.y[0] <= 580):
            self.play_sound("crash")
            raise "Hit the boundary!"

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont("arial", 30)
        line1 = font.render(f"Game over! Your score: {self.snake.length}.", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("To play again press Enter. To quit press Escape.", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.display.flip()
        pygame.mixer.music.pause()

    def display_score(self):
        font = pygame.font.SysFont("arial", 30)
        score = font.render(f"Score: {self.snake.length}", True, (200, 200, 200))
        self.surface.blit(score, (10, 10))

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.fruit = Apple(self.surface)

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(0.15)


if __name__ == "__main__":
    game = Game()
    game.run()

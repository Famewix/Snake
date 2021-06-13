import pygame
import sys
import os
import random
from pygame.math import Vector2
from time import sleep

pygame.init()
cellSize = 20
cellNumber = 40
screenColor = (88,88,88) # black
fruitColor = (255, 255, 255) # lineColor
snakeColor = (0,0,0) # green
lineColor = (88, 88, 88) # gray
FPS = 60

os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Fruit:
    def __init__(self):
        self.randomize()

    def randomize(self):
        self.x = random.randint(0, cellNumber - 1)
        self.y = random.randint(0, cellNumber - 1)
        self.pos = Vector2(self.x, self.y)

    def draw_fruit(self):
        fruit_rect = pygame.Rect(
            self.pos.x * cellSize,
            self.pos.y * cellSize, 
            cellSize , cellSize
        )
        pygame.draw.rect(screen, fruitColor, fruit_rect)


class Snake:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False

    def draw_snake(self):
        for snake_block in self.body:
            block_rect = pygame.Rect(
                snake_block.x * cellSize, 
                snake_block.y * cellSize, 
                cellSize, cellSize
            )
            pygame.draw.rect(screen, snakeColor, block_rect)
    
    def movement(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        eat_sound.play()
        self.new_block = True


class MainGame:
    def __init__(self):
        self.fruit = Fruit()
        self.snake = Snake()
        self.score = 0

    def update(self):
        self.snake.movement()
        self.check_collision()
        self.check_fails_tel()

    def draw_objects(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.show_score()

    def show_score(self):
        score_surf = game_font.render(f"Score: {str(self.score)}", True, fruitColor)
        score_rect = score_surf.get_rect(center=((cellNumber * cellSize)/5, (cellNumber * cellSize) - 50))
        screen.blit(score_surf, score_rect)

    def grid_lines(self):
        y_grid_pos = cellSize
        x_grid_pos = cellSize
        for i in range(cellNumber):
            pygame.draw.aaline(screen, lineColor, (y_grid_pos, 0), (y_grid_pos, cellNumber * cellSize))
            pygame.draw.aaline(screen, lineColor, (0, x_grid_pos), (cellNumber * cellSize, x_grid_pos))
            y_grid_pos += cellSize
            x_grid_pos += cellSize

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.score += 1
            

    def check_fails_tel(self):
        if not 0 <= self.snake.body[0].x < cellNumber:
            self.teleport_x()
        elif not 0 < self.snake.body[0].y < cellNumber:
            self.teleport_y()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                die_sound.play()
                sleep(0.5)
                self.game_over()

    def game_over(self):
        pygame.quit()
        sys.exit()

    def teleport_x(self):
        for block in self.snake.body[:]:
            if block.x > cellNumber:
                block.x = 0
            elif block.x < 0:
                block.x = cellNumber

    def teleport_y(self):
        for block in self.snake.body[:]:
            if block.y > cellNumber:
                block.y = 0
            elif block.y < 0:
                block.y = cellNumber

screen = pygame.display.set_mode((cellSize * cellNumber, cellSize * cellNumber))
pygame.display.set_caption('Minimal Snake')
clock = pygame.time.Clock()
game_font = pygame.font.Font('font\\ARLRDBD.ttf', 20)
eat_sound = pygame.mixer.Sound('sounds\\eat.wav')
die_sound = pygame.mixer.Sound('sounds\\die.wav')
main_game = MainGame()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_a:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_s:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_d:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)

    screen.fill(screenColor)
    main_game.draw_objects()
    # main_game.grid_lines()
    pygame.display.update()
    clock.tick(FPS)

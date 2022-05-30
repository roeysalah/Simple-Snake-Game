import collections

import pygame
import random
from enum import Enum
pygame.init()

class SnakeDirection(Enum):
    UP = 4
    DOWN = 3
    LEFT = 2
    RIGHT = 1



Pt = collections.namedtuple('Pt',['x','y'])

SIZE = 20
FONT = pygame.font.SysFont('Arial', SIZE)



class Snake:

    def __init__(self,width=640,height=480):
        self.width = width
        self.height = height
        self.display_screen = pygame.display.set_mode((self.width,self.height))
        pygame.display.set_caption("Snake") # Set the title of the game
        self.clock = pygame.time.Clock() # Used to control the speed of the game

        #init game state variables - snake and food
        self.direction = SnakeDirection.RIGHT
        self.SnakeHead = Pt(x = self.width / 2, y = self.height / 2)
        self.SnakeCurr = [self.SnakeHead,
                          Pt(self.SnakeHead.x - SIZE, self.SnakeHead.y),
                          Pt(self.SnakeHead.x - (2 * SIZE), self.SnakeHead.y)]
        self.__SnakeSpeed = 5
        self.score = 0
        self.food = None
        self._generate_food()

    def __set(self,speed):
        self.__SnakeSpeed = speed

    def _generate_food(self):
        x = random.randint(0, (self.width - SIZE) // SIZE) * SIZE
        y = random.randint(0, (self.height - SIZE) // SIZE) * SIZE
        self.food = Pt(x, y)
        if self.food in self.SnakeCurr:
            self._generate_food()

    def play(self):
        """
        In this function we play the game
        :return:
        """
        #1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.direction = SnakeDirection.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = SnakeDirection.DOWN
                elif event.key == pygame.K_LEFT:
                    self.direction = SnakeDirection.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = SnakeDirection.RIGHT


        self._move(self.direction) # update snake move in the direction
        self.SnakeCurr.insert(0, self.SnakeHead) # add a new head to the snake

        game_over = False
        if self._check_collision(): # check if snake collide with boundry/itself
            game_over = True
            return game_over , self.score

        if self.SnakeHead == self.food:
            self.score += 1
            acclerate = self.__SnakeSpeed + 1
            self.__set(acclerate)
            self.clock.tick(acclerate)
            self._generate_food()
        else:
            self.SnakeCurr.pop()
            self.clock.tick(self.__SnakeSpeed)
        #update snake
        self._update_snake()
        # return game over and score
        return (game_over,self.score)

    def _update_snake(self):
        """
        This function update the snake
        :return:
        """
        self.display_screen.fill((0,0,0)) # fill the screen with black
        for p in self.SnakeCurr:
            pygame.draw.rect(self.display_screen,(0,0,255),(p.x,p.y,SIZE,SIZE))
            pygame.draw.rect(self.display_screen,(0,100,255),(p.x+4,p.y+4,12,12))

        pygame.draw.rect(self.display_screen,(255,0,0),(self.food.x,self.food.y,SIZE,SIZE))




        text = FONT.render("Score: " + str(self.score),True,(255,255,255))
        self.display_screen.blit(text,[0,0])
        pygame.display.flip() # update the screen

    def _move(self,direction):
        """
        This function move the snake in the direction
        :param direction:
        :return:
        """
        x = self.SnakeHead.x
        y = self.SnakeHead.y
        if direction == SnakeDirection.UP:
            y -= SIZE
        elif direction == SnakeDirection.DOWN:
            y += SIZE
        elif direction == SnakeDirection.LEFT:
            x -= SIZE
        elif direction == SnakeDirection.RIGHT:
            x += SIZE

        self.SnakeHead = Pt(x, y) # update the head of the snake with new head position

    def _check_collision(self):
        """
        check if snake collide with boundry
        :return:
        """
        if self.SnakeHead.x < 0 or self.SnakeHead.x > self.width - SIZE:
            return True
        elif self.SnakeHead.y < 0 or self.SnakeHead.y > self.height - SIZE:
            return True
        elif self.SnakeCurr[0] in self.SnakeCurr[1:]: # check if snake collide with itself
            return True
        return False


if __name__ == '__main__':
    game = Snake()
    while True:
        game_over, score = game.play()
        if game_over == True:
            break

    pygame.display.set_caption("Snake")
    text = FONT.render("Your Score is : {}".format(score),True, (255, 0, 0),(0,0,255))
    pygame.display.set_mode((640,480))
    game.display_screen.blit(text,[300,200])
    pygame.display.flip()  # update the screen
    pygame.time.wait(1000)
    pygame.quit()

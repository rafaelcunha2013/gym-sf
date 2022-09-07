"""
Render a gridworld environment using the pygame library
"""

import pygame
import numpy as np
from four_room import FourRoom


class Render:
    # Define some colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)

    def __init__(self, maze):
        # Environment that will be showed
        self.maze_height, self.maze_width = maze.shape
        self.maze = maze

        # Square dimensions
        self.WIDTH = 20
        self.HEIGHT = 20
        self.MARGIN = 1
        self.number_of_squares = self.maze_height

        # Set the width and height of the screen [width, height]
        grid_length = self.number_of_squares * (self.WIDTH + self.MARGIN) + self.MARGIN
        self.size = (grid_length, grid_length)
        self.screen = pygame.display.set_mode(self.size)
        self.agent_state = None
        self.initialize()
        pygame.time.delay(200)

    def update(self, state):
        if isinstance(state[0], tuple):
            for single_state in self.agent_state:
                r, c = single_state
                color = Render.YELLOW
                self.draw_shape(r, c, color, 'rect')
            for single_state in state:
                r, c = single_state
                color = Render.BLUE
                self.draw_shape(r, c, color, 'circle')
            self.agent_state = state
        else:
            r, c = self.agent_state[0]
            color = Render.YELLOW
            self.draw_shape(r, c, color, 'rect')
            r, c = state
            color = Render.BLUE
            self.draw_shape(r, c, color, 'circle')

            self.agent_state = [state]

        pygame.display.flip()
        pygame.time.delay(20)

    def initialize(self):
        # Agent state
        self.agent_state = []

        pygame.init()
        # self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("GridWorld")

        # Used to manage how fast the screen updates
        clock = pygame.time.Clock()

        # background image.
        self.screen.fill(Render.BLACK)

        # --- Drawing code should go here
        # color = Render.GREEN
        for r in range(self.maze_height):
            for c in range(self.maze_width):
                color = Render.WHITE
                self.draw_shape(r, c, color, 'rect')

        for c in range(self.maze_width):
            for r in range(self.maze_height):
                if self.maze[r, c] == 'G':
                    color = Render.GREEN
                    self.draw_shape(r, c, color, 'circle')
                elif self.maze[r, c] == ' ':
                    color = Render.WHITE
                    self.draw_shape(r, c, color, 'rect')
                elif self.maze[r, c] == '_':
                    self.agent_state.append((r, c))
                    color = Render.BLUE
                    self.draw_shape(r, c, color, 'circle')
                elif self.maze[r, c] == 'X':
                    color = Render.BLACK
                    self.draw_shape(r, c, color, 'rect')
                elif self.maze[r, c] in {'3'}:
                    color = Render.GREEN
                    self.draw_shape(r, c, color, 'tri')
                elif self.maze[r, c] in {'2'}:
                    color = Render.RED
                    self.draw_shape(r, c, color, 'tri')
                elif self.maze[r, c] in {'1'}:
                    color = Render.BLUE
                    self.draw_shape(r, c, color, 'tri')

        pygame.display.flip()

        # --- Limit to 60 frames per second
        clock.tick(60)

        # Close the window and quit.
        # pygame.quit()

    def draw_shape(self, r, c, color, shape):
        if shape == 'rect':
            pygame.draw.rect(self.screen,
                             color,
                             [(self.MARGIN + self.WIDTH) * c + self.MARGIN,
                              (self.MARGIN + self.HEIGHT) * r + self.MARGIN,
                              self.WIDTH,
                              self.HEIGHT])
        elif shape == 'circle':
            pygame.draw.circle(self.screen,
                               color,
                               [(self.MARGIN + self.WIDTH) * c + self.MARGIN + self.WIDTH / 2,
                                (self.MARGIN + self.HEIGHT) * r + self.MARGIN + self.HEIGHT / 2],
                               10)
        elif shape == 'tri':
            pygame.draw.polygon(self.screen,
                                color,
                                [[(self.MARGIN + self.WIDTH) * c + self.MARGIN + self.WIDTH / 2,
                                  (self.MARGIN + self.HEIGHT) * r + self.MARGIN],
                                 [(self.MARGIN + self.WIDTH) * c + self.MARGIN,
                                  (self.MARGIN + self.HEIGHT) * r + self.MARGIN + self.HEIGHT - 0.1],
                                 [(self.MARGIN + self.WIDTH) * c + self.MARGIN + self.WIDTH,
                                  (self.MARGIN + self.HEIGHT) * r + self.MARGIN + self.HEIGHT - 0.1]])


if __name__ == "__main__":

    maze = [
        ['1', ' ', ' ', ' ', ' ', '2', 'X', ' ', ' ', ' ', ' ', ' ', 'G'],
        [' ', ' ', ' ', ' ', ' ', ' ', 'X', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', '1', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', 'X', ' ', ' ', ' ', ' ', ' ', ' '],
        ['2', ' ', ' ', ' ', ' ', '3', 'X', ' ', ' ', ' ', ' ', ' ', ' '],
        ['X', 'X', '3', ' ', 'X', 'X', 'X', 'X', 'X', ' ', '1', 'X', 'X'],
        [' ', ' ', ' ', ' ', ' ', ' ', 'X', '2', ' ', ' ', ' ', ' ', '3'],
        [' ', ' ', ' ', ' ', ' ', ' ', 'X', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', '2', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', 'X', ' ', ' ', ' ', ' ', ' ', ' '],
        ['_', ' ', ' ', ' ', ' ', ' ', 'X', '3', ' ', ' ', ' ', ' ', '1']]
    maze = np.array(maze)

    rewards = dict(zip(['1', '2', '3'], list(np.random.uniform(low=-1.0, high=1.0, size=3))))
    gridworld = FourRoom(maze=maze, shape_rewards=rewards)

    s0 = gridworld.initialize()
    my_grid = Render(maze=gridworld.env_maze)

    for _ in range(1000):

        action = np.random.randint(0, 4)
        if np.random.random() < 0.20:
            if np.random.random() < 0.50:
                action = 2
            else:
                action = 1
        next_state, reward, done = gridworld.transition(action)

        my_grid.update(next_state[0])
        if done:
            gridworld = FourRoom(maze=maze, shape_rewards=rewards)
            s0 = gridworld.initialize()
            my_grid = Render(maze=gridworld.env_maze)

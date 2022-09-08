"""
Render a gridworld environment using the pygame library
"""

import pygame
import numpy as np
from gym.utils.renderer import Renderer


class Render:
    # Define some colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)

    def __init__(self, maze, render_mode='human'):
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
        self.screen = None

        # if self.render_mode == 'human':
        #     import pygame
        #     self.screen = pygame.display.set_mode(self.size)
        self.agent_state = None
        self.render_mode = render_mode
        # self.clock = None
        # self.renderer = None
        # Agent state
        self.agent_state = []
        if self.render_mode == 'human':
            # import pygame
            pygame.init()
            pygame.display.init()
            self.screen = pygame.display.set_mode(self.size)
            self.clock = pygame.time.Clock()

        # self.renderer = Renderer(self.render_mode, self._render_frame)
        # self.initialize()
        # pygame.time.delay(200)

    def update(self, state, mode='human'):
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

        if mode == 'human':
            pygame.display.flip()
            pygame.time.delay(20)

    # def initialize(self):
    #     # Agent state
    #     self.agent_state = []
    #     if self.render_mode == 'human':
    #         # import pygame
    #         pygame.init()
    #         pygame.display.init()
    #         self.screen = pygame.display.set_mode(self.size)
    #         self.clock = pygame.time.Clock()
    #
    #     self.renderer = Renderer(self.render_mode, self._render_frame)

        # self.screen = pygame.display.set_mode(self.size)
        # pygame.display.set_caption("GridWorld")

        # Used to manage how fast the screen updates
        # clock = pygame.time.Clock()

    def render_frame(self, mode='human'):
        # This will be the function called by the Renderer to collect a single frame.
        assert mode is not None  # The renderer will not call this function with no-rendering.

        # import pygame  # avoid global pygame dependency. This method is not called with no-render.

        # background image.
        self.canvas = pygame.Surface(self.size)
        self.canvas.fill(Render.BLACK)
        # self.screen.fill(Render.BLACK)

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

        # --- Update the content of the entire display
        # pygame.display.flip()

        # --- Limit to 60 frames per second
        # clock.tick(60)

        # Close the window and quit.
        # pygame.quit()


        if mode == "human":
            assert self.screen is not None
            # The following line copies our drawings from `canvas` to the visible window
            self.screen.blit(self.canvas, self.canvas.get_rect())
            pygame.event.pump()
            pygame.display.update()

            # We need to ensure that human-rendering occurs at the predefined framerate.
            # The following line will automatically add a delay to keep the framerate stable.
            self.clock.tick(self.maze.metadata["render_fps"])
        else:  # rgb_array or single_rgb_array
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(self.canvas)), axes=(1, 0, 2)
            )

    def draw_shape(self, r, c, color, shape):
        if shape == 'rect':
            pygame.draw.rect(self.canvas,
                             color,
                             [(self.MARGIN + self.WIDTH) * c + self.MARGIN,
                              (self.MARGIN + self.HEIGHT) * r + self.MARGIN,
                              self.WIDTH,
                              self.HEIGHT])
        elif shape == 'circle':
            pygame.draw.circle(self.canvas,
                               color,
                               [(self.MARGIN + self.WIDTH) * c + self.MARGIN + self.WIDTH / 2,
                                (self.MARGIN + self.HEIGHT) * r + self.MARGIN + self.HEIGHT / 2],
                               10)
        elif shape == 'tri':
            pygame.draw.polygon(self.canvas,
                                color,
                                [[(self.MARGIN + self.WIDTH) * c + self.MARGIN + self.WIDTH / 2,
                                  (self.MARGIN + self.HEIGHT) * r + self.MARGIN],
                                 [(self.MARGIN + self.WIDTH) * c + self.MARGIN,
                                  (self.MARGIN + self.HEIGHT) * r + self.MARGIN + self.HEIGHT - 0.1],
                                 [(self.MARGIN + self.WIDTH) * c + self.MARGIN + self.WIDTH,
                                  (self.MARGIN + self.HEIGHT) * r + self.MARGIN + self.HEIGHT - 0.1]])


if __name__ == "__main__":
    from four_room import FourRoom

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

    gridworld.reset()
    my_grid = Render(maze=gridworld.env_maze)

    for _ in range(1000):

        action = np.random.randint(0, 4)
        if np.random.random() < 0.20:
            if np.random.random() < 0.50:
                action = 2
            else:
                action = 1
        next_state, reward, done = gridworld.step(action)

        my_grid.update(next_state[0])
        if done:
            gridworld = FourRoom(maze=maze, shape_rewards=rewards)
            gridworld.reset()
            my_grid = Render(maze=gridworld.env_maze)

"""
Render a gridworld environment using the pygame library
"""
import copy

import pygame
import numpy as np


class Render:
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 20}
    # Define some colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (0, 255, 0) # GREEN = (0, 255, 0)
    GREEN = (255, 0, 0) # RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)

    def __init__(self, maze, render_mode='rgb_array'):
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

        self.agent_state = None
        self.render_mode = render_mode

        # Agent state
        self.agent_state = []
        self.canvas = pygame.Surface(self.size)
        mode = self.check_display(render_mode)
        if self.render_mode == 'human':
            pygame.init()
            pygame.display.init()
            pygame.display.set_caption("Four-Room")
            self.screen = pygame.display.set_mode(self.size)
            self.clock = pygame.time.Clock()

    def update(self, state, mode='human'):
        # print(state)
        # print(self.agent_state)
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

        mode = self.check_display(mode)
        if mode == 'human':
            self.screen.blit(self.canvas, self.canvas.get_rect())
            pygame.event.pump()
            pygame.display.update()
            self.clock.tick(self.metadata["render_fps"])
        else:  # rgb_array or single_rgb_array
            frame = np.transpose(np.array(pygame.surfarray.pixels3d(self.canvas)), axes=(1, 0, 2))
            frame = np.roll(frame[:, :], 1)
            return frame

    def render_frame(self, mode='human', agent='unique'):
        if agent != 'unique':
            self.agent_state = copy.deepcopy(agent)
        # This will be the function called by the Renderer to collect a single frame.
        assert mode is not None  # The renderer will not call this function with no-rendering.

        self.canvas.fill(Render.BLACK)

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
                    if agent == 'unique':
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

        mode = self.check_display(mode)
        if mode == "human":
            assert self.screen is not None
            # The following line copies our drawings from `canvas` to the visible window
            self.screen.blit(self.canvas, self.canvas.get_rect())
            pygame.event.pump()
            pygame.display.update()

            # We need to ensure that human-rendering occurs at the predefined framerate.
            # The following line will automatically add a delay to keep the framerate stable.
            self.clock.tick(self.metadata["render_fps"])
        else:  # rgb_array or single_rgb_array
            frame = np.transpose(np.array(pygame.surfarray.pixels3d(self.canvas)), axes=(1, 0, 2))
            frame = np.roll(frame[:, :], 1)
            return frame

    def check_display(self, mode):
        if self.render_mode == 'human' or mode == 'human':
            try:
                pygame.display.init()
            except pygame.error:
                self.render_mode = 'rgb_array'
                mode = 'rgb_array'
        
        return mode

# continue with your program logic here



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

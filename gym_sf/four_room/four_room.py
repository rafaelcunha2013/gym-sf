# -*- coding: UTF-8 -*-
import gym
from gym import spaces
from gym.utils.renderer import Renderer

from gym_sf.four_room.render import Render
from gym_sf.four_room.utilities import frame_to_video
import numpy as np
import random
import copy

MAZE = np.array([
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
    ['_', ' ', ' ', ' ', ' ', ' ', 'X', '3', ' ', ' ', ' ', ' ', '1']])
REWARDS = dict(zip(['1', '2', '3'], list([1.0, 0.5, -1.0])))


class FourRoom(gym.Env):

    """
    A discretized version of the gridworld environment introduced in [1]. Here, an agent learns to
    collect shapes with positive reward, while avoid those with negative reward, and then travel to a fixed goal.
    The gridworld is split into four rooms separated by walls with passage-ways.

    # Code adapted from: https://github.com/mike-gimelfarb/deep-successor-features-for-transfer/blob/main/source/tasks/gridworld.py

    In this version, a render is implemented and the agent can start at random locations.

    References
    ----------
    [1] Barreto, Andr�, et al. "Successor Features for Transfer in Reinforcement Learning." NIPS. 2017.
    """

    LEFT, UP, RIGHT, DOWN = 0, 1, 2, 3

    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self, maze=MAZE, shape_rewards=REWARDS,
                 render_mode='human', random_initial_position=True, video=False):
        """
        Creates a new instance of the FourRoom environment.

        Parameters
        ----------
        maze : np.ndarray
            an array of string values representing the type of each cell in the environment:
                G indicates a goal state (terminal state)
                _ indicates an initial state (there can be multiple, and one is selected at random
                    at the start of each episode)
                X indicates a barrier
                0, 1, .... 9 indicates the type of shape to be placed in the corresponding cell
                entries containing other characters are treated as regular empty cells
        shape_rewards : dict
            a dictionary mapping the type of shape (0, 1, ... ) to a corresponding reward to provide
            to the agent for collecting an object of that type
        """
        self.max_num_agents = 1
        self.random_initial_position = random_initial_position
        self.step_count = None
        self.terminated = None
        self.truncated = None

        self.height, self.width = maze.shape
        self.maze = maze
        self.env_maze = copy.deepcopy(self.maze)
        self.my_render = None
        self.shape_rewards = shape_rewards
        shape_types = sorted(list(shape_rewards.keys()))
        self.all_shapes = dict(zip(shape_types, range(len(shape_types))))

        self.goal = None
        self.initial = []
        self.occupied = set()
        self.shape_ids = dict()
        for c in range(self.width):
            for r in range(self.height):
                if maze[r, c] == 'G':
                    self.goal = (r, c)
                elif maze[r, c] == '_':
                    self.initial.append((r, c))
                elif maze[r, c] == 'X':
                    self.occupied.add((r, c))
                elif maze[r, c] in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}:
                    self.shape_ids[(r, c)] = len(self.shape_ids)

        self.state = None
        self.render_flag = None
        self.render_mode = render_mode
        self.video = video

        # Variables to fulfill gym env requirements
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(low=np.zeros(2+len(self.shape_ids)),
                                            high=len(self.maze)*np.ones(2+len(self.shape_ids)),
                                            dtype=np.int32)
        self.reward_space = spaces.Box(low=0, high=1, shape=(3,))

        self.renderer = Renderer(self.render_mode, self._render_frame)

    @staticmethod
    def state_to_array(state):
        s = [element for tupl in state for element in tupl]
        return np.array(s, dtype=np.int32)

    def reset(self, seed=None, options=None, render_flag=False, return_info=False):
        self.step_count = 0
        self.truncated = False
        self.terminated = False
        self.render_flag = render_flag
        self.env_maze = copy.deepcopy(self.maze)
        if self.random_initial_position:
            for c in range(self.width):
                for r in range(self.height):
                    if self.env_maze[r, c] == '_':
                        self.env_maze[r, c] = ' '
            self.initial = []
            n_r, n_c = np.shape(self.maze)
            initial_position = False
            while not initial_position:
                r, c = (np.random.randint(0, n_r), np.random.randint(0, n_c))
                if self.maze[r, c] == ' ':
                    self.initial.append((r, c))
                    self.env_maze[r, c] = '_'
                    initial_position = True
        self.state = (random.choice(self.initial), tuple(0 for _ in range(len(self.shape_ids))))
        self.my_render = Render(maze=self.env_maze, render_mode=self.render_mode)
        self.my_render.render_frame(mode=self.render_mode)
        self.renderer.render_step()

        # return self.state, {}
        return (self.state_to_array(self.state), {}) if return_info else self.state_to_array(self.state)

    def step(self, action):
        reward = 0.
        self.step_count += 1

        self.renderer.render_step()
        (row, col), collected = self.state

        # perform the movement
        if action == FourRoom.LEFT:
            col -= 1
        elif action == FourRoom.UP:
            row -= 1
        elif action == FourRoom.RIGHT:
            col += 1
        elif action == FourRoom.DOWN:
            row += 1
        else:
            raise Exception('bad action {}'.format(action))

        s1 = (row, col)

        # out of bounds, cannot move
        if col < 0 or col >= self.width or row < 0 or row >= self.height:
            pass

        # into a blocked cell, cannot move
        elif s1 in self.occupied:
            pass

        # can now move

        # into a goal cell
        elif s1 == self.goal:
            self.state = (s1, collected)
            reward = 1.
            self.terminated = True

        # into a shape cell
        elif s1 in self.shape_ids:
            shape_id = self.shape_ids[s1]
            if collected[shape_id] == 1:
                self.state = (s1, collected)
                # already collected this flag
            else:

                # collect the new flag
                collected = list(collected)
                collected[shape_id] = 1
                collected = tuple(collected)
                self.state = (s1, collected)
                reward = self.shape_rewards[self.maze[row, col]]
        else:
            self.state = (s1, collected)

        # if self.step_count == 30:
        #     import pygame
        #     pygame.image.save(self.my_render.canvas, "four-room2.jpeg")
        # into an empty cell
        if self.step_count >= self.spec.max_episode_steps:
            self.truncated = True
        return self.state_to_array(self.state), reward, self.terminated, self.truncated, {},

    def render(self):
        frames = self.renderer.get_renders()
        if self.video:
            frame_to_video(frames)

        return frames

    def _render_frame(self, mode):
        if mode == 'human':
            self.my_render.update(self.state[0], mode=self.render_mode)
        else:  # rgb_array or single_rgb_array
            return self.my_render.update(self.state[0], mode=self.render_mode)

    def close(self):
        if self.render_mode == 'human':
            import pygame

            pygame.display.quit()
            pygame.quit()


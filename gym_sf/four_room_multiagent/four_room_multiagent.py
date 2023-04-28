# -*- coding: UTF-8 -*-
import gym
from gym import spaces

from gym_sf.four_room.render import Render
from gym_sf.four_room.utilities import frame_to_video
from gym_sf.four_room.four_room import FourRoom
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
    ['_', ' ', ' ', ' ', ' ', ' ', 'X', '2', ' ', ' ', ' ', ' ', '3'],
    [' ', ' ', ' ', ' ', ' ', ' ', 'X', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', '2', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', 'X', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', '_', 'X', '3', ' ', ' ', ' ', ' ', '1']])
REWARDS = dict(zip(['1', '2', '3'], list([1.0, 0.5, -1.0])))
# action_conversion = [('0', [0, 0]),
#                      ('1', [1, 0]),
#                      ('2', [2, 0]),
#                      ('3', [3, 0]),
#                      ('4', [0, 1]),
#                      ('5', [1, 1]),
#                      ('6', [2, 1]),
#                      ('7', [3, 1]),
#                      ('8', [0, 2]),
#                      ('9', [1, 2]),
#                      ('10', [2, 2]),
#                      ('11', [3, 2]),
#                      ('12', [0, 3]),
#                      ('13', [1, 3]),
#                      ('14', [2, 3]),
#                      ('15', [3, 3])]
# action_dict = dict(action_conversion)

action_dict = dict()
for i in range(16):
    action_dict[i] = [i % 4, i // 4]


class FourRoomMultiagent(FourRoom):
    """
    Four room environment suitable for two agents
    """
    def __init__(self, maze=MAZE, shape_rewards=REWARDS,
                 render_mode='rgb_array', random_initial_position=True, video=False,
                 video_path='root', max_num_agents=2, initial_position=[(12,0)], given_initial_position=False):
        super().__init__(maze=maze, shape_rewards=shape_rewards,
                 render_mode=render_mode, random_initial_position=random_initial_position, video=video,
                 video_path=video_path)
        self.max_num_agents = max_num_agents
        self.action_space = spaces.Discrete(4 ** max_num_agents)
        self.observation_space = spaces.Box(low=np.zeros(2*max_num_agents + len(self.shape_ids)),
                                            high=len(self.maze) * np.ones(2*max_num_agents + len(self.shape_ids)),
                                            dtype=np.int32)
        self.action_dict = action_dict
        self.given_initial_position = given_initial_position
        self.init_position = initial_position

    def erase_maze_position(self):
        for c in range(self.width):
            for r in range(self.height):
                if self.env_maze[r, c] == '_':
                    self.env_maze[r, c] = ' '      

    
    def random_position(self):
        self.erase_maze_position()
        # for c in range(self.width):
        #     for r in range(self.height):
        #         if self.env_maze[r, c] == '_':
        #             self.env_maze[r, c] = ' '
        self.initial = []
        n_r, n_c = np.shape(self.maze)
        for _ in range(self.max_num_agents):
            initial_position = False
            while not initial_position:
                r, c = (np.random.randint(0, n_r), np.random.randint(0, n_c))
                if self.maze[r, c] == ' ':
                    self.initial.append((r, c))
                    self.env_maze[r, c] = '_'
                    initial_position = True

    def given_position(self):
        self.erase_maze_position()
        self.initial = self.init_position 
        for r, c in self.init_position:      
            self.env_maze[r, c] = '_'


    @staticmethod
    def state_to_array(state):
        if isinstance(state[0][0], tuple):
            s_agent = [element for tupl in state[0] for element in tupl]
            s_objects = list(state[1])
            s = s_agent + s_objects
        else:
            s = [element for tupl in state for element in tupl]
        return np.array(s, dtype=np.int32)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.step_count = 0
        self.truncated = False
        self.terminated = False
        self.env_maze = copy.deepcopy(self.maze)
        if self.given_initial_position:
            self.given_position()
        if self.random_initial_position:
            self.random_position()
        if self.max_num_agents == 1:
            self.state = (random.choice(self.initial), tuple(0 for _ in range(len(self.shape_ids))))
        else:
            self.state = (self.initial, tuple(0 for _ in range(len(self.shape_ids))))
        self.my_render = Render(maze=self.env_maze, render_mode=self.render_mode)
        if self.render_mode == "rgb_array_list":
            self.frames = []
            self.frames.append(self.my_render.render_frame(mode=self.render_mode, agent=self.initial))
        else:
            self.my_render.render_frame(mode=self.render_mode, agent=self.initial)

        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()


        # return self.state, {}
        return self.state_to_array(self.state), info


    def step(self, actions):
        reward = 0.
        self.step_count += 1
        collected = self.state[1]
        actions = self.action_dict[str(actions)]
        for i in range(self.max_num_agents):
            if self.max_num_agents == 1:
                (row, col) = self.state[0]
                action = actions[0]
            else:
                (row, col) = self.state[0][i]
                action = actions[i]


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
                update = False

            # into a blocked cell, cannot move
            elif s1 in self.occupied:
                update = False

            # can now move

            # into a goal cell
            elif s1 == self.goal:
                update = True
                reward = 1.
                self.terminated = True

            # into a shape cell
            elif s1 in self.shape_ids:
                shape_id = self.shape_ids[s1]
                if collected[shape_id] == 1:
                    update = True
                    # already collected this flag
                else:

                    # collect the new flag
                    collected = list(collected)
                    collected[shape_id] = 1
                    collected = tuple(collected)
                    update = True
                    reward = self.shape_rewards[self.maze[row, col]]
            else:
                update = True
            if update:
                agent_state = copy.deepcopy(self.state[0])
                if self.max_num_agents > 1:
                    agent_state[i] = s1
                else:
                    agent_state = s1
                self.state = (agent_state, collected)

            # into an empty cell
            if self.step_count >= self.spec.max_episode_steps:
                self.truncated = True

            info = self._get_info()

        if self.render_mode == 'human' or self.render_mode == 'rgb_array_list':
            self._render_frame()

        return self.state_to_array(self.state), reward, self.terminated, self.truncated, info

    def _render_frame(self):
        if self.render_mode == 'human':
            self.my_render.update(self.state[0], mode=self.render_mode)
        elif self.render_mode == 'rgb_array':  # rgb_array or single_rgb_array
            return self.my_render.update(self.state[0], mode=self.render_mode)
        elif self.render_mode == 'rgb_array_list':
            self.frames.append(self.my_render.update(self.state[0], mode=self.render_mode))


if __name__ == '__main__':

    import os

    # render_mode = "rgb_array_list" # "rgb_array" "rgb_array_list"
    render_mode = 'human'
    video_path = os.getcwd()
    # num_agents = 2

    num_agents = 2

    env = gym.make("four-room-multiagent-v0", render_mode=render_mode, max_episode_steps=5000,
                video=True, video_path=video_path, max_num_agents=num_agents, given_initial_position=False)
    # env = gym.make("four-room-v0", render_mode='human', new_step_api=True, max_episode_steps=5000)
    terminated = False
    truncated = False
    env.reset()

    for _ in range(500):
        action = env.action_space.sample()
        for agent in range(num_agents):
            if np.random.random() < 0.20:
                if np.random.random() < 0.50:
                    action = 2
                else:
                    action = 1
        next_state, reward, terminated, truncated, _ = env.step(action)

        if terminated or truncated:
            env.render()
            env.reset()
    env.close()
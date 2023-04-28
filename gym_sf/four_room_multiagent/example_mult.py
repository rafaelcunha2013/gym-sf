import numpy as np
import gym
import gym_sf
import os
import time

############# --- run 'pip intall ." on the terminal, on the same level as setup.py
# to install the package locally"

# render_mode = "rgb_array_list" # "rgb_array" "rgb_array_list"
render_mode = 'human'
video_path = os.getcwd()
num_agents = 2
initial_position=[(12,0), (11, 0)]


env = gym.make("four-room-multiagent-v0", render_mode=render_mode, max_episode_steps=5000,
               video=True, video_path=video_path, max_num_agents=num_agents, 
               given_initial_position=True, initial_position=[(12,0), (12, 0)],
               random_initial_position=False)
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
    # time.sleep(1)

    if terminated or truncated:
        env.render()
        env.reset()
env.close()
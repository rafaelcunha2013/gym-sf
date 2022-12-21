import numpy as np
import gym
import gym_sf

render_mode = "rgb_array_list" # "rgb_array" "rgb_array_list"
env = gym.make("four-room-v0", render_mode=render_mode, max_episode_steps=5000,
               video=True)
# env = gym.make("four-room-v0", render_mode='human', new_step_api=True, max_episode_steps=5000)
terminated = False
truncated = False
env.reset()

for _ in range(500):
    action = env.action_space.sample()
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

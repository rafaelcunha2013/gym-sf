import numpy as np
import gym

# env = gym.make("gym_sf/four-room-v0")
env = gym.make("gym_sf:gym_sf/four-room-v0", render_mode='human', new_step_api=True, max_episode_steps=5000)
# env = FourRoom(render_mode='rgb_array')
terminated = False
truncated = False
env.reset()

for _ in range(50):
    # a.append(env.render())
    env.render()
    action = env.action_space.sample()
    if np.random.random() < 0.20:
        if np.random.random() < 0.50:
            action = 2
        else:
            action = 1
    next_state, reward, terminated, truncated, _ = env.step(action)

    if terminated or truncated:
        env.reset()
env.close()

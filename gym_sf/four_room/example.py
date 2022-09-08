import numpy as np
from four_room import FourRoom
# from render import Render

env = FourRoom()
done = False
env.reset()

for _ in range(5000):
    env.render()
    action = env.action_space.sample()
    if np.random.random() < 0.20:
        if np.random.random() < 0.50:
            action = 2
        else:
            action = 1
    next_state, reward, done = env.step(action)

    if done:
        env.reset()
        # print('hi')




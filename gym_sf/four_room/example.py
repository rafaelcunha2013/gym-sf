import numpy as np
from four_room import FourRoom
# from render import Render

env = FourRoom(render_mode='rgb_array')
done = False
env.reset()
a = []

for _ in range(50):
    a.append(env.render())
    action = env.action_space.sample()
    if np.random.random() < 0.20:
        if np.random.random() < 0.50:
            action = 2
        else:
            action = 1
    next_state, reward, done = env.step(action)

    if done:
        env.reset()
        print('hi')
env.close()
print(a)

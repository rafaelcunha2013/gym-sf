import numpy as np
from four_room import FourRoom
from render import Render

gridworld = FourRoom()

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
        gridworld = FourRoom()
        s0 = gridworld.initialize()
        my_grid = Render(maze=gridworld.env_maze)



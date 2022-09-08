
# Gym-SF: Reinforcement Learning Environments to use with Successor Features

Gym environments for transfer reinforcement learning problems that uses successor features. The environments follow the standard [gym's API](https://github.com/openai/gym).

For details on successor features definitions, see [Fast reinforcement learning with generalized policy updates](https://www.pnas.org/doi/10.1073/pnas.1907370117).

## Install

Via pip:
```bash
pip install gym-sf
```

Alternatively, you can install the newest unreleased version:
```bash
git clone https://github.com/rafaelcunha2013/gym-sf.git
cd gym-sf
pip install -e .
```

## Usage

```python
import gym
import gym_sf

env = gym_sf.make("gym_sf:gym_sf/four-room-v0", render_mode='human', new_step_api=True, max_episode_steps=5000)

terminated = False
truncated = False
env.reset()

for _ in range(500):
    env.render()
    action = env.action_space.sample()
    next_state, reward, terminated, truncated, _ = env.step(action)
    
    if terminated or truncated:
        env.reset()
env.close()
```


## Environments

| Env | Obs/Action spaces | Objectives | Description |
| --- | --- | --- | --- |
|  `four-room-v0` <br><img src="https://raw.githubusercontent.com/LucasAlegre/mo-gym/main/screenshots/four-room.png" width="200px"> | Discrete / Discrete |  `[item1, item2, item3]` | Agent must collect three different types of items in the map and reach the goal. From [Alegre et al. 2022](https://proceedings.mlr.press/v162/alegre22a.html). |


## Citing

If you use this repository in your work, please cite:

```bibtex
@misc{gym-sf,
  author = {Rafael F. Cunha},
  title = {Gym-SF: Reinforcement Learning Environments to use with successor features},
  year = {2022},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/rafaelcunha2013/gym-sf}},
}
```

## Acknowledgments

* The `README.md` and package structure is based on https://github.com/LucasAlegre/mo-gym.
* The `sf-four-room-v0` env is based on https://github.com/mike-gimelfarb/deep-successor-features-for-transfer.
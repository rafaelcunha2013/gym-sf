from gym.envs.registration import register

register(
    id='gym_sf/four-room-v0',
    entry_point='gym_sf.four_room:FourRoom',
    max_episode_steps=5000,
)
# import gym_sf.four_room
# from gym_sf.four_room.four_room import FourRoom
# from gym_sf.four_room.render import Render

from gym_sf.four_room.render import Render
from gym.envs.registration import register

register(
    id='four-room-multiagent-v0',
    entry_point='gym_sf.four_room_multiagent.four_room_multiagent:FourRoomMultiagent',
    max_episode_steps=5000,
)
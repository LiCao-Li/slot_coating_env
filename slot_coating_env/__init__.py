from gym.envs.registration import register

register(
    id='slotdie-v0',
    entry_point='slot_coating_env.envs:SlotDie',
)

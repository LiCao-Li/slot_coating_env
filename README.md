# slot_coating_env

customize an initial environment for the slot die coating process, given a type of liquid.

States values are continuous (np.array) for contacting angles, describing liquid positions. 

Action values are continous (np.array), including coating machine setting parameters. 
- web transfer speed
- coating gap
- ratio between coating gap and target thickness 

Rewards are customized based on physical formulas for Newtonian and Non-Newtonian liquids.

next step:
1. Q-learning for simple test and debudding 
2. DDPG algorithm testing
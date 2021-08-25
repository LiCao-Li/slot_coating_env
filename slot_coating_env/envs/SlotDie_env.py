import gym 
from gym import error, space, utils
from gym.utils import seeding

Class SlotDie(gym.Env):

    """slot_die coating process
    The goal of this algorithm is to max the rewards among 100 independent coating experiments by using a certain type of liquid
    determinied values for a certain type of liquid:
    - ink viscosity
    - density
    - surface tension
    these values are ink properties value, it can be determined based on type of liquids
	
	At each step, agent will have a state that depicts the liquid position:
	theta - contacting angle on the bottom
    phi - contacting angle on the top

    After each step the agent receives an observation of:
    - 0: no experiments conducted (after reset)
    - 1: defect free
    - 2: leaking
    - 3: breaking-up
	
	actions contains: U, mu, g, r
	U - coating speed
	g - coating gap
	r - ratio between coating gap and target thickness
	
	fixed value for machine settings:
	- coating width
	- xf position (judgement for defects)

	intermediate values during calculation phase:
	- target thickness
	- flow rate
	- a,b_l,b_s,modified_CA, ambient pressure

	help function:
	- check_function(inputs_from_actions): return x_u values

    The rewards is estimated by x_u values, it depicts the distance between x_u and x_f

    Ideally an agent will be able to recognise actions that lead to a higher reward and
    increase the rate in which choose that direction until the reward reaches
    its maximum 
    """
	def __init__(self):
	# self.action_space, self_observation_space
	
    self.experiments_count = 0
    self.experiments_max = 100
    self.observation = 0

    self.x_f = 500
    self.Lu = 500
    # liquid property
    self.viscosity = 23
    self.density = 1210
    self.n = 1
    self.m = 0.045
    self.surface = 0.066
    # variables
    # states value are liquid positions
	self.observation_space = spaces.Box(low = np.array([60,120]), 
											high = np.array([120,160]), dtype=np.uint8)
	# action values are web_speed, coating_gap and ratios
	self.action_space = spaces.Box(low = np.array([0.05,200,1.5]), 
										high = np.array([0.1,500,5]))

	def judge(self,action):

		return x_u

	def reset(self): 
	# return a value self.observation_space	

    self.experiments_count = 0
    self.observation = 0
    return self.observation


	def step(self,action):
		if (self.judge(action) <= self.x_f - self.Lu):
            self.observation = 3 # defect free

        elif (self.judge(action) >= self.x_f):
            self.observation = 2  # break-up

        elif (self.judge(action) < self.x_f and self.judge(action) > 0):
            self.observation = 1  # defects free

        reward = self.judge(action)

        self.experiments_count += 1
        done = self.experiments_count >= self.experiments_max
        info = {}

        return self.observation, reward, done, info








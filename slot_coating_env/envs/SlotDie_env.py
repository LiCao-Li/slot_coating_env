import gym 
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np

class SlotDie(gym.Env):
    
    """ Explaination
    slot_die coating process
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
    - judge(inputs_from_actions): return x_u values

    The rewards is estimated by x_u values, it depicts the distance between x_u and x_f

    Ideally an agent will be able to recognise actions that lead to a higher reward and
    increase the rate in which choose that direction until the reward reaches
    its maximum 
    """
    def __init__(self):
        # self.action_space, self_observation_space
        self.experiments_count = 0
        self.experiments_max = 1000
        self.observation = 0
        self.x_f = 500*1e-6
        self.Lu = 500*1e-6
        # liquid property
        self.mu = 23
        self.density = 1210
        self.n = 1
        self.m = 0.045
        self.h_w = 0.1
        self.surface = 0.066
        self.xd = 2*self.Lu + self.h_w
        # variables
        # states value are liquid positions
        self.observation_space = spaces.Box(low = np.array([60,120]),high = np.array([120,160]), dtype=np.uint8)
        # action values are web_speed, coating_gap and ratios
        self.action_space = spaces.Box(low = np.array([0.05,200,1.5]),high = np.array([0.1,500,5]))
        self.state = self.observation_space.sample()
    
    def judge(self,action_sample):
        # nd.array action [U,g,r]
        self.thickness = action_sample[1]/action_sample[2]
        self.a = (action_sample[0]*(self.n+1)*(2*self.n+1)/self.n)**n*(action_sample[1]**(-n-1))
        self.b_s = (action_sample[0]*(action_sample[1]-2*self.thickness)*(n+1)*(2*n+1)/n)**n * (action_sample[1]**(-2*n-1))
        self.b_l = -(action_sample[0]*(2*self.thickness-action_sample[1])*(n+1)*(2*n+1)/n)**n * (action_sample[1]**(-2*n-1))
        self.modified_CA = ((action_sample[0]*self.m*(action_sample[0]/action_sample[1])**(n-1))/self.surface)**(2/3)
        self.fr = self.thickness*(action_sample[0]*self.h_w)
        
        self.p_ambient = self.density*action_sample[0]**2/2
        if self.thickness < action_sample[1]/2:
            self.xu_estimate = self.x_f - action_sample[1]**2*(self.p_ambient - 1.34*self.modified_CA*self.surface/self.thickness - (self.xd-self.x_f)*self.m*self.b_s - self.surface*(math.cos(self.state[1])+math.cos(self.state[0]))/action_sample[2])/(6*self.mu*action_sample[0])

                
        elif self.thickness > action_sample[1]/2:
            self.xu_estimate = self.x_f - action_sample[1]**2*(self.p_ambient - 1.34*self.modified_CA*self.surface/self.thickness - (self.xd-self.x_f)*self.m*self.b_l - self.surface*(math.cos(self.state[1])+math.cos(self.state[0]))/action_sample[2])/(6*self.mu*action_sample[0])

        return self.xu_estimate
    

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

        else:
            self.observation = 1  # defects free

        reward = self.x_f - self.judge(action)

        self.experiments_count += 1
        done = self.experiments_count >= self.experiments_max
        info = {}

        return self.observation, reward, done, info








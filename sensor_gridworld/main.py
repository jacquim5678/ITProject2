from cgitb import reset
import gym
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from gym import spaces

class SensorGridWorld(gym.Env):
       # Custom Sensor Grid world environment. This 
       # environment will simulate a battlefield 
       # encompassing a High value target, sensors and enemy targets
       def __init__(self, grid_size=1048):
              super(SensorGridWorld, self).__init__()
              # Size 
              self.grid_size = grid_size
              self.HVT = ((45,23))
              self.DRONES = 4
              self.ENEMY = 1

       def reset(self):
              self.grid = np.random.randint(100, size=(1048,1048))
              temp = self.grid
              return temp

       def render(self, mode='console'):
              print(self.grid)
              sns.set(rc={'figure.figsize':(30,30)})
              sns.heatmap(self.grid, cbar=False, cbar_ax = False, square = True, yticklabels = False, xticklabels = False)
              plt.tight_layout(pad=0)
              plt.show()

       def close(self):
              pass
env = SensorGridWorld()
env.reset()
env.render()

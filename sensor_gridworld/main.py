import random
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
              # 1 grid square = 1m2
              self.grid = np.zeros((1048,1048))
              # High Value Target
              self.grid[509:539,509:539] = 75
              numDrone = self.DRONES
              for each in range (0,numDrone):
                     temp1 = random.randint(0,1048)
                     temp2 = random.randint(0, 1048)
                     self.grid[temp1 - 100:temp1 + 100, temp2 - 100:temp2 + 100] = 150
                     self.grid[temp1 - 75:temp1 + 75, temp2 - 75:temp2 + 75] = 200
                     self.grid[temp1 - 25:temp1 + 25, temp2 - 25:temp2 + 25] = 125
                     self.grid[temp1, temp2] = 0
                     # High Value Target
              self.grid[509:539, 509:539] = 75
              temp = self.grid
              return temp

       def render(self, mode='console'):
              print(self.grid)
              sns.set(rc={'figure.figsize':(30,30)})
              sns.heatmap(self.grid, cbar=False, cbar_ax = False, square = True, yticklabels = False, xticklabels = False, vmin=0, vmax=250, cmap="cubehelix")
              plt.tight_layout(pad=0)
              plt.show()

       def close(self):
              pass
env = SensorGridWorld()
env.reset()
env.render()

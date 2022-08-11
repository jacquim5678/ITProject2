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
              SENSORS = (("Radar",200),("IR",60),("Light",40))
              DRONES = list()

              for each in range(0, numDrone):
                     DRONES.append((random.randint(0,1048),random.randint(0,1048)))
              print(DRONES)
              # Sensor 1
              for x in range(0, numDrone):
                     self.grid[DRONES[x][0] - SENSORS[0][1]:DRONES[x][0] + SENSORS[0][1], DRONES[x][1] - SENSORS[0][1]: DRONES[x][1] + SENSORS[0][1]] = 150
              # Sensor 2
              for x in range(0, numDrone):
                     self.grid[DRONES[x][0] - SENSORS[1][1]:DRONES[x][0] + SENSORS[1][1], DRONES[x][1] - SENSORS[1][1]: DRONES[x][1] + SENSORS[1][1]] = 75
              # sensor 3
              for x in range(0, numDrone):
                     self.grid[DRONES[x][0] - SENSORS[2][1]:DRONES[x][0] + SENSORS[2][1], DRONES[x][1] - SENSORS[2][1]: DRONES[x][1] + SENSORS[2][1]] = 30
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

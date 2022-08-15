import random
from cgitb import reset
import gym
import warnings


import xarray as xr
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge, Polygon, Rectangle, PathPatch
from matplotlib.path import Path
from matplotlib.collections import PatchCollection

import numpy as np
from gym import spaces

warnings.simplefilter("always")

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
              patches = []
              numDrone = self.DRONES
              SENSORS = (("Radar",200),("IR",60),("Light",40))
              DRONES = list()
              patches.append((Rectangle((450,450), 400, 150, color="green")))

              x = []
              x.append(tuple((random.randint(0,1048),random.randint(0,1048))))
              x.append(tuple((random.randint(0,1048),random.randint(0,1048))))
              x.append(tuple((random.randint(0,1048),random.randint(0,1048))))
              print(x)
              
              for x in x:
                     circle = Circle((x[0], x[1]), 210, color="purple", alpha=0.5)
                     patches.append(circle)
                     circle = Circle((x[0], x[1]), 75, color="yellow", alpha=0.5)
                     patches.append(circle)
                     circle = Circle((x[0], x[1]), 180, color="pink", alpha=0.5)
                     patches.append(circle)
                     circle = Circle((x[0], x[1]), 1, color="black", alpha=1)
                     patches.append(circle)
              
              numEnemy = self.ENEMY
              ENEMY = list()
              stepsEmtake = 1000  # No. of times will iterate through movements
              # Do only once to set starting point
              ENEMY.append((random.randint(0, 200), random.randint(0, 200)))
              for x in range(0, stepsEmtake):
                  print("em location is")
                  print(ENEMY)
                  ENEMY.append((ENEMY[x][0] + random.randint(-5, 5), ENEMY[x][1] + random.randint(-5, 5)))  # Indicates EM
                  # movement should probs only be one 1m
              temp = ENEMY.copy()
              temp.append((0,0))
              
              print(ENEMY)
              code = [Path.MOVETO] + [Path.LINETO]*(len(ENEMY)-1) + [Path.CLOSEPOLY]
              print(code)
              path = Path(temp,code)
              enemyPath = PathPatch(path, color='red', lw=100, fill=False)
              
              dimension = []
              dimension.append(Rectangle((0,0), 1, 1))  
              dimension.append(Rectangle((0,1048), 1, 1)) 
              dimension.append(Rectangle((1048,0), 1, 1)) 
              dimension.append(Rectangle((1048,1048), 1, 1)) 
              print(patches)
              print(dimension)              
              p2= PatchCollection(dimension, alpha=0)
              print(enemyPath)
              fig, ax = plt.subplots(figsize=(1048,1048), dpi=10)
              ax.add_collection(p2)
              for each in patches:
                  ax.add_artist(each)
              ax.add_patch(enemyPath)
              plt.xlim([0,1048])
              plt.ylim([0,1048])
              plt.tight_layout(pad=.5)
              plt.axis("image")
              
              plt.show()
              
              
       def render(self, mode='console'):
                print("render")

       def close(self):
              pass
env = SensorGridWorld()
env.reset()
env.render()

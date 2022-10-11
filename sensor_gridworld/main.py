import random
from cgitb import reset
import gym
import warnings
import math

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
    def __init__(self, grid_size, DRONES):
        super(SensorGridWorld, self).__init__()
        # Size
        self.grid_size = grid_size
        self.DRONES = DRONES
        self.REDTEAM = 1

    def reset(self):
        # Grid Plot Initialisation
        fig, ax = plt.subplots(figsize=(1048, 1048), dpi=10)
        plt.xlim([0, 1048])
        plt.ylim([0, 1048])
        plt.tight_layout(pad=0)
        plt.axis("image")

        # Empty Grid
        Grid = []
        Grid.append(Rectangle((0, 0), 1, 1))
        Grid.append(Rectangle((0, 1048), 1, 1))
        Grid.append(Rectangle((1048, 0), 1, 1))
        Grid.append(Rectangle((1048, 1048), 1, 1))
        GridPatch = PatchCollection(Grid, alpha=0)
        ax.add_collection(GridPatch)

        # High Value Target
        HVT = []
        HVT.append(Rectangle((450, 450), 400, 150, color="blue"))
        for x in HVT:
            ax.add_artist(x)

        # Obstacles
        Obstacles = []
        for x in range(0, 4):
            Obstacles.append(Rectangle((random.randint(0, 1048), random.randint(
                0, 1048)), random.randint(20, 100), random.randint(20, 100), color="black"))
        for x in Obstacles:
            ax.add_artist(x)

        # Sensors
        SENSEDAREA = []
        DRONES = self.DRONES
        Drones = []
        rpt = 1
        for x in DRONES:
            sensor = x[1]
            for y in sensor:
                Drones.append(Circle(
                    (x[0][0], x[0][1]), SensorData[y-1][1], color=SensorData[y-1][3], alpha=0.5))
                #------------------- Find Area covered by Sensors -----------------------#
                init_XY = ((x[0][0] - SensorData[y-1][1]), (x[0][1] - SensorData[y-1][1]))

                #go through each cell in the square produced by sensor range and if distance to center is greater than range, do not append to sensed area
                z = 0
                for z in range(2 * (SensorData[y-1][1])):
                    a = 0
                    for a in range(2 * (SensorData[y-1][1])):
                        dist = math.sqrt(abs(((init_XY[0] - x[0][0])**2 + (init_XY[1] - x[0][1])**2)))
                        if (dist < SensorData[y-1][1]):
                            SENSEDAREA.append(init_XY)
                        init_XY = (init_XY[0] + 1, init_XY[1])
                        a = a + 1
                    init_XY = (init_XY[0] - 2*(SensorData[y-1][1]) + 1, init_XY[1] + 1)
                    z = z + 1
        for x in Drones:
            ax.add_artist(x)    

        SENSEDAREA = list(dict.fromkeys(SENSEDAREA))
        #print(DRONES[0][0])

        x = []
        x.append(tuple((random.randint(0, 1048), random.randint(0, 1048))))
        x.append(tuple((random.randint(0, 1048), random.randint(0, 1048))))
        x.append(tuple((random.randint(0, 1048), random.randint(0, 1048))))
        
        # REDTEAM
        
        numREDTEAM = self.REDTEAM
        REDTEAM = 0
        stepsRedtake = 0  # No. of times will iterate through movements
        # Do only once to set starting point
        # Assigning grid coord fpr EN to spwan at (only edges)
        sides = ['top', 'bottom', 'left', 'right']
        side = random.choice(sides)
        if side == 'top':
            # Cord to spawn at top (x,Y)
            REDTEAM = ((random.randint(0, 1048), random.randint(0, 100)))
        elif side == 'bottom':
            REDTEAM = ((random.randint(0, 1048), random.randint(900, 1048)))
        elif side == 'left':
            REDTEAM = ((random.randint(0, 100), random.randint(0, 1048)))
        elif side == 'right':
            REDTEAM = ((random.randint(900, 1048), random.randint(0, 1048)))
        
        #no longer needed
        # for x in range(0, stepsRedtake):
        #     REDTEAM.append((REDTEAM[x][0] + random.randint(-100, 100),
        #                  REDTEAM[x][1] + random.randint(-100, 100)))  # Indicates EM
        #     # movement should probs only be one 1m
        
        
        # getting REDTEAM to centre
        GRIDSIZE = 1048
        MIDPOINT = int(GRIDSIZE/2)
        MIDCORDS = (MIDPOINT, MIDPOINT)
        #print("REDTEAM COORDS: ", REDTEAM[0], REDTEAM[1])
        #used to preserve values of REDTEAm tuple for drawing of REDTEAM path
        REDTEAMCALCS = (REDTEAM[0], REDTEAM[1])

        # ------------------ List of places REDTEAM tranversed --------------------#
        ## linear line formula y = mx + c;
        #since redteam is travelling to exact middle, treat middle as origin and thus c will be 0
        RedTeamLocations = []
        #subtract origin point values of midcords to get euclidean location of redteam
        REDTEAMCALCS = (((REDTEAMCALCS[0]-MIDCORDS[0]), (REDTEAMCALCS[1]-MIDCORDS[1])))
        if REDTEAMCALCS[0] != 0:
            gradient = (REDTEAMCALCS[1]/REDTEAMCALCS[0])
        for x in range(abs(REDTEAMCALCS[0])):
            y = gradient * x
            y = round(y)
            #add back midcord values to get actual location of redteam at each timestep
            x = x + MIDCORDS[0]
            y = y + MIDCORDS[1]
            temp = [x,y]
            RedTeamLocations.append(temp)
        # Two end points to plot
        RedTeamtStartEnd = [REDTEAM, MIDCORDS]
        
        # Drawing the line between points
        code = [Path.MOVETO] + [Path.LINETO] 
        path = Path(RedTeamtStartEnd, code)
        
        RedTeamPath = PathPatch(path, color='red', lw=100, fill=False)

        #loop through RedTeamLocations and check if cell exists in Sensed Area
        RedTeamSensed = []

        x = 0
        for x in range(len(RedTeamLocations)):
            print(RedTeamLocations[x], SENSEDAREA.count(RedTeamLocations[x]))
            if SENSEDAREA.count(x) >= 1:
                RedTeamSensed.append(x)
            x = x + 1
        
        #print(DRONES[0][0])
        #print(SENSEDAREA.count((633, 424)))#

        if len(RedTeamSensed) > 0:
            print("The Red Team was sensed at locations: ", RedTeamSensed)
        else:
            print("The Red Team was not sensed ", RedTeamSensed)

        ax.add_patch(RedTeamPath)
        plt.show()

    def render(self, mode='console'):
        print("render")

    def close(self):
        pass


# No - Name - Range - Battery Use
# 3 - IR - 15m - 2 - Pink
# 4 - US - 10m - 1 - Green
# 1 - Acoustic - 100m - 2 - Yellow
# 2 - Optical - 45m - 6 - Purple
SensorData = (("Acoustic", 100, 2, "yellow"), ("Optical", 45, 6,
              "purple"), ("IR", 15, 2, "pink"), ("US", 10, 1, "green"))
GRIDSIZE = 1048
MIDPOINT = int(GRIDSIZE/2)
T = GRIDSIZE/5
# SensorGridWorld(GridSize,DroneCharacteristic)
DRONES = []
DRONES.append(((int(T+MIDPOINT), int(MIDPOINT)), (1, 3, 4)))
DRONES.append(
    ((int(T+math.cos(60)+MIDPOINT), int(T+math.sin(60)+MIDPOINT)), (2, 3)))
DRONES.append(((int(-T+math.cos(120)+MIDPOINT),
              int(T+math.sin(120)+MIDPOINT)), (1, 2, 3, 4)))
DRONES.append(((int(-T+MIDPOINT), MIDPOINT), (1, 3, 4)))
DRONES.append(
    ((int(-T+math.cos(240)+MIDPOINT), int(-T+math.sin(240)+MIDPOINT)), (2, 3, 4)))
DRONES.append(
    ((int(T+math.cos(360)+MIDPOINT), int(-T+math.sin(360)+MIDPOINT)), (3, 4)))

#print(DRONES)

env = SensorGridWorld(GRIDSIZE, DRONES)
env.reset()
env.render()

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
        gridSize = 1048
        fig, ax = plt.subplots(figsize=(gridSize, gridSize), dpi=10)
        plt.xlim([0, gridSize])
        plt.ylim([0, gridSize])
        plt.tight_layout(pad=0)
        plt.axis("image")

        # Empty Grid
        Grid = []
        Grid.append(Rectangle((0, 0), 1, 1))
        Grid.append(Rectangle((0, gridSize), 1, 1))
        Grid.append(Rectangle((gridSize, 0), 1, 1))
        Grid.append(Rectangle((gridSize, gridSize), 1, 1))
        GridPatch = PatchCollection(Grid, alpha=0)
        ax.add_collection(GridPatch)

        # High Value Target
        HVT = []
        HVTlocation = (450, 450)
        HVTwidth = 400
        HVThieght = 150
        HVT.append(Rectangle(HVTlocation, HVTwidth, HVThieght, color="blue"))
        for x in HVT:
            ax.add_artist(x)

        # Obstacles
        Obstacles = []
        ObstaclesX1 = []
        ObstaclesY1 = []
        ObstaclesX2 = []
        ObstaclesY2 = []
        numObstacles = 4
        for x in range(0, numObstacles):
            v1 = random.randint(0, 1048)
            v2 = random.randint(0, 1048)
            v3 = random.randint(20, 500)
            v4 = random.randint(20, 500)
            #-------------- Find Area Obstacles Cover----------------------------------------#
            ObstaclesX1.append(v1)
            ObstaclesY1.append(v2)
            ObstaclesX2.append(v1 + v3)
            ObstaclesY2.append(v2 + v4)
            
            Obstacles.append(Rectangle((v1, v2), v3, v4, color="black"))
        for x in Obstacles:
            ax.add_artist(x)
            
      
        # Sensors
        SENSEDAREA = []
        DRONES = self.DRONES
        Drones = []
        rpt = 1
        for x in DRONES:
            sensor = x[1]
            #print("Starting Drone: ", x)
            for y in sensor:
                #print("------- Starting Sensor: ", y)
                #print("-------------- Sensor range: ", SensorData[y-1][1])
                init_length = len(SENSEDAREA)
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
                    init_XY = (init_XY[0] - 2*(SensorData[y-1][1]), init_XY[1] + 1)
                    z = z + 1
                #print("-------------- Sensor area: ", len(SENSEDAREA) - init_length)
        for x in Drones:
            ax.add_artist(x)    

        SENSEDAREA = list(dict.fromkeys(SENSEDAREA))

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
        ENDPOINT = MIDCORDS
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
        if REDTEAMCALCS[0] > 0:    
            for x in range(REDTEAMCALCS[0]):
                y = gradient * x
                y = round(y)
                #add back midcord values to get actual location of redteam at each timestep
                temp = (x + 524, y + 524)
                RedTeamLocations.append(temp)
        if REDTEAMCALCS[0] < 0:    
            for x in range(0, REDTEAMCALCS[0]+1, -1):
                y = gradient * x
                y = round(y)
                #add back midcord values to get actual location of redteam at each timestep
                temp = (x + 524, y + 524)
                RedTeamLocations.append(temp)
                
        # Loop through RedTeamLocations if hit an obstacle
        # Function to determine if a point lies within a rectangle
        def FindPoint(x1, y1, x2,
              y2, x, y) :
            if (x > x1 and x < x2 and
                y > y1 and y < y2) :
                return True
            else :
                return False
        blocked = False
        
        for obs in range(len(Obstacles)):
            for y in range(len(RedTeamLocations)-1, -1, -1):
                blocked = FindPoint(ObstaclesX1[obs], ObstaclesY1[obs], ObstaclesX2[obs], ObstaclesY2[obs], RedTeamLocations[y][0], RedTeamLocations[y][1])
                if blocked == True:
                    print("Hit an obs at " + str(RedTeamLocations[y][0]) + " " +  str(RedTeamLocations[y][1]))
                    # Moves the end point of the to where obstacle blocked it 
                    ENDPOINT = ((RedTeamLocations[y][0]), (RedTeamLocations[y][1]))
                    # Removes RedTeamLocation after obstacle point from list
                    RedTeamLocationsv2 = list(RedTeamLocations)
                    del RedTeamLocationsv2[-y:]
                    RedTeamLocations = RedTeamLocationsv2
                    break
        
        # Two end points to plot
        RedTeamtStartEnd = [REDTEAM, ENDPOINT]
        
        # Drawing the line between points
        code = [Path.MOVETO] + [Path.LINETO] 
        path = Path(RedTeamtStartEnd, code)
        
        RedTeamPath = PathPatch(path, color='red', lw=100, fill=False)

                    
        #loop through RedTeamLocations and check if cell exists in Sensed Area
        RedTeamSensed = []
        if blocked == False:
            for x in RedTeamLocations:
                if SENSEDAREA.count(x) > 0:
                    RedTeamSensed.append(x)
    
            if len(RedTeamSensed) > 0:
                print("The Red Team was sensed at locations: ", RedTeamSensed)
                print("Sensed ", round((len(RedTeamSensed)/len(RedTeamLocations)) * 100), "% of RedTeam Cells" )
            else:
                print("The Red Team was not sensed ", RedTeamSensed)
                
            ax.add_patch(RedTeamPath)
            plt.show()
            
        if blocked == True:
            for x in RedTeamLocationsv2:
                if SENSEDAREA.count(x) > 0:
                     RedTeamSensed.append(x)
     
            if len(RedTeamSensed) > 0:
                print("The Red Team was sensed at locations: ", RedTeamSensed)
                print("Sensed ", round((len(RedTeamSensed)/len(RedTeamLocationsv2)) * 100), "% of RedTeam Cells" )
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
T = GRIDSIZE/6
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

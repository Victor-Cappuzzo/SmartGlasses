import math
import numpy as np

class Screen():
    def __init__(self, theta1, theta2, width, height, x, y, z):
        self.theta1 = theta1 * math.pi / 180
        self.theta2 = theta2 * math.pi / 180
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.z = z

        # Calculate rotation matrices
        R1 = [[1, 0,                      0                    ],
              [0, math.cos(self.theta1), -math.sin(self.theta1)],
              [0, math.sin(self.theta1),  math.cos(self.theta1)]]

        R2 = [[ math.cos(self.theta2), 0, math.sin(self.theta2)],
              [ 0,               1,    0                       ],
              [-math.sin(self.theta2), 0, math.cos(self.theta2)]]
        
        # Calculate normal vector of screen
        # The unrotated normal vector is the Z-axis
        self.normal = np.dot(R2, np.dot(R1, np.array([0, 0, 1])))

        # Variables for the point where each of the 9 rays will start
        #   In form of [x, y, z] for each point
        #   This is before the screen is rotated into place (on XY plane)
        self.intersect_points = [[x, y, z], # Center
                                 [x-self.width/2, y+self.height/2, z], # Top left
                                 [x, y+self.height/2, z], # Top middle
                                 [x+self.width/2, y+self.height/2, z], # Top right
                                 [x-self.width/2, y, z], # Middle left
                                 [x+self.width/2, y, z], # Middle right
                                 [x-self.width/2, y-self.height/2, z], # Bottom left
                                 [x, y-self.height/2, z], # Bottom center
                                 [x+self.width/2, y-self.height/2, z],] # Bottom right
        
        # Rotate the screen into place
        for i in range(9):
            self.intersect_points[i] = np.dot(R2, np.dot(R1, self.intersect_points[i]))


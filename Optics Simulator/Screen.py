import math
import numpy as np
import matplotlib.pyplot as plt

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
        #print("Screen normal: ", self.normal)

        # Variables for the point where each of the 9 rays will start
        #   In form of [x, y, z] for each point
        #   This is before the screen is rotated into place (centered on XY plane)
        #   1 2 3
        #   4 0 5
        #   6 7 8
        self.intersect_points = np.array([[0, 0, 0], # Center
                                 [-self.width/2, self.height/2, 0], # Top left
                                 [0, self.height/2, 0], # Top middle
                                 [self.width/2, self.height/2, 0], # Top right
                                 [-self.width/2, 0, 0], # Middle left
                                 [self.width/2, 0, 0], # Middle right
                                 [-self.width/2, -self.height/2, 0], # Bottom left
                                 [0, -self.height/2, 0], # Bottom center
                                 [self.width/2, -self.height/2, 0],]) # Bottom right
        
        # Rotate and translate the screen into place
        for i in range(9):

            # Rotation
            self.intersect_points[i] = np.dot(R2, np.dot(R1, self.intersect_points[i]))

            # Translation
            self.intersect_points[i] += [self.x, self.y, self.z]

      # Plot the screen using the intersect points
      def plot_screen(self, ax):

            # Put X intersect points into a 3x3 grid
            xx = [[self.intersect_points[1][0], self.intersect_points[2][0], self.intersect_points[3][0]],
                  [self.intersect_points[4][0], self.intersect_points[0][0], self.intersect_points[5][0]],
                  [self.intersect_points[6][0], self.intersect_points[7][0], self.intersect_points[8][0]]]

            # Put Y intersect points into a 3x3 grid
            yy = [[self.intersect_points[1][1], self.intersect_points[2][1], self.intersect_points[3][1]],
                  [self.intersect_points[4][1], self.intersect_points[0][1], self.intersect_points[5][1]],
                  [self.intersect_points[6][1], self.intersect_points[7][1], self.intersect_points[8][1]]]

            # Put Z intersect points into a 3x3 grid
            zz = [[self.intersect_points[1][2], self.intersect_points[2][2], self.intersect_points[3][2]],
                  [self.intersect_points[4][2], self.intersect_points[0][2], self.intersect_points[5][2]],
                  [self.intersect_points[6][2], self.intersect_points[7][2], self.intersect_points[8][2]]]
            
            # Plot
            #fig = plt.gcf()
            #ax = fig.add_subplot(projection='3d')
            #ax = fig.gca()
            ax.plot_surface(np.array(xx), np.array(yy), np.array(zz), alpha=0.5)

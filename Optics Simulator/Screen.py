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
        print("Screen normal: ", self.normal)

        # Variables for the point where each of the 9 rays will start
        #   In form of [x, y, z] for each point
        #   This is before the screen is rotated into place (centered on XY plane)
        self.intersect_points = np.array([[0, 0, 0], # Center
                                 [-self.width/2, self.height/2, 0], # Top left
                                 [0, self.height/2, 0], # Top middle
                                 [self.width/2, self.height/2, 0], # Top right
                                 [-self.width/2, 0, 0], # Middle left
                                 [self.width/2, 0, 0], # Middle right
                                 [-self.width/2, -self.height/2, 0], # Bottom left
                                 [0, -self.height/2, 0], # Bottom center
                                 [self.width/2, -self.height/2, 0],]) # Bottom right
        
        print("Screen intersection points before rotation: ", self.intersect_points)
        
        # Rotate and translate the screen into place
        for i in range(9):

            # Rotation
            self.intersect_points[i] = np.dot(R2, np.dot(R1, self.intersect_points[i]))

            # Translation
            self.intersect_points[i] += [self.x, self.y, self.z]

        print("Screen intersection points after transformation: ", self.intersect_points)
      

      # Plot the screen
      def plot_screen(self):

            # Calculate d
            # A plane in point normal form is a*x + b*y + c*z + d = 0
            # d = -(a*x + b*y + c*z) = -point . normal
            center = [self.x, self.y, self.z]
            d = -np.array(center).dot([self.normal[0], self.normal[1], self.normal[2]])

            #xx, yy = np.meshgrid(range(int(self.width)), range(int(self.height)))

            """
            x = self.intersect_points[:, 0]
            y = self.intersect_points[:, 1]
            z = self.intersect_points[:, 2]

            X, Y = np.meshgrid(x, y)
            Z = np.zeros_like(X)

            # Interpolate Z values using nearest neighbor method
            for p in self.intersect_points:
                 x_idx = np.argmin(np.abs(x - p[0]))
                 y_idx = np.argmin(np.abs(y - p[1]))
                 Z[y_idx, x_idx] = p[2]

            print(Z)

            fig = plt.gcf()
            ax = fig.add_subplot(111, projection='3d')
            ax.plot_surface(X, Y, Z, cmap='viridis')

            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            """

            x = self.intersect_points[:, 0]
            y = self.intersect_points[:, 1]

            xx, yy = np.meshgrid(x, y)
            
            # Calculate z
            # z = -(a*x + b*y + d)/c
            z = -(self.normal[0]*xx + self.normal[1]*yy)/self.normal[2]

            # Plot
            fig = plt.gcf()
            ax = fig.add_subplot(projection='3d')
            ax.plot_surface(xx, yy, z)
            
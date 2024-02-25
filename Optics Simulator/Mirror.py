import numpy as np
import math
import matplotlib.pyplot as plt

class Mirror():
    def __init__(self, theta1, theta2, len):
        self.theta1 = theta1 * math.pi / 180
        self.theta2 = theta2 * math.pi / 180
        self.len = len

        # Variables for point defining plane
        self.x = 0
        self.y = 0
        self.z = 0

        # Rotation matrices
        R1 = [[1, 0,                      0                    ],
              [0, math.cos(self.theta1), -math.sin(self.theta1)],
              [0, math.sin(self.theta1),  math.cos(self.theta1)]]

        R2 = [[ math.cos(self.theta2), 0, math.sin(self.theta2)],
              [ 0,               1,    0                       ],
              [-math.sin(self.theta2), 0, math.cos(self.theta2)]]
        
        # Calculate normal vector
        # The unrotated normal vector is the Z-axis
        self.normal = np.dot(R2, np.dot(R1, np.array([0, 0, 1])))
        self.a, self.b, self.c = self.normal
        print("Normal: ", self.normal)

        # Variables for the vector of incidence [a_in b_in c_in]
        self.incident = [0, 0, 0]

        # Variables for vector of reflection [a_out b_out c_out]
        self.reflection = [0, 0, 0]

        # Variables for the point where each of the 9 rays intersect the plane
        #   In form of [x, y, z] for each point
        #   1 2 3
        #   4 0 5
        #   6 7 8
        self.intersect_points = np.array([[0, 0, 0], # Center
                                 [0, 0, 0], # Top left
                                 [0, 0, 0], # Top middle
                                 [0, 0, 0], # Top right
                                 [0, 0, 0], # Middle left
                                 [0, 0, 0], # Middle right
                                 [0, 0, 0], # Bottom left
                                 [0, 0, 0], # Bottom center
                                 [0, 0, 0],]) # Bottom right

    # Set the incident vector from the previous mirror coming into the current mirror
    def set_incident_vector(self, a, b, c):
        self.incident = [a, b, c]
        print("Incident: ", self.incident)

    # Calculate the reflection vector
    def calc_reflection_vector(self):

        # Reflection vector
        self.reflection = self.incident - 2*(np.dot(self.incident, self.normal))*self.normal
        print("Reflection: ", self.reflection)

    # Assign the plane's center point given a start point and using the incident vector and len
    def set_center_point(self, x0, y0, z0):

        # Calculate deltas
        delta_x = self.len*self.incident[0]
        delta_y = self.len*self.incident[1]
        delta_z = self.len*self.incident[2]

        # Calculate end point coordinates
        self.x = delta_x + x0
        self.y = delta_y + y0
        self.z = delta_z + z0
        print("Center point: ", [self.x, self.y, self.z])

    # Calculate the intersection points of the plane
    def calc_intersect_points(self, points):

        # Loop through for each of the plane's intersect points
        for i in range(len(points)):

            # Get the current start point
            r0 = points[i]

            # Calculate d
            # A plane in point normal form is a*x + b*y + c*z + d = 0
            # d = -(a*x + b*y + c*z) = -point . normal
            center = [self.x, self.y, self.z]
            d = -np.array(center).dot([self.a, self.b, self.c])

            # Calculate t from p0, normal, and center point
            # Plane in form a*x + b*y + c*z + d = 0 where (x0, y0, z0) is a point on the plane
            #   # Here, this point is the center point of the plane (x, y, z), and [a b c] is the plane's normal vector
            # Line is in form r = r0 + t*v where r0 is a point on the line and v is the vector of the line [vx vy vz]
            #   Here, v is the incident vector from the previous mirror coming into the current mirror
            #   Here, r0 = (r0x, r0y, r0z) is the starting point of the incident ray to this mirror
            # t = (-d - a*r0x - b*r0y - c*r0z) / (a*vx + b*vy + c*vz)
            t = (-d - self.a*r0[0] - self.b*r0[1] - self.c*r0[2]) / (self.a*self.incident[0] + self.b*self.incident[1] + self.c*self.incident[2])
            print("t: ", t)

            # Calculate points of intersection
            self.intersect_points[i][0] = r0[0] + t*self.incident[0]
            self.intersect_points[i][1] = r0[1] + t*self.incident[1]
            self.intersect_points[i][2] = r0[2] + t*self.incident[2]

    # Plot the mirror and incident rays from the previous mirror
    def plot_mirror(self, start_points, ax):

        # Loop through each start point and intersection points of the plane
        for i in range(len(start_points)):

            # Get the current start point
            r0 = start_points[i]

            # Get current intersection point
            r = self.intersect_points[i]

            # Plot ray
            plt.plot([r0[0], r[0]], [r0[1], r[1]], [r0[2], r[2]])
            print("r0: ", r0, "     r: ", r)

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
            
        # Plot mirror
        ax.plot_surface(np.array(xx), np.array(yy), np.array(zz), alpha=0.5)
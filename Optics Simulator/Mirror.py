import numpy as np
import math

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
        self.a, self.b, self.c = np.dot(R2, np.dot(R1, np.array([0, 0, 1])))

        # Variables for the vector of incidence [a_in b_in c_in]
        self.incident = [0, 0, 0]

        # Variables for vector of reflection [a_out b_out c_out]
        self.reflection = [0, 0, 0]

        # Variables for the point where each of the 9 rays intersect the plane
        #   In form of [x, y, z] for each point
        self.intersect_points = [[0, 0, 0], # Center
                                 [0, 0, 0], # Top left
                                 [0, 0, 0], # Top middle
                                 [0, 0, 0], # Top right
                                 [0, 0, 0], # Middle left
                                 [0, 0, 0], # Middle right
                                 [0, 0, 0], # Bottom left
                                 [0, 0, 0], # Bottom center
                                 [0, 0, 0],] # Bottom right

    # Set the incident vector from the previous mirror coming into the current mirror
    def set_incident_vector(self, a, b, c):
        self.incident = [a, b, c]

    # Calculate the reflection vector
    def calc_reflection_vector(self):

        # Normal vector
        normal = [self.x, self.y, self.z]

        # Reflection vector
        self.reflection = self.incident - 2*(np.dot(self.incident, normal))*normal

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

    # Calculate the intersection points of the plane
    def calc_intersect_points(self, points):

        # Loop through for each of the plane's intersect points
        for i in range(len(points)):

            # Get the current start point
            p0 = points[i]

            # Calculate d
            # A plane in point normal form is a*x + b*y + c*z + d = 0
            # d = -(a*x + b*y + c*z) = -point . normal
            center = [self.x, self.y, self.z]
            d = -center.dot(self.incident)

            # Calculate t from p0, normal, and center point
            # Plane in form a*x + b*y + c*z + d = 0 where (x0, y0, z0) is a point on the plane
            # Line is in form r = r0 + t*v where r0 is a point on the line and v is the vector of the line
            t = (d - )
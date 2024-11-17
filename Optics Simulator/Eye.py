import numpy as np
import math
import matplotlib.pyplot as plt

class Eye():
    def __init__(self, x, y, z, radius):
        self.x = x
        self.y = y
        self.z = z
        self.radius = radius

        # Plane variables for frame to act as a mirror
        self.normal  = self.a, self.b, self.c = np.array([0, 1, 0]) # Normal vector set as the +Y axis

        # Variables for the vector of incidence [a_in b_in c_in]
        self.incident = [0, 0, 0]

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
        
        # Variable for how many of the intersect points actually are on the eye
        self.success = 0
        
    # Set the incident vector from the previous mirror coming into the current mirror
    def set_incident_vector(self, a, b, c):
        self.incident = [a, b, c]
        #print("Incident: ", self.incident)

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
            #print("t: ", t)

            # Calculate points of intersection
            self.intersect_points[i][0] = r0[0] + t*self.incident[0]
            self.intersect_points[i][1] = r0[1] + t*self.incident[1]
            self.intersect_points[i][2] = r0[2] + t*self.incident[2]

    def plot_eye(self, start_points):

        # Calculate corners of eye rectangle from the perspective of the person wearing them
        tl = [self.x - self.radius, self.y, self.z + self.radius]
        tr = [self.x + self.radius, self.y, self.z + self.radius]
        br = [self.x + self.radius, self.y, self.z - self.radius]
        bl = [self.x - self.radius, self.y, self.z - self.radius]

        # Plot the eye as a rectangle
        plt.plot([tl[0], tr[0]], [tl[1], tr[1]], [tl[2], tr[2]], color="black") # tl to tr
        plt.plot([tr[0], br[0]], [tr[1], br[1]], [tr[2], br[2]], color="black") # tr to br
        plt.plot([br[0], bl[0]], [br[1], bl[1]], [br[2], bl[2]], color="black") # br to bl
        plt.plot([bl[0], tl[0]], [bl[1], tl[1]], [bl[2], tl[2]], color="black") # bl to tl

        # Loop through each start point and intersection points of the plane
        for i in range(len(start_points)):

            # Get the current start point
            r0 = start_points[i]

            # Get current intersection point
            r = self.intersect_points[i]

            # Plot ray
            #plt.plot([r0[0], r[0]], [r0[1], r[1]], [r0[2], r[2]])
            #print("r0: ", r0, "     r: ", r)

            # Determine if the current intersect point is actually on the eye
            if r[0] >= self.x - self.radius and r[0] <= self.x + self.radius:
                if r[2] >= self.z - self.radius and r[2] <= self.z + self.radius:
                    
                    plt.plot([r0[0], r[0]], [r0[1], r[1]], [r0[2], r[2]])
                    self.success += 1

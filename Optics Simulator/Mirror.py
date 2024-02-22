import math

class Mirror():
    def __init__(self, theta1, theta2, len):
        self.theta1 = theta1 * math.pi / 180
        self.theta2 = theta2 * math.pi / 180
        self.len = len

        # Variables for point defining plane
        self.a = 0
        self.b = 0
        self.c = 0

        # Variables for normal vector defining plane
        self.x = 0
        self.y = 0
        self.z = 0

        # Variables for the vector of incidence [a_in b_in c_in]
        self.incident = [0, 0, 0]

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
    def set_incident(self, a, b, c):
        self.incident = [a, b, c]
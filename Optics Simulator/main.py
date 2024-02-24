import numpy as np
import math
import matplotlib.pyplot as plt
from Mirror import Mirror
from Screen import Screen
from Glasses import Glasses

# ________________________________________________________________________
''' INPUT VARIABLES VARIABLES '''
FILENAME = "parameters.txt"

# ________________________________________________________________________
''' SCREEN VARIABLES '''
# Define screen size in mm
SCREEN_WIDTH = None
SCREEN_HEIGHT = None

# Define screen position in mm from center of bridge to center of screen
# X-direction defined as left (-) to right (+)
# Y-direction defined as back (-) to front (+)
# Z-direction defined as down (-) to up(+)
#
# These directions are the same as defined in CAD
SCREEN_X = None
SCREEN_Y = None
SCREEN_Z = None
SCREEN_THETA1 = None
SCREEN_THETA2 = None

# ________________________________________________________________________
''' MIRROR VARIABLES '''

# Define mirror array
mirrors = []

# Define mirrors
# mirror = [theta1, theta2, len]
#
# Mirror orientation is defined by its normal vector. Since the plane of each mirror may
# not pass through the origin, its normal vector is defined as the vector normal to some
# point on the plane starting at the origin
#
# The normal vector starts as the +Z axis (0,0,1), the mirror being the XY plane, and can be rotated from two planes:
#   theta1 = angle of rotation between normal vector and ZX plane (+ = CCW, - = CW)
#   theta2 = angle of rotation between normal vector and YZ plane (+ = CCW, - = CW)
#
# Length is defined as the distance from the center of mirror n-1 to the center of mirror n
#   Length vector is perpendicular to mirror n-1
#

m1_t1 = -45 * math.pi / 180
m1_t2 = 0 * math.pi / 180
m1_len = 60

m2_t1 = 0 * math.pi / 180
m2_t2 = 135 * math.pi / 180
m2_len = 40

m3_t1 = -90 * math.pi / 180
m3_t2 = 45 * math.pi / 180
m3_len = 20

# ________________________________________________________________________
''' GLASSES VARIABLES '''

# Glasses = [frame_x, frame_z, frame_width, frame_height, temple_z, temple_len]

# Frame location, width, and height
#     X, Y, and Z are defined at center
#     Frame will be defined as a rectangle that lays on the ZX plane in the +X, +Z quadrant
#           This means that frame_y = 0
FRAME_X = None
FRAME_Z = None
FRAME_WIDTH = None
FRAME_HEIGHT = None

# Glasses temple location and length
#     X, Y, and Z are defined at the hinge between temple and frame
#           This means that temple_X = frame_x + frame_width/2 and temple_y = 0
#     Temple will be defined as a line parallel to the Y axis that lays in the +X, +Z quadrant
TEMPLE_Z = None
TEMPLE_LEN = None




def main():

      # ________________________________________________________________________
      # Open parameter file
      paramFile = open(FILENAME)

      # Load parameters from file
      for line in paramFile:

            # If the line does not start with a '#' or '\n'
            if line[0] != '#' and line[0] != '\n':
                  #print(line)
                  # Remove any spaces from the line, in case the user entered them
                  line = line.replace(" ", "")

                  # Separate the variable name from the value
                  name, value = line.split('=')

                  # Determine what parameter we are working with

                  # Screen parameters
                  if name == "screen_width":
                        SCREEN_WIDTH = float(value)
                        
                  elif name == "screen_height":
                        SCREEN_HEIGHT = float(value)

                  elif name == "screen_x":
                        SCREEN_X = float(value)

                  elif name == "screen_y":
                        SCREEN_Y = float(value)

                  elif name == "screen_z":
                        SCREEN_Z = float(value)

                  elif name == "screen_theta1":
                        SCREEN_THETA1 = float(value)

                  elif name == "screen_theta2":
                        SCREEN_THETA2 = float(value)
                        

                  # Glasses parameters
                  elif name == "frame_x":
                        FRAME_X = float(value)

                  elif name == "frame_z":
                        FRAME_Z = float(value)

                  elif name == "frame_width":
                        FRAME_WIDTH = float(value)

                  elif name == "frame_height":
                        FRAME_HEIGHT = float(value)

                  elif name == "temple_z":
                        TEMPLE_Z = float(value)

                  elif name == "temple_len":
                        TEMPLE_LEN = float(value)

                  # Mirror parameters
                  elif "mirror" in name:
                        
                        # Split up the three mirror parameters
                        t1, t2, l = value.split(',')

                        # Create a new mirror
                        mirror = Mirror(float(t1), float(t2), float(l))

                        # Add the mirror to the mirrors array
                        mirrors.append(mirror)

                  # If there is an unknown parameter read (typo in parameters file)
                  else:
                        print("ERROR: Unknown name in parameter file: " + name)
                        exit(1)

      # Create the screen
      screen = Screen(SCREEN_THETA1, SCREEN_THETA2, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_X, SCREEN_Y, SCREEN_Z)

      # Create the glasses
      glasses = Glasses(FRAME_X, FRAME_Z, FRAME_WIDTH, FRAME_HEIGHT, TEMPLE_Z, TEMPLE_LEN)

      # Set up plot
      fig = plt.figure()
      ax = fig.add_subplot(projection='3d')
      ax.set_xlabel('X')
      ax.set_ylabel('Y')
      ax.set_zlabel('Z')

      # Plot screen
      screen.plot_screen()

      # Loop through each mirror
      for i in range(len(mirrors)):

            # Get current mirror
            m = mirrors[i]

            # Get the incident vector of the previous mirror/screen

            # If i = 0, then we need to get the incident vector from the screen, which is
            # just the screen's normal vector
            if i == 0:

                  # Set incident vector from screen
                  m.set_incident_vector(screen.normal[0], screen.normal[1], screen.normal[2])

                  # Calculate reflection vector from screen
                  m.calc_reflection_vector()

                  # Set point of current plane from screen
                  m.set_center_point(screen.x, screen.y, screen.z)

                  # Calculate the intersection points from screen to first mirror
                  m.calc_intersect_points(screen.intersect_points)

                  # Plot the current plane and rays going into this plane
                  m.plot_mirror(screen.intersect_points)


            # If i != 0, then we need to get the incident vector from the previous mirror
            else:

                  # Get previous mirror
                  mm1 = mirrors[i-1]

                  # Set incident vector from previous mirror
                  mm1.set_incident_vector(mm1.normal[0], mm1.normal[1], mm1.normal[2])

                  # Calculate reflection vector from previous mirror
                  mm1.calc_reflection_vector()

                  # Set point of current plane from previous mirror
                  mm1.set_center_point(mm1.x, mm1.y, mm1.z)

                  # Calculate the intersection points from previous mirror to current mirror
                  mm1.calc_intersect_points(mm1.intersect_points)

                  # Plot the current plane and rays going into this plane

      """
      # ________________________________________________________________________
      # Plot mirror 1
      R1 = [[1, 0,                0              ],
            [0, math.cos(m1_t1), -math.sin(m1_t1)],
            [0, math.sin(m1_t1),  math.cos(m1_t1)]]

      R2 = [[ math.cos(m1_t2), 0, math.sin(m1_t2)],
            [ 0,               1, 0              ],
            [-math.sin(m1_t2), 0, math.cos(m1_t2)]]

      #n1 = R2*R1*np.array([0, 0, 1])
      n1 = np.dot(R2, np.dot(R1, np.array([0, 0, 1])))

      # Plot planes
      # Point = (x, y, z)
      # Normal = [a b c]
      point = np.array([SCREEN_X, SCREEN_Y + m1_len, SCREEN_Z])
      normal = np.array(n1)

      # A plane in point normal form is a*x + b*y + c*z + d = 0
      # d = -(a*x + b*y + c*z) = -point . normal
      d = -point.dot(normal)

      xx, yy = np.meshgrid(range(10), range(10))

      # Calculate z
      # z = -(a*x + b*y + d)/c
      z = -(normal[0]*xx + normal[1]*yy)/normal[2]

      # Plot
      fig = plt.figure()
      ax = fig.add_subplot(projection='3d')
      ax.plot_surface(xx, yy, z)
      plt.show()
      """

      plt.show()

      """
      Steps:

      1. From .txt file, get screen size, and position of center (the screen is just another mirror/plane)
      2. Define starting points on the screen for each of the 9 light rays (in screen object)
      3. For each plane:
            a. Calculate rotation matrices to then find normal vector from theta1 and theta2 (in Mirror object)
            b. Get the direction of the rays coming from the n-1th plane
            c. Calculate the end point of the center ray using the n-1th mirror's center point and the nth mirror's len
            d. Use the point and normal vector to define the plane (update mirror's parameters)
            e. For each ray:
                  i. Find where the ray from the n-1th mirror intersects the nth mirror/plane
                  ii. Update the corresponding intersection point (x, y, z) for the current mirror
            f. Using the center ray from the n-1th mirror to the nth mirror, determine the new direction of the reflected ray
            g. Plot the nth mirror and the 9 rays going from the n-1th mirror to the nth mirror


      """
main()
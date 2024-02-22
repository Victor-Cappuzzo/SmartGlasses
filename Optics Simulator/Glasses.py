class Glasses():

    def __init__(self, frame_x, frame_z, frame_width, frame_height, temple_z, temple_len):

        # Frame variables
        self.frame_x = frame_x
        self.frame_y = 0
        self.frame_z = frame_z
        self.frame_width = frame_width
        self.frame_height = frame_height

        # Temple variables
        self.temple_x = self.frame_x + self.frame_width/2
        self.temple_y = 0
        self.temple_z = temple_z
        self.temple_len = temple_len


class Gondola:
    def __init__(self, length, height, x, z):
        """
        Gondola parametric object
        :param payload_mass: [float] payload mass carried [kg]
        :param length:
        :param height:
        :param x:
        :param z:
        """
        self.length = length
        self.height = height
        self.x_cg = length / 2
        self.z_cg = height / 2
        self.x = x
        self.z = z




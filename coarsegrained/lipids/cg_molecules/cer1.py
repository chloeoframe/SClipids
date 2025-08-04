import mbuild as mb
import numpy as np

class Cer1(mb.Compound):
    def __init__(self):
        """Returns a CG uCER1 with the head-to-tail vector pointing in -z.
        """
        super(Cer1, self).__init__()
        mb.load('cer1.hoomdxml', compound=self, relative_to_module=self.__module__)
        self.periodicity = [0, 0, 0]
        xx = list(self.particles())
        mb.coordinate_transform.z_axis_transform(self,
                new_origin=xx[18], point_on_z_axis=xx[24])
        self.translate([-self.center[0], -self.center[1], 0])  # center in xy plane
        self.masses = [0.403639, 0.584458, 0.555982, 0.555982, 0.584458, 0.584458, 0.610727,
                        0.389305, 0.584458, 0.584458, 0.584458, 0.584458, 0.584458,
                        0.584458, 0.584458, 0.584458, 0.584458, 0.597575, 0.556458,
                        0.584458, 0.584458, 0.584458, 0.584458, 0.584458, 0.236214,
                        0.236214]
        self.mass = np.sum(self.masses)
        self.rotate(np.pi, [1, 0, 0])


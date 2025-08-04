import mbuild as mb
import numpy as np

class Cer2_16(mb.Compound):
    def __init__(self):
        """Returns a CG CER2 with 16c FA tail with the head-to-tail vector pointing in -z.
        """
        super(Cer2_16, self).__init__()
        mb.load('cer2-16.hoomdxml', compound=self, relative_to_module=self.__module__)
        self.periodicity = [0, 0, 0]
        xx = list(self.particles())
        mb.coordinate_transform.z_axis_transform(self,
                new_origin=xx[6], point_on_z_axis=xx[11])
        self.masses = [0.598458, 0.584458, 0.584458, 0.584458, 0.584458, 0.597575,
                        0.556458, 0.556458, 0.584458, 0.584458, 0.584458, 0.598458,
                        0.236214, 0.236214]
        self.mass = np.sum(self.masses)
        self.rotate(np.pi, [1, 0, 0])

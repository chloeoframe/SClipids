import mbuild as mb
import numpy as np

class Ester(mb.Compound):
    def __init__(self):
        """Returns a CG ester with the head-to-tail vector pointing in -z.
        """
        super(Ester, self).__init__()
        mb.load('ester.hoomdxml', compound=self, relative_to_module=self.__module__)
        self.periodicity = [0, 0, 0]
        xx = list(self.particles())
        self.translate_to([2.5/6/2]*3)  # center in xy plane
        self.masses = [0.598458, 0.610727, 0.598458]
        self.mass = np.sum(self.masses)
        self.rotate(np.pi, [1, 0, 0])


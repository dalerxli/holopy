# Copyright 2011-2016, Vinothan N. Manoharan, Thomas G. Dimiduk,
# Rebecca W. Perry, Jerome Fung, Ryan McGorty, Anna Wang, Solomon Barkley
#
# This file is part of HoloPy.
#
# HoloPy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# HoloPy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with HoloPy.  If not, see <http://www.gnu.org/licenses/>.

'''
Defines ellipsoidal scatterers.

.. moduleauthor:: Thomas G. Dimiduk <tdimiduk@physics.harvard.edu>
'''


import numpy as np

from .scatterer import CenteredScatterer, Indicators
from ..errors import InvalidScatterer
from functools import reduce

def isnumber(x):
    try:
        x + 1
        return True
    except TypeError:
        return False

def all_numbers(x):
    return reduce(lambda rest, i: isnumber(i) and rest, x, True)


class Ellipsoid(CenteredScatterer):
    """
    Scattering object representing ellipsoidal scatterers

    Parameters
    ----------
    n : complex
        Index of refraction
    r : float or (float, float, float)
        x, y, z semi-axes of the ellipsoid
    center : 3-tuple, list or numpy array
        specifies coordinates of center of the scatterer
    rotation : 3-tuple, list or numpy.array
        specifies the Euler angles (alpha, beta, gamma) in radians 
        defined in a-dda manual section 8.1
    """

    def __init__(self, n=None, r=None, center=None,rotation=(0,0,0)):
        self.n = n

        if np.isscalar(r) or len(r) != 3:
            raise InvalidScatterer(self,"r specified as {0}; "
                                           "r should be "
                                           "specified as (r_x, r_y, r_z)"
                                           "".format(center))

        self.r = r

        if np.isscalar(rotation) or len(rotation) != 3:
            raise InvalidScatterer(self,"rotation specified as {0}; "
                                           "rotation should be "
                                           "specified as (alpha, beta, gamma)"
                                           "".format(rotation))
        self.rotation = rotation
        super(Ellipsoid, self).__init__(center)

    @property
    def indicators(self):
        """
        NOTE: Ellipsoid indicators does not currently apply rotations
        """
        return Indicators(lambda point: ((point / self.r) ** 2).sum(-1) < 1,
                          [[-self.r[0], self.r[0]], [-self.r[1], self.r[1]],
                            [-self.r[2], self.r[2]]])


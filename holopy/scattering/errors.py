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
"""
Exceptions used in scatterpy module.  These are separated out from the
other exceptions in other parts of HoloPy to keep things modular.

.. moduleauthor :: Vinothan N. Manoharan <vnm@seas.harvard.edu>
"""


import warnings

class NoScattering(ImportWarning):
    def __init__(self, theory):
        self.theory = theory
    def __str__(self):
        return "Could not import "+self.theory+" scattering theory. You will not be able to do scattering calculations but the rest of HoloPy should remain usable. This is probably due to a problem with compiling Fortran code."


class InvalidScatterer(Exception):
    def __init__(self, scatterer, message):
        self.scatterer = scatterer
        super(InvalidScatterer, self).__init__(
            "Invalid scatterer of type " +
            self.scatterer.__class__.__name__ +
            ".\n" + message)

class OverlapWarning(UserWarning):
    def __init__(self, scatterer, overlaps):
        self.scatterer = scatterer
        self.overlaps = overlaps
    def __str__(self):
        return "{0} has overlaps between spheres: {1}".format(repr(self.scatterer),
                                                              self.overlaps)
warnings.simplefilter('always', OverlapWarning)

class TheoryNotCompatibleError(Exception):
    def __init__(self, theory, scatterer, reason=None):
        self.theory = theory
        self.scatterer = scatterer
        message = (self.theory.__class__.__name__ +
                   " scattering theory can't handle scatterers of type " +
                    self.scatterer.__class__.__name__)
        if reason is not None:
            message += " because: " + message
        super(TheoryNotCompatibleError, self).__init__(message)

class MissingParameter(Exception):
    def __init__(self, parameter_name):
        self.parameter_name = parameter_name
    def __str__(self):
        return ("Calculation requires specification of " + self.parameter_name + ".")

class MultisphereFailure(Exception):
    def __str__(self):
        return ("Multisphere calculations failed to converge, or returned NaN. this probably means "
                "your scatterer is unphysical.")

class TmatrixFailure(Exception):
    def __init__(self, logfilestr):
            self.logfilestr = logfilestr
    def __str__(self):
        with open(self.logfilestr) as logfile:
            reason=list(logfile)[-1]
        return("Tmatrix calculation failed. This might be because your scatterer's size or aspect ratio is too large for default parameters. \n Tmatrix error message: " + reason + "Full details are available in " + self.logfilestr)

class DependencyMissing(Exception):
    def __init__(self, dep):
        self.dep = dep
    def __str__(self):
        return("External Dependency: " + self.dep + " could not be found, terminating.")

class AutoTheoryFailed(Exception):
    def __init__(self, scatterer):
        self.scatterer = scatterer

    def __str__(self):
        return ("Could not automatically determine a theory to compute scattering from scatterer: {}. You will have to manually specify a theory (or submit a bug if you think we should be able to tell what theory you need). ".format(self.scatterer))

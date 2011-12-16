# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#

class Package:
    """
    Meta data for external dependencies
    """
    name = None
    environ = None
    optional = False

    def __init__(self, name, optional):
        self.name = name
        self.optional = optional
        return


def requirements():
    """
    Build a dictionary with the external dependencies of the {pyre} project
    """

    # build the package instances
    gsl = Package(name='gsl', optional=False)
    libpq = Package(name='libpq', optional=True)
    mpi = Package(name='mpi', optional=True)
    python = Package(name='python', optional=False)
    # attach
    packages = { package.name: package for package in (gsl, libpq, mpi, python) }
    # and return
    return packages


# end of file 

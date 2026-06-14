# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A sandbox for exploring write-capable {pyre.h5} schemas using a small, growing
subset of the NISAR data products as the proving ground
"""


# import and publish select pyre symbols
from  pyre import (
    # the manager of the pyre runtime
    executive,
    # value constraints
    constraints,
    # hdf5 support
    h5
)

# register the package with the framework
package = executive.registerPackage(name="nisar", file=__file__)
# save the geography
home, prefix, defaults = package.layout()

# the package meta-data
from . import meta


# administrivia
def copyright():
    """
    Return the copyright note
    """
    # pull and print the meta-data
    return print(meta.header)


def license():
    """
    Print the license
    """
    # pull and print the meta-data
    return print(meta.license)


def built():
    """
    Return the build timestamp
    """
    # pull and return the meta-data
    return meta.date


def credits():
    """
    Print the acknowledgments
    """
    # pull and print the meta-data
    return print(meta.acknowledgments)


def version():
    """
    Return the version
    """
    # pull and return the meta-data
    return meta.version


# end of file

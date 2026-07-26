# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclasses
from .Library import Library
from .LibraryInstallation import LibraryInstallation

# the flavor description
from .Recipe import Recipe


# the fftw package category
class FFTW(Library, family="pyre.externals.fftw"):
    """
    The fastest Fourier transform in the west
    """

    # constants
    category = "fftw"

    # interface
    @classmethod
    def recipes(cls):
        """
        Generate the sequence of recipes for my known flavors
        """
        # there is only one flavor
        yield Recipe(
            # of this category
            category=cls.category,
            # realized by the generic installation
            factory=Default,
            # provable by the top level header
            headers=("fftw3.h",),
            # contributing this library to the link line
            libraries=("fftw3",),
            # and this marker to the compile line
            defines=("WITH_FFTW",),
            # with database specific names where the category name isn't enough
            natives={
                "dpkg": ("libfftw3-dev",),
                "macports": ("fftw-3",),
                "rpm": ("fftw-devel",),
            },
        )
        # all done
        return


# the implementation
class Default(LibraryInstallation, family="pyre.externals.fftw.default", implements=FFTW):
    """
    A generic FFTW installation
    """

    # constants
    category = FFTW.category
    flavor = category


# end of file

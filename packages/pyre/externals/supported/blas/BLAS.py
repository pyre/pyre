# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclasses
from ...Library import Library

# the flavor description
from ...Recipe import Recipe


# the blas package category
class BLAS(Library, family="pyre.externals.blas"):
    """
    The basic linear algebra subroutines
    """

    # constants
    category = "blas"

    # interface
    @classmethod
    def recipes(cls):
        """
        Generate the sequence of recipes for my known flavors, in order of preference
        """
        # get the implementations
        from .OpenBLAS import OpenBLAS
        from .Atlas import Atlas
        from .GSLCBLAS import GSLCBLAS

        # openblas
        yield Recipe(
            # of this category
            category=cls.category,
            # the flavor tag
            flavor="openblas",
            # realized by the openblas installation
            factory=OpenBLAS,
            # provable by the cblas interface header
            headers=("cblas.h",),
            # contributing this library to the link line
            libraries=("openblas",),
            # and this marker to the compile line
            defines=("WITH_OPENBLAS",),
            # with database specific names where the flavor name isn't enough
            natives={
                "conda": ("openblas", "libopenblas"),
                "dpkg": ("libopenblas-dev",),
                "macports": ("OpenBLAS", "openblas"),
                "rpm": ("openblas-devel",),
            },
        )
        # atlas
        yield Recipe(
            # of this category
            category=cls.category,
            # the flavor tag
            flavor="atlas",
            # realized by the atlas installation
            factory=Atlas,
            # provable by the cblas interface header
            headers=("cblas.h",),
            # contributing these libraries to the link line
            libraries=("cblas", "atlas"),
            # and this marker to the compile line
            defines=("WITH_ATLAS",),
            # with database specific names where the flavor name isn't enough
            natives={"dpkg": ("libatlas-base-dev",)},
        )
        # the gsl cblas fallback
        yield Recipe(
            # of this category
            category=cls.category,
            # the flavor tag
            flavor="gslcblas",
            # realized by the gsl cblas installation
            factory=GSLCBLAS,
            # provable by the gsl flavor of the cblas interface header
            headers=("gsl/gsl_cblas.h",),
            # contributing this library to the link line
            libraries=("gslcblas",),
            # and this marker to the compile line
            defines=("WITH_GSLCBLAS",),
            # with database specific names where the flavor name isn't enough
            natives={
                "conda": ("gsl",),
                "dpkg": ("libgsl-dev",),
                "macports": ("gsl",),
            },
        )
        # all done
        return


# end of file

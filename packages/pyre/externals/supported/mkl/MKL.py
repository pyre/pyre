# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclasses
from ...Library import Library

# the flavor description
from ...Recipe import Recipe


# the mkl package category
class MKL(Library, family="pyre.externals.mkl"):
    """
    The intel math kernel library
    """

    # constants
    category = "mkl"

    # interface
    @classmethod
    def recipes(cls):
        """
        Generate the sequence of recipes for my known flavors

        Conda splits the headers into {mkl-include}, so it rides along as a companion;
        oneAPI installations live under nonstandard roots like {/opt/intel/oneapi/mkl},
        which the bare engine reaches through its search path
        """
        # get the implementations
        from .Default import Default

        # there is only one flavor
        yield Recipe(
            # of this category
            category=cls.category,
            # realized by the generic installation
            factory=Default,
            # provable by the umbrella header
            headers=("mkl.h",),
            # the single dynamic runtime is the sane default link line; users who want
            # the explicit interface/threading/core triple override {libraries}
            libraries=("mkl_rt",),
            # the marker for the compile line
            defines=("WITH_MKL",),
            # with database specific names where the category name isn't enough
            natives={
                # conda: the libraries lead, the headers ride along
                "conda": (("mkl", "mkl-include"),),
                # debian carries mkl in non-free
                "dpkg": ("libmkl-dev",),
            },
        )
        # all done
        return


# end of file

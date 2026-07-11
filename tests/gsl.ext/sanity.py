#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Sanity check: the {libgsl} bindings load and publish the expected classes, enumerations, and
free functions, without the {gsl} package shim in the way
"""


def test():
    # the bindings, straight from the extension
    from gsl import libgsl

    # the bound data types
    for name in ["Vector", "Matrix", "RNG", "Permutation", "Histogram"]:
        # each is a class the extension defines
        assert isinstance(getattr(libgsl, name), type)

    # the flag enumerations
    for name in ["Transpose", "Triangle", "Diagonal", "Side", "EigenOrder"]:
        # each is present
        assert hasattr(libgsl, name)

    # a sample of the free functions the modules publish
    for name in [
        "blas_ddot",
        "stats_correlation",
        "linalg_LU_decomp",
        "uniform_sample",
        "rng_avail",
    ]:
        # each is callable
        assert callable(getattr(libgsl, name))

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file

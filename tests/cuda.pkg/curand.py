#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
The curand bindings fill grids with draws from the requested distributions, in both precisions
"""


def test():
    # support
    import numpy
    import pyre.cuda

    # the bindings
    curand = pyre.cuda.curand
    # a generator
    generator = curand.create_generator(curand.RngType.DEFAULT)
    # with a fixed seed
    curand.set_seed(generator, 2026)
    # for each precision
    for suffix, cell in (("_double", "float64"), ("", "float32")):
        # draws from the uniform distribution
        uniform = pyre.cuda.managed(shape=(1000,), cell=cell)
        getattr(curand, "generate_uniform" + suffix)(generator, uniform, 1000)
        # land in its range
        values = numpy.asarray(uniform)
        assert values.min() > 0 and values.max() <= 1
        # draws from the normal distribution
        normal = pyre.cuda.managed(shape=(10000,), cell=cell)
        getattr(curand, "generate_normal" + suffix)(generator, normal, 10000, 0.0, 1.0)
        # have its moments
        values = numpy.asarray(normal)
        assert abs(values.mean()) < 0.1 and abs(values.std() - 1) < 0.1
    # release the generator
    curand.destroy_generator(generator)

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file

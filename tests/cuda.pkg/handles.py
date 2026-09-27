#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
A device makes its library handles once, and hands back the same ones after that
"""


def test():
    # access the package
    import pyre.cuda

    # the first device
    device = pyre.cuda.manager.devices[0]
    # hands back the same cublas handle every time
    assert device.cublasHandle == device.cublasHandle
    # and the same cusolver handle
    assert device.cusolverHandle == device.cusolverHandle
    # and the same curand generator
    assert device.curandGenerator() == device.curandGenerator()

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file

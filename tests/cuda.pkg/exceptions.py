#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
The exceptions of a missing capability are import errors that name what is missing
"""


def test():
    # access the package
    import pyre.cuda

    # a client that guards its import catches them as import errors
    assert issubclass(pyre.cuda.ExtensionNotFoundError, ImportError)
    assert issubclass(pyre.cuda.CudaPythonNotFoundError, ImportError)
    # and they say what is missing
    assert "extension" in str(pyre.cuda.ExtensionNotFoundError())
    assert "cuda-python" in str(pyre.cuda.CudaPythonNotFoundError())

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file

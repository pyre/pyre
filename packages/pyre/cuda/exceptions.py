# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Definitions for all exceptions raised by this package
"""

# framework
import pyre


class Error(pyre.PyreError):
    """
    Exception raised when the cuda support layer detects an error
    """

    # public data
    description = "cuda error"


class ExtensionNotFoundError(Error, ImportError):
    """
    Exception raised when the cuda extension of pyre is not installed, because pyre was built
    without cuda
    """

    # public data
    description = "pyre.cuda: the cuda extension is not installed; pyre was built without cuda"


class CudaPythonNotFoundError(Error, ImportError):
    """
    Exception raised when cuda-python, which the package uses to reach the devices, is not
    installed
    """

    # public data
    description = "pyre.cuda: cuda-python is not installed; get it with 'pip install cuda-python'"


# end of file

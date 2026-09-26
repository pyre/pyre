# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Support for cuda capable devices

The cuda extension of pyre is loaded here, and only here, so that importing pyre never touches
cuda; a machine without the extension or without cuda-python gets an exception that says which
"""

# the exceptions
from .exceptions import Error, ExtensionNotFoundError, CudaPythonNotFoundError

# the extension
try:
    # is installed with the rest of the bindings
    from ..extensions import cuda as libcuda
# when it is not there
except ImportError as error:
    # say so
    raise ExtensionNotFoundError() from error

# cuda-python, which reaches the devices
try:
    # its runtime bindings
    from cuda.bindings import runtime
# when it is not there
except ImportError as error:
    # say so
    raise CudaPythonNotFoundError() from error

# the attached devices
from .DeviceManager import DeviceManager

# the manager of the devices
manager = DeviceManager()

# the class of grids whose cells live in managed memory
grid = libcuda.Grid
# the factory that allocates a grid over a fresh block of managed memory
managed = libcuda.managed
# wait for the work queued on the device
synchronize = libcuda.synchronize


# end of file

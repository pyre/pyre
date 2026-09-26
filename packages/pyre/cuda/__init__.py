# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# my meta-data
from . import meta

# the administrivia
version = meta.version
copyright = meta.copyright


def license():
    print(meta.license)


# get the exceptions
from .exceptions import Error

# pull in pyre so we can reach the bindings
import pyre

# thin bindings for cublas, cusolver, and curand, operating on {pyre.grid} grids; only
# present when the extension was built with {WITH_CUDA}
if pyre.libpyre is None or not hasattr(pyre.libpyre, "cuda"):
    # without the bindings there is nothing to publish
    cublas = None
    cusolver = None
    curand = None
else:
    # reach into the bindings by attribute, the way the rest of pyre does
    cublas = pyre.libpyre.cuda.cublas
    cusolver = pyre.libpyre.cuda.cusolver
    curand = pyre.libpyre.cuda.curand


# build the device manager; nvidia's own cuda-python bindings raise if there is no cuda
# capable hardware or driver on this machine, exactly as the old hand rolled extension used to
# fail to load, so degrade to no devices rather than making the whole package unusable
try:
    # attempt to
    from .DeviceManager import DeviceManager

    manager = DeviceManager()
# if anything about that failed
except Exception as error:
    # not much to do...
    import journal

    journal.warning("cuda").log(f"could not find 'cuda' support: {error}")
    # leave the manager unusable but importable
    DeviceManager = None
    manager = None


# end of file

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

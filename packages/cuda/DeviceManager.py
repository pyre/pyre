# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# meta-class
from pyre.patterns.Singleton import Singleton


# declaration
class DeviceManager(metaclass=Singleton):
    """
    The singleton that provides access to what is known about CUDA capable hardware
    """


    # meta-methods
    def __init__(self, extension, **kwds):
        # chain up
        super().__init__(**kwds)

        # grab the device class
        from .Device import Device

        # build the device list and attach it
        self.devices = extension.discover(Device)

        # all done
        return


# end of file

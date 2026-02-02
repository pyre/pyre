# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# leif strand
# (c) 1998-2026 all rights reserved


# declaration
class Port:
    """
    A mechanism that enables peer processes to draw the attention of the process owning the
    port
    """

    # interface
    @classmethod
    def open(cls, address, **kwds):
        """
        Attempt to draw the attention of the peer process at {address}
        """
        raise NotImplementedError(f"class '{cls.__name__}' must implement 'open'")

    @classmethod
    def install(cls, **kwds):
        """
        Install and activate a port. Called by the owning process when it is ready to start
        accepting guests
        """
        raise NotImplementedError(f"class '{cls.__name__}' must implement 'install'")


# end of file

# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the metaclass of channels
class Severity(type):
    """
    The metaclass of channels; it grants class level access to the defaults of a severity, so
    that they can be read and set on the channel class itself
    """

    # the severity wide defaults
    @property
    def defaultActive(cls) -> bool:
        """
        The default activation state of the channels of this severity
        """
        # my index knows
        return cls.index.active

    @property
    def defaultFatal(cls) -> bool:
        """
        The default fatality of the channels of this severity
        """
        # my index knows
        return cls.index.fatal

    @property
    def defaultDevice(cls):
        """
        The default device of the channels of this severity
        """
        # my index knows
        return cls.index.device

    @defaultDevice.setter
    def defaultDevice(cls, device) -> None:
        """
        Make {device} the default device of the channels of this severity
        """
        # hand it to my index
        cls.index.device = device
        # all done
        return


# end of file

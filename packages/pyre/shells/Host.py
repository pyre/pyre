# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# externals
import pyre
import platform


# declaration
class Host(pyre.protocol, family='pyre.hosts'):
    """
    Encapsulation of host specific information
    """


    # public state
    # packages = pyre.catalog(protocol=???)


    # class interface
    @classmethod
    def pyre_default(cls):
        """
        Build the preferred host implementation
        """
        print("Host.default")
        print("    platform: {}".format(platform.uname()))
        return None


    @classmethod
    def pyre_cast(cls, value):
        """
        Convert {value} into a configured host instance
        """
        print("Host.pyre_cast: value={!r}".format(value))
        return super().pyre_cast(value)


# end of file 

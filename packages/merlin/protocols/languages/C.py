# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import merlin

# the base language protocol
from .Language import Language


# C language configuration
class C(Language):
    """
    The C language specification
    """

    # configurable state
    dialect = merlin.properties.str()

    # framework hooks
    @classmethod
    def pyre_default(cls, **kwds):
        """
        Specify the default implementation
        """
        # publish the default implementation
        return merlin.languages.c()


# end of file

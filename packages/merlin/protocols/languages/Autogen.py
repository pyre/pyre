# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# support
import merlin

# the base language protocol
from .Language import Language


# the template expander
class Autogen(Language):
    """
    The template expander specification
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
        return merlin.languages.autogen()


# end of file

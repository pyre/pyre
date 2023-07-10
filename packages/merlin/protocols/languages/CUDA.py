# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import merlin

# the base language protocol
from .Language import Language


# CUDA configuration
class CUDA(Language):
    """
    The CUDA specification
    """

    # framework hooks
    @classmethod
    def pyre_default(cls, **kwds):
        """
        Specify the default implementation
        """
        # publish the default implementation
        return merlin.languages.cuda()


# end of file

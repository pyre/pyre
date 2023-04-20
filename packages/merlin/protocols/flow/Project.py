# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import merlin


# a builder of libraries
class Project(merlin.protocol, family="merlin.builders.project"):
    """
    Workflow generator for projects
    """

    # framework hooks
    @classmethod
    def pyre_default(cls, **kwds):
        """
        Specify the default implementation
        """
        # choose the default implementer
        return merlin.builders.flow.project


# end of file

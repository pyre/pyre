# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# support
import merlin


# class declaration
class Project(merlin.protocol, family="merlin.projects.basic"):
    """
    A high level container of assets
    """


    # framework hooks
    @classmethod
    def pyre_default(cls, **kwds):
        """
        Provide a default implementation of the {project} protocol
        """
        # grab the basic project foundry and return it
        return merlin.projects.project


# end of file

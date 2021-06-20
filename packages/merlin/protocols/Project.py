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


    @classmethod
    def pyre_configure(cls, name, locator, **kwds):
        """
        Locate and load configuration files for a component that is about to be instantiated
        given its {name}
        """
        # chain up
        super().pyre_configure(name=name, locator=locator, **kwds)

        # grab the executive
        executive = cls.pyre_executive
        # ask it to hunt down and load any project configuration files
        executive.configureStem(stem=name, cfgpath=["pfs:/workspace"], locator=locator)

        # all done
        return cls


# end of file

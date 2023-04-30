# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import merlin
# superclass
from .Asset import Asset
# schema
from .Library import Library as library


# class declaration
class Project(Asset, family="merlin.assets.projects"):
    """
    A high level container of artifacts
    """


    # required state
    libraries = merlin.properties.tuple(schema=library())
    libraries.doc = "the collection of project libraries"


    # framework hooks
    @classmethod
    def pyre_default(cls, **kwds):
        """
        Specify the default implementation
        """
        # grab the basic project foundry and return it
        return merlin.assets.project


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

# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <nichael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# support
import merlin
# superclass
from .Asset import Asset


# class declaration
class Source(Asset,
             family="merlin.projects.sources.source", implements=merlin.protocols.source):
    """
    Encapsulation of a source file
    """


    # meta methods
    def __init__(self, language, **kwds):
        # chain up
        super().__init__(**kwds)
        # and remember my source language
        self.language = language
        # all done
        return


# end of file

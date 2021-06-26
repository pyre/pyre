# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# support
import merlin
# schema
from .Language import Language as language


# class declaration
class Library(merlin.protocol, family="merlin.projects.libraries"):
    """
    A high level container of binary artifacts
    """


    # user configurable state
    languages = merlin.properties.tuple(schema=language())
    languages.doc = "the languages of the library source assets"


    # framework hooks
    @classmethod
    def pyre_default(cls, **kwds):
        """
        Specify the default implementation
        """
        # grab the library foundry and return it
        return merlin.projects.library


# end of file

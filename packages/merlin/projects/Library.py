# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# support
import merlin


# class declaration
class Library(merlin.component,
              family="merlin.projects.library", implements=merlin.protocols.library):
    """
    A container of binary artifacts
    """


    # user configurable state
    languages = merlin.properties.tuple(schema=merlin.protocols.language())
    languages.doc = "the languages of the library source assets"


# end of file

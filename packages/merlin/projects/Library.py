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
    name = merlin.properties.str()
    name.doc = "the name of the library; used as a seed to name its various assets"

    root = merlin.properties.path()
    root.doc = "the path to the library source relative to the root of the repository"

    languages = merlin.properties.tuple(schema=merlin.protocols.language())
    languages.doc = "the languages of the library source assets"


# end of file

# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# support
import merlin


# base class for all supported languages
class Language(merlin.component, implements=merlin.protocols.language):
    """
    A category of source artifacts, usually associated with a family of processing workflows
    """


    # constants
    name = None
    linkable = False


    # required state
    sources = merlin.properties.strings()
    sources.doc = "the set of suffixes that identify an artifact as a source"


# end of file

# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# support
import merlin


# the protocol that all supported languages must implement
class Language(merlin.protocol, family="merlin.languages"):
    """
    A category of source artifacts, usually associated with a family of processing workflows
    """


    # required state
    sources = merlin.properties.strings()
    sources.doc = "the set of suffixes that identify an artifact as a source"


# end of file

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
    # the language tag
    name = None
    # properties of the canonical toolchains associated with this language
    linkable = False   # whether the products are recognized by the system linker
    # asset factories
    sourceFactory = merlin.projects.source
    headerFactory = merlin.projects.header

    # required state
    headers = merlin.properties.strings()
    headers.doc = "the set of suffixes that identify an artifact as a header"

    sources = merlin.properties.strings()
    sources.doc = "the set of suffixes that identify an artifact as a source"


    # interface
    @classmethod
    def recognize(cls, name, node):
        """
        Attempt to recognize the asset represented by {node}
        """
        # extract the suffix of the filename
        suffix = node.uri.suffix
        # if it is one of mine
        if suffix in cls.sources:
            # make a source asset
            asset = cls.sourceFactory(name=name, node=node, language=cls)
            # and return it
            return asset

        # if not, check against my headers
        if node.uri.suffix in cls.headers:
            # make a header
            asset = cls.headerFactory(name=name, node=node)
            # and return it
            return asset

        # out of ideas
        return None


# end of file

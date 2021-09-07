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
    headers = merlin.properties.strings()
    headers.doc = "the set of suffixes that identify an artifact as a header"

    sources = merlin.properties.strings()
    sources.doc = "the set of suffixes that identify an artifact as a source"


    # implementation details
    # a map from the common to the canonical name of a language; this index is
    # maintained automatically by the {merlin.components.language} foundry
    aliases = {}


    # framework hooks
    @classmethod
    def pyre_convert(cls, value, **kwds):
        """
        Translate the component specification in {value} into canonical form; invoked during value
        processing
        """
        # turn the value into a {uri}
        uri = cls.uri().coerce(value)
        # extract the address bit, convert it to lower case
        family = uri.address.lower()
        # run it through the compiler aliases
        family = cls.aliases.get(family, family)
        # and reattach it
        uri.address = family

        # recast to a string and chain up
        return super().pyre_convert(value=str(uri), **kwds)


# end of file

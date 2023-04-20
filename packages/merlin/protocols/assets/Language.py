# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import merlin


# the protocol that all supported languages must implement
class Language(merlin.protocol, family="merlin.languages"):
    """
    A category of source artifacts, usually associated with a family of processing workflows
    """


    # required state
    categories = merlin.properties.catalog(schema=merlin.properties.str())
    categories.doc = "a map from file categories to a list of suffixes"


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
        # if {value} is not a string
        if not isinstance(value, str):
            # leave it alone
            return value

        # otherwise, turn the value into a {uri}
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

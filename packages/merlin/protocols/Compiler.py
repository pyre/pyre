# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import merlin


# the protocol that all supported compilers must implement
class Compiler(merlin.protocol, family="merlin.compilers"):
    """
    An artifact factory that translates sources into a binary form
    """


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

        # otherwise, pull the known aliases from {compilers}
        from merlin.compilers import aliases

        # turn the value into a {uri}
        uri = cls.uri().coerce(value)
        # extract the address bit
        family = uri.address
        # run it through the compiler aliases
        family = aliases.get(family, family)
        # and reattach it
        uri.address = family

        # recast into a string and chain up
        return super().pyre_convert(value=str(uri), **kwds)


# end of file

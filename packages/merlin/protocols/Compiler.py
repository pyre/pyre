# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


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
        # pull the known aliases from {compilers}
        from merlin.compilers import aliases

        # turn the value into a {uri}
        uri = cls.uri().coerce(value)
        # extract the address bit
        family = uri.address
        # run it through the compiler aliases
        family = aliases.get(family, family)
        # and reattach it
        uri.address = family

        # chain up
        return super().pyre_convert(value=str(uri), **kwds)


# end of file

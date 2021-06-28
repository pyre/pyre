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


# end of file

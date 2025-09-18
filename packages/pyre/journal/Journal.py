# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# support
import pyre


# the specification for the top level channel manager
class Journal(pyre.protocol, family="pyre.journal"):
    """
    The manager of the application journal channels
    """

    # user configurable tate
    decor = pyre.properties.int()
    decor.default = 1
    decor.doc = "the default state of all application channels"

    detail = pyre.properties.int()
    detail.default = 2
    detail.doc = "the maximum level of detail that is included in the output"

    margin = pyre.properties.str()
    margin.default = "  "
    margin.doc = "the decoration to add to indented output"

    # interface obligations
    @pyre.provides
    def register(self, app, name):
        """
        Register the application name with the journal
        """

    # framework hooks
    @classmethod
    def pyre_default(cls, **kwds):
        """
        Provide a default implementation
        """
        # i have on of those
        from .Chronicler import Chronicler

        # so hand it off
        return Chronicler


# end of file

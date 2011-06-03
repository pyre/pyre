# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# packages
import pyre


# declaration
class Device(pyre.interface, family="journal.devices"):
    """
    The interface that devices must implement
    """


    # types
    from .Renderer import Renderer


    # public state
    renderer = pyre.properties.facility(interface=Renderer)


    # interface
    @pyre.provides
    def record(self, page, metadata):
        """
        Create a journal entry from the given information
        """


    # utilities
    @classmethod
    def defaultRenderer(cls):
        """
        Examine {sys.stdout} and turn on color output if the current terminal type supports it
        """
        # access the stdout stream
        import sys
        # if it is a tty
        try:
            if sys.stdout.isatty():
                # figure out the terminal type
                import os
                term = os.environ.get('TERM', 'unknown').lower()
                # if it is ANSI compatible
                if term in cls.ansi:
                    # the default is colored
                    from .ANSIRenderer import ANSIRenderer
                    return ANSIRenderer
        # some devices don't support isatty
        except AttributeError:
            pass
        # plain text, by default
        from .TextRenderer import TextRenderer
        return TextRenderer


    # private data
    ansi = {'ansi', 'vt102', 'vt220', 'vt320', 'vt420', 'xterm', 'xterm-color'}


# end of file 

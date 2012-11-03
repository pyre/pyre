# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# access to the framework
import pyre


# declaration
class Terminal(pyre.protocol, family='pyre.terminals'):
    """
    An abstraction for the capabilities of user terminals
    """


    # framework support
    @classmethod
    def pyre_default(cls):
        """
        Sniff out the capabilities of the current terminal and choose the default implementation
        """
        # access the {stdout} stream
        import sys
        # check whether
        try:
            # the current terminal is a tty
            if sys.stdout.isatty():
                # access the environment
                import os
                # to figure out the terminal type
                term = os.environ.get('TERM', 'unknown').lower()
                # if it is ANSI compatible
                if term in cls.ansi:
                    # get the ansi terminal
                    from .ANSI import ANSI
                    # and return it
                    return ANSI
        # some devices don't support {isatty}
        except AttributeError: pass

        # otherwise, get the plain terminal
        from .Plain import Plain
        # and return it
        return Plain


    # implementation details
    ansi = {'ansi', 'vt102', 'vt220', 'vt320', 'vt420', 'xterm', 'xterm-color'}
            

# end of file 

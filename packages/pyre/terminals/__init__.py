# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the foundry decorator
from .. import foundry

# the terminal capability protocols
from .Terminal import Terminal as terminal
from .Console import Console as console

# the key decoder, for building interactive prompts
from . import keys


# the terminal implementations
@foundry(implements=terminal)
def ansi():
    """
    A terminal that renders color using ANSI control sequences
    """
    # get the component
    from .ANSI import ANSI

    # and publish it
    return ANSI


@foundry(implements=terminal)
def interactive():
    """
    A live terminal with raw input and cursor control, but no color
    """
    # get the component
    from .Interactive import Interactive

    # and publish it
    return Interactive


@foundry(implements=terminal)
def plain():
    """
    A terminal with no color and no live input
    """
    # get the component
    from .Plain import Plain

    # and publish it
    return Plain


# end of file

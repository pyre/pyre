#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    A plain terminal reports no color and answers the {os}-backed device queries
    """
    # get the framework
    import pyre

    # make a plain terminal
    from pyre.terminals.Plain import Plain

    # and instantiate it
    terminal = Plain(name="test.plain")

    # it has no color capability, so every color request comes back empty
    assert terminal.color("red") == ""
    # named or numeric
    assert terminal.rgb("c02020") == ""
    # it renders nothing
    assert terminal.render(None) == ""
    # and has nothing to reset
    assert terminal.reset() == ""
    # it does not advertise cursor control or raw input at all
    assert not hasattr(terminal, "hideCursor")
    # and no raw input
    assert not hasattr(terminal, "rawmode")

    # and the device queries return values of the expected kind
    assert isinstance(terminal.width(), int)
    # both dimensions
    assert isinstance(terminal.height(), int)
    # and whether it is interactive
    assert isinstance(terminal.interactive(), bool)

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file

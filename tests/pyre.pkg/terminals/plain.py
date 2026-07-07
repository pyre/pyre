#! /usr/bin/env python3
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

    term = Plain(name="test.plain")

    # it has no color capability
    assert term.chromatic is False
    # so every color request comes back empty
    assert term.color("red") == ""
    assert term.render(None) == ""
    assert term.reset() == ""

    # and the device queries return values of the expected kind
    assert isinstance(term.width(), int)
    assert isinstance(term.height(), int)
    assert isinstance(term.interactive(), bool)

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file

#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    The {pyre.terminals} package publishes the protocol, its implementations, and the sniff
    """
    # get the framework
    import pyre

    # the package is reachable through {import pyre}
    terminals = pyre.terminals
    # the two capability protocols are published
    assert terminals.terminal is not None
    assert terminals.console is not None
    # as are the three implementation foundries
    assert terminals.ansi is not None
    assert terminals.interactive is not None
    assert terminals.plain is not None
    # and the key decoder
    assert terminals.keys is not None

    # the compatibility sniff now lives on the terminal protocol and answers the known cases
    assert terminals.terminal.compatible("xterm") is True
    assert terminals.terminal.compatible("dumb") is False

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file

#!/usr/bin/env python3
# -*- python -*-
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
    # both of them
    assert terminals.console is not None
    # as are the three implementation foundries
    assert terminals.ansi is not None
    # the interactive one
    assert terminals.interactive is not None
    # and the plain one
    assert terminals.plain is not None
    # and the key decoder
    assert terminals.keys is not None

    # the compatibility sniff lives on the terminal protocol: it recognizes the terminals it knows
    # are compatible
    assert terminals.terminal.compatible("xterm") is True
    # and the ones it knows are not
    assert terminals.terminal.compatible("dumb") is False

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file

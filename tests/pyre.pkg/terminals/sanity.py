#! /usr/bin/env python3
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
    # the protocol and the two implementation foundries are published
    assert terminals.terminal is not None
    assert terminals.ansi is not None
    assert terminals.plain is not None

    # the compatibility sniff answers the known cases
    assert terminals.compatible("xterm") is True
    assert terminals.compatible("dumb") is False

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file

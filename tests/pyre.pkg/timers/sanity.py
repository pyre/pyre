#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Sanity test: make sure the pure python timer implementations are accessible
    """
    # access the timer bindings
    from pyre.timers.WallTimer import WallTimer
    from pyre.timers.ProcessTimer import ProcessTimer
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file

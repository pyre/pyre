#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that component behaviors are callable
"""


def test():
    import pyre

    # declare a component
    class component(pyre.component):
        """a test component"""

        # behavior
        @pyre.export
        def do(self):
            """behave"""
            return True

    # instantiate it
    c = component(name="test")
    # invoke its behavior
    assert c.do()
    # and return it
    return c


# main
if __name__ == "__main__":
    test()


# end of file

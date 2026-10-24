#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that an instance that has opened a stream keeps it when its class changes, so that nobody
has to close a stream the instance did not ask to give up
"""


def test() -> None:
    """
    Make an instance, open its stream, point the class at another file, and read the instance again
    """
    # access the framework
    import pyre

    # a component class with a stream
    class base(pyre.component, family="pyre.tests.attributes.base"):
        """a component class with a stream"""

        # the stream, with its class default
        t = pyre.properties.istream(default=f"file:{__file__}")

    # an instance
    b = base(name="b")
    # that opens its stream
    stream = b.t
    # point the class at another file
    base.t = "file:/dev/null"
    # the instance keeps the stream it opened
    assert b.t is stream
    # which is still open
    assert not stream.closed
    # and done with it
    stream.close()

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file

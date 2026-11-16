#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise the channel schema: a channel renders as the import path of its class, its hints and
its descriptor numbers, and the rendering coerces back into a channel of the same kind over the
same descriptors
"""


def test():
    # support
    import pyre

    # make a converter
    schema = pyre.schemata.channel()

    # make a channel
    parent, child = pyre.ipc.newSocket().open()
    # render it
    rendering = schema.string(child)
    # the rendering names the class, its hints and its descriptor
    assert rendering == f"pyre.ipc.SocketPair:SocketPair?family=1&type=1&proto=0#{child.fileno()}"
    # channels are left alone
    assert schema.coerce(child) is child
    # renderings are turned into channels; detach the original, so the two do not share a
    # descriptor that both would close
    descriptor = child.detach()
    # coerce the rendering
    rebuilt = schema.coerce(rendering)
    # into a channel of the same kind
    assert type(rebuilt) is type(child)
    # over the same descriptor
    assert rebuilt.fileno() == descriptor
    # that works
    rebuilt.write(bytes=b"hello")
    # as the other end can tell
    assert parent.read(minlen=5, maxlen=5) == b"hello"

    # a pipe channel that only writes
    pipe = pyre.ipc.newPipe().wrap(outfd=7)
    # renders with the end it has
    assert schema.string(pipe) == "pyre.ipc.Pipe:Pipe?ends=out#7"

    # nothing is rendered as nothing
    assert schema.string(None) is None

    # values of other kinds
    try:
        # cannot be coerced
        schema.coerce(7)
    # and the schema says so
    except schema.CastingError:
        # as expected
        pass
    # anything else
    else:
        # is a failure
        assert False, "an integer was coerced into a channel"

    # clean up
    rebuilt.close()
    # both ends
    parent.close()

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file

#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that the fork shell hands each process one channel per standard stream of the child,
each owning its own descriptors, and that the parent sees the end of the output of the child
when it exits
"""


def test():
    # support
    import pyre

    # declare a trivial application
    class application(pyre.application, family="shells.application"):
        """
        A sample application
        """

        @pyre.export
        def main(self, channels, **kwds):
            """
            The behavior of the child process
            """
            # say something short on my output stream, and leave
            channels.stdout.write(b"done")
            # all done
            return 0

        @pyre.export
        def launched(self, channels, **kwds):
            """
            The behavior of the parent process
            """
            # one channel per stream
            assert channels._fields == ("stdin", "stdout", "stderr")
            # the parent writes to the input of the child
            assert channels.stdin.descriptors() == [channels.stdin.outbound]
            # and reads its output
            assert channels.stdout.descriptors() == [channels.stdout.inbound]
            # and its error stream
            assert channels.stderr.descriptors() == [channels.stderr.inbound]
            # through descriptors that are all different
            assert (
                len({channels.stdin.outbound, channels.stdout.inbound, channels.stderr.inbound})
                == 3
            )
            # asking for more than the child says returns what it said once it is gone
            assert channels.stdout.read(minlen=1024, maxlen=1024) == b"done"
            # all done
            return 0

    # instantiate it
    app = application(name="πολυδεύκης")
    # launch it
    status = app.run()
    # check it
    assert status == 0
    # and return the application instance
    return app


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file

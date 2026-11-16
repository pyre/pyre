#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Instantiate a script
"""


def test():
    # externals
    import pyre  # access the framework

    # declare a trivial application
    class application(pyre.application, family="shells.application"):
        """
        A sample application
        """

        @pyre.export
        def main(self, **kwds):
            """
            The behavior of the daemon, whose output goes to the launching process
            """
            # say something on my output stream
            print("Hello")
            # all done
            return 0

        # implementation details
        @pyre.export
        def launched(self, channels, **kwds):
            """
            The behavior in the parent process
            """
            # make sure we can read the output of the child correctly
            assert channels.stdout.read(6) == b"Hello\n"
            # all done
            return 0

    # instantiate it
    app = application(name="μέδουσα")
    # check that its shell was configured correctly
    assert app.shell.pyre_name == "κητώ"
    # launch it
    status = app.run()
    # check it
    assert status == 0
    # and return the app
    return app


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file

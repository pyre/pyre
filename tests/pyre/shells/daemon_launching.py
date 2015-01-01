#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


"""
Instantiate a script
"""


def test():
    # externals
    import pyre # access the framework

    # declare a trivial application
    class application(pyre.application, family='shells.application'):
        """a sample application"""

        @pyre.export
        def main(self, **kwds):
            print("Hello")
            return 0

    # instantiate it
    app = application(name='μέδουσα')
    # check that its shell was configured correctly
    assert app.shell.pyre_name == 'κητώ'

    # if it is in debugging mode
    if app.DEBUG:
        print("in debugging mode")
        # launch it
        status = app.run()
        # check it
        assert status == 0
        # and return the app
        return app

    # if this is the re-invocation  of the daemon spawn
    if app.shell.daemon:
        # launch it
        status = app.run()
        # check it
        assert status == 0
        # and return the status
        return status

    # otherwise, launch it and get the channels to the child
    stdout, stderr = app.run()

    # make sure we can read its output correctly
    assert stdout.read(10) == b"Hello\n"

    # and return the app
    return app


# main
if __name__ == "__main__":
    test()


# end of file

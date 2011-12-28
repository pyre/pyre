#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Exercise the spawning of daemons
"""


def test():
    import os
    # access the framework
    import pyre
    # instantiate a daemon
    d = pyre.daemon(name="daemon")
    # launch it
    d.run()
    pid = os.getpid()
    # print("{}: waiting for children to exit".format(pid))

    # collect the return codes
    while 1:
        # try to collect the exit status of my children
        try:
            child, status = os.wait()
        # if something went wrong
        except OSError as error:
            # because there are no more children
            if error.errno == 10:
                # say so
                # print("{}: no children".format(pid))
                # and bail out
                break
            # otherwise, report the exception
            raise
        # otherwise, report the child pid and the exit code
        else:
            # print("{}: child {}: status={}".format(pid, child, status))
            pass

    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file 

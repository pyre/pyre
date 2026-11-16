#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a channel crosses an {exec} as a string on the command line: the new process
inherits its descriptors under the same numbers, turns the string back into the channel, and
talks through it
"""

# what the new process runs: rebuild the channel from its first argument and say hello
script = """
import sys
import pyre
channel = pyre.schemata.channel().coerce(sys.argv[1])
channel.write(bytes=type(channel).__name__.encode())
"""


def test():
    # externals
    import subprocess
    import sys

    # support
    import pyre

    # make a channel
    parent, child = pyre.ipc.newSocket().open()
    # render the child's end
    rendering = pyre.schemata.channel().string(child)
    # start a new interpreter, handing it the channel
    process = subprocess.Popen(
        [sys.executable, "-c", script, rendering], pass_fds=child.descriptors(), close_fds=True
    )
    # its end is its own now
    child.close()
    # it says hello with the kind of channel it rebuilt
    assert parent.read(minlen=10, maxlen=10) == b"SocketPair"
    # and leaves happy
    assert process.wait() == 0
    # clean up
    parent.close()

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file

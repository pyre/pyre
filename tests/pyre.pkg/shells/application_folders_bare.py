#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that an application launched from a prefix without private folders leaves the prefix
alone, instead of creating them on every launch, and mounts empty folders in their place
"""


def launch(application, name, prefix):
    """
    Instantiate {application} as {name}, as if it had been launched by a script in {prefix}/bin
    """
    # externals
    import os
    import sys

    # get access to the framework
    import pyre

    # the launching script
    script = os.path.join(prefix, "bin", "folders.py")
    # make it
    os.makedirs(os.path.dirname(script), exist_ok=True)
    open(script, mode="w").close()

    # remember how this script was launched
    argv0 = sys.argv[0]
    # pretend it was launched by the script in {prefix}
    sys.argv[0] = script
    # carefully
    try:
        # instantiate
        app = application(name=name)
    # in any case
    finally:
        # restore the launch path
        sys.argv[0] = argv0
    # the application found its prefix through the script
    assert str(app.pyre_prefix) == os.path.realpath(prefix)
    # hand it off
    return app


def test():
    # externals
    import os
    import tempfile

    # get access to the framework
    import pyre

    # declare a trivial application with a namespace
    class application(pyre.application, family="folders.application"):
        """A trivial pyre application in the {folders} namespace"""

    # a prefix with no private folders
    with tempfile.TemporaryDirectory() as prefix:
        # launch from it
        app = launch(application=application, name="bare", prefix=prefix)
        # nothing was created
        assert sorted(os.listdir(prefix)) == ["bin"]
        # but the private filespace has both folders, empty
        for folder in ["etc", "var"]:
            # each one
            assert app.pfs[folder].contents == {}

    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file

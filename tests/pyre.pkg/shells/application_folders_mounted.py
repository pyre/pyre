#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that an application mounts the private folders it finds under its prefix, without
creating the ones that are not there
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

    # a prefix with a {var} folder of its own
    with tempfile.TemporaryDirectory() as prefix:
        # make it, with something in it
        os.makedirs(os.path.join(prefix, "var", "folders"))
        open(os.path.join(prefix, "var", "folders", "state.txt"), mode="w").close()
        # launch from it
        app = launch(application=application, name="furnished", prefix=prefix)
        # the folder is mounted
        assert "state.txt" in app.pfs["var"].contents
        # and its sibling was not created
        assert sorted(os.listdir(prefix)) == ["bin", "var"]

    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file

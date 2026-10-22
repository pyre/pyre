#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Setting an environment variable through the executive places it in the environment and in the
configuration store, attributed to the line that set it
"""


def test() -> None:
    """
    Set a variable through the executive's environment and look for it in both places
    """
    # support
    import os
    import pyre

    # the executive's view of the environment
    environ = pyre.executive.environ
    # and its configuration store
    nameserver = pyre.executive.nameserver
    # a variable nobody else sets
    name = "PYRE_TESTS_FRAMEWORK_ENVIRON_SET"
    # and the store key it maps to
    key = environ.prefix + name

    # set it
    environ[name] = "hello"
    # it is now in the environment of the process
    assert os.environ[name] == "hello"
    # and in the store
    assert nameserver[key] == "hello"
    # attributed to the line above that set it, in this file
    locator = str(nameserver.getInfo(nameserver.hash(key)).locator)
    # so the locator names this file
    assert "environ_set.py" in locator, locator

    # remove it from the environment
    del environ[name]
    # so it is gone from there
    assert name not in os.environ

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file

#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Verify that the package publishes the same names, whichever implementation is active
    """
    # externals
    import types

    # access
    import journal

    # the names the package publishes
    published = {
        # the exceptions
        "JournalError",
        "FirewallError",
        "DebugError",
        "ApplicationError",
        # the choice of implementation
        "without_libjournal",
        # the keeper of the global settings
        "chronicler",
        # the devices
        "trash",
        "file",
        "cout",
        "cerr",
        "splitter",
        "tee",
        "courier",
        "device",
        # the channels
        "debug",
        "firewall",
        "info",
        "warning",
        "error",
        "help",
        "severities",
        # entries in transit
        "entry",
        "record",
        "control",
        "replay",
        # the convenience functions
        "application",
        "quiet",
        "logfile",
        "decor",
        "detail",
        "margin",
        "bootComplete",
        # the color and symbol tables
        "ansi",
        "ascii",
        # administrative
        "copyright",
        "license",
        "version",
        "credits",
    }
    # the modules that implement the package may show up in its namespace; they are not published
    names = {
        name
        for name, value in vars(journal).items()
        if not name.startswith("_") and not isinstance(value, types.ModuleType)
    }

    # every published name must be present
    missing = published - names
    # and nothing else may be
    extra = names - published
    # check
    assert not missing, f"missing: {sorted(missing)}"
    # both ways
    assert not extra, f"unexpected: {sorted(extra)}"

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file

#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
The host recognizes library filenames in every spelling the supported platforms use

The two platforms version their shared libraries at opposite ends of the name, so a
pattern that knows only one convention silently fails to find half the libraries that
are actually there
"""

# externals
import re


def test():
    """
    Match library filenames against the pattern the host builds
    """
    # support
    import pyre

    # the generic host, so the answers don't depend on where this runs
    from pyre.platforms.Host import Host

    # the pattern for a library named {mpi}
    pattern = Host.libraryPattern(stem="mpi")

    # the linux spellings: bare, and versioned after the suffix
    assert re.match(pattern, "libmpi.so")
    assert re.match(pattern, "libmpi.so.40")
    assert re.match(pattern, "libmpi.so.40.30.0")
    # the darwin spellings: bare, and versioned ahead of the suffix
    assert re.match(pattern, "libmpi.dylib")
    assert re.match(pattern, "libmpi.40.dylib")
    # and the static archive
    assert re.match(pattern, "libmpi.a")

    # the stem is captured, whichever spelling matched
    assert re.match(pattern, "libmpi.so.40").group("stem") == "mpi"
    assert re.match(pattern, "libmpi.40.dylib").group("stem") == "mpi"

    # a different library is not mine
    assert not re.match(pattern, "libmpix.so")
    # neither is one without the prefix
    assert not re.match(pattern, "mpi.so")
    # nor one whose suffix belongs to something else
    assert not re.match(pattern, "libmpi.py")

    # a caller that cannot use a static archive says so
    dynamic = Host.libraryPattern(stem="mpi", static=False)
    # and the archive stops matching
    assert not re.match(dynamic, "libmpi.a")
    # while the shared libraries still do
    assert re.match(dynamic, "libmpi.so.40")
    assert re.match(dynamic, "libmpi.40.dylib")

    # the stem is a pattern in its own right, which is how versioned names are reached
    versioned = Host.libraryPattern(stem=r"python3\.\d+[tdm]*")
    # an abi tagged interpreter library resolves
    assert re.match(versioned, "libpython3.13t.so").group("stem") == "python3.13t"
    # as does the darwin spelling of the same thing
    assert re.match(versioned, "libpython3.14.dylib").group("stem") == "python3.14"

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file

#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Database reported versions outrank content extracted ones
"""

# the fake database: the serial hdf5 flavor, with a version that deliberately disagrees
# with the fixture's {H5pubconf.h}
installed = {
    # the development package
    "libhdf5-dev": ("1.14.6", "1"),
}

# the contents of each package; the paths are anchored in the test fixture, whose serial
# variant of {H5pubconf.h} declares version 1.14.5
contents = {
    # the serial development artifacts
    "libhdf5-dev": [
        "prefix/include/hdf5/serial/hdf5.h",
        "prefix/lib/hdf5/serial/libhdf5.dylib",
        "prefix/lib/hdf5/serial/libhdf5_cpp.dylib",
    ],
}


def test():
    """
    Resolve hdf5 and verify the database version wins over the header's
    """
    # the engine to fake
    from pyre.platforms.DPkg import DPkg

    # the index class
    from pyre.externals.Index import Index

    # an engine wired to the fake database instead of a dpkg client
    class engine(DPkg):
        """
        A dpkg engine over canned data
        """

        # the installed package index
        def getInstalledPackages(self):
            """
            Serve the canned index
            """
            # easy enough
            return installed

        # package contents
        def retrievePackageContents(self, package):
            """
            Serve the canned contents
            """
            # easy enough
            yield from contents[package]
            # all done
            return

    # make a private index over the fake engine
    index = Index()
    # wire it
    index._engines = (engine(name="dpkg.fake.proof.precedence"),)
    # resolve
    report = index.resolve(requested=["hdf5"])
    # the database speaks with authority: 1.14.6, not the header's 1.14.5
    assert report.selections["hdf5"].version == "1.14.6"

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file

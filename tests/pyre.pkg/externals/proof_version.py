#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Content extractors supply the version when the database doesn't report one
"""

# the fake database: the serial hdf5 flavor
installed = {
    # the development package
    "libhdf5-dev": ("1.14.5", "1"),
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
    Resolve hdf5 against a version-less database and verify the harvested version
    """
    # the engine to fake
    from pyre.platforms.DPkg import DPkg

    # the index class
    from pyre.externals.Index import Index

    # an engine wired to the fake database, whose version records are missing
    class engine(DPkg):
        """
        A dpkg engine over canned data that doesn't know package versions
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

        # the version oracle
        def version(self, package):
            """
            Pretend the database has no version records
            """
            # nothing to report
            return None

    # make a private index over the fake engine
    index = Index()
    # wire it
    index._engines = (engine(name="dpkg.fake.proof.version"),)
    # resolve
    report = index.resolve(requested=["hdf5"])
    # the version came from the build configuration header
    assert report.selections["hdf5"].version == "1.14.5"

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file

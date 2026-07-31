#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Version demands filter selections using the database-reported versions
"""

# the fake database: both mpi flavors are installed
installed = {
    # openmpi, the preferred flavor
    "libopenmpi-dev": ("5.0.8", "1"),
    "openmpi-bin": ("5.0.8", "1"),
    # mpich, the alternative
    "libmpich-dev": ("4.3.0", "1"),
    "mpich": ("4.3.0", "1"),
}

# the contents of each package; the paths are anchored in the test fixture so that the
# configured directories exist and the installations validate
contents = {
    # the openmpi development artifacts and launcher
    "libopenmpi-dev": ["prefix/include/mpi.h", "prefix/lib/libmpi.dylib"],
    "openmpi-bin": ["prefix/bin/mpirun.openmpi"],
    # the mpich development artifacts and launcher
    "libmpich-dev": ["prefix/include/mpich/mpi.h", "prefix/lib/mpich/libmpich.dylib"],
    "mpich": ["prefix/bin/mpirun.mpich"],
}


def test():
    """
    Resolve version windows the database can and cannot satisfy
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

    # a window the openmpi installation satisfies
    index = Index()
    # wire it
    index._engines = (engine(name="dpkg.fake.version.lo"),)
    # resolve
    report = index.resolve(requested=["mpi>=5"])
    # the preferred flavor satisfies the demand
    assert report.selections["mpi"].flavor == "openmpi"
    # and carries the database-reported version
    assert report.selections["mpi"].version == "5.0.8"

    # a window neither installation satisfies
    index = Index()
    # wire it
    index._engines = (engine(name="dpkg.fake.version.hi"),)
    # resolve
    report = index.resolve(requested=["mpi>=6"])
    # the category must be flagged as conflicted, since the demand did the filtering
    assert "mpi" in report.conflicted
    # and not as missing
    assert "mpi" not in report.unavailable

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file

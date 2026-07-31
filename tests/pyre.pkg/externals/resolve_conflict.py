#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Unsatisfiable demands are reported as conflicts, not as missing packages
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
    Demand a flavor no recipe answers to and verify the conflict diagnosis
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
    index._engines = (engine(name="dpkg.fake.conflict"),)
    # resolve a request no flavor can answer
    report = index.resolve(requested=["mpi[nosuchflavor]"])
    # the category must be flagged as conflicted
    assert "mpi" in report.conflicted
    # with the offending requirement as the evidence
    assert any(str(req) == "mpi[nosuchflavor]" for req in report.conflicted["mpi"])
    # it must not appear among the selections
    assert "mpi" not in report.selections
    # and it must not masquerade as a missing package: mpi is very much installed here
    assert "mpi" not in report.unavailable

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file

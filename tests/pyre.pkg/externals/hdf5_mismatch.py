#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Demands that would mix mpi implementations are reported as an mpi conflict
"""

# the fake database: all three hdf5 flavors and both mpi implementations are installed
installed = {
    # the hdf5 flavors
    "libhdf5-dev": ("1.14.5", "1"),
    "libhdf5-openmpi-dev": ("1.14.5", "1"),
    "libhdf5-mpich-dev": ("1.14.5", "1"),
    # the mpi implementations
    "libopenmpi-dev": ("5.0.8", "1"),
    "openmpi-bin": ("5.0.8", "1"),
    "libmpich-dev": ("4.3.0", "1"),
    "mpich": ("4.3.0", "1"),
}

# the contents of each package; the paths are anchored in the test fixture so that the
# configured directories exist and the installations validate
contents = {
    # the hdf5 variant subdirectories, debian style
    "libhdf5-dev": [
        "prefix/include/hdf5/serial/hdf5.h",
        "prefix/lib/hdf5/serial/libhdf5.dylib",
        "prefix/lib/hdf5/serial/libhdf5_cpp.dylib",
    ],
    "libhdf5-openmpi-dev": [
        "prefix/include/hdf5/openmpi/hdf5.h",
        "prefix/lib/hdf5/openmpi/libhdf5.dylib",
        "prefix/lib/hdf5/openmpi/libhdf5_cpp.dylib",
    ],
    "libhdf5-mpich-dev": [
        "prefix/include/hdf5/mpich/hdf5.h",
        "prefix/lib/hdf5/mpich/libhdf5.dylib",
        "prefix/lib/hdf5/mpich/libhdf5_cpp.dylib",
    ],
    # the mpi development artifacts and launchers
    "libopenmpi-dev": ["prefix/include/mpi.h", "prefix/lib/libmpi.dylib"],
    "openmpi-bin": ["prefix/bin/mpirun.openmpi"],
    "libmpich-dev": ["prefix/include/mpich/mpi.h", "prefix/lib/mpich/libmpich.dylib"],
    "mpich": ["prefix/bin/mpirun.mpich"],
}


def test():
    """
    Demand an openmpi hdf5 alongside an mpich mpi and verify the conflict
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
    index._engines = (engine(name="dpkg.fake.hdf5.mismatch"),)
    # demand an openmpi hdf5 in the same breath as an mpich mpi
    report = index.resolve(requested=["hdf5[openmpi]", "mpi[mpich]"])
    # the mpi demands cannot be reconciled
    assert "mpi" in report.conflicted
    # the evidence names both irreconcilable requirements
    evidence = {str(req) for req in report.conflicted["mpi"]}
    assert "mpi[openmpi]" in evidence and "mpi[mpich]" in evidence
    # and no mpi was selected
    assert "mpi" not in report.selections

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file

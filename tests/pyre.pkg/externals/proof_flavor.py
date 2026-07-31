#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Content proofs classify a flavor-ambiguous database

Conda and macports name every hdf5 flavor {hdf5}; the fake package here carries an mpi
aware build under that bare name, so only the {H5pubconf.h} proof can classify it: the
serial recipe must reject it, and the openmpi recipe must claim it
"""

# the fake database: one ambiguously named hdf5, plus the mpi it was built against
installed = {
    # the bare name every conda/macports flavor answers to
    "hdf5": ("1.14.5", "1"),
    # the mpi implementation
    "libopenmpi-dev": ("5.0.8", "1"),
    "openmpi-bin": ("5.0.8", "1"),
}

# the contents of each package; the paths are anchored in the test fixture, whose openmpi
# variant of {H5pubconf.h} declares {H5_HAVE_PARALLEL}
contents = {
    # the mpi aware build, under the bare name
    "hdf5": [
        "prefix/include/hdf5/openmpi/hdf5.h",
        "prefix/lib/hdf5/openmpi/libhdf5.dylib",
        "prefix/lib/hdf5/openmpi/libhdf5_cpp.dylib",
    ],
    # the mpi development artifacts and launcher
    "libopenmpi-dev": ["prefix/include/mpi.h", "prefix/lib/libmpi.dylib"],
    "openmpi-bin": ["prefix/bin/mpirun.openmpi"],
}


def test():
    """
    Resolve an unconstrained request and verify the proof drives the classification
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
    index._engines = (engine(name="dpkg.fake.proof.flavor"),)
    # resolve an unconstrained request; the name says nothing, the header everything
    report = index.resolve(requested=["hdf5"])
    # the serial recipe was refuted by the proof, and the openmpi recipe claimed the build
    assert report.selections["hdf5"].flavor == "hdf5-openmpi"
    # correctly classified as parallel
    assert "parallel" in report.selections["hdf5"].tags
    # with the induced mpi edge honored
    assert report.selections["mpi"].flavor == "openmpi"
    # and nothing conflicted
    assert not report.conflicted

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file

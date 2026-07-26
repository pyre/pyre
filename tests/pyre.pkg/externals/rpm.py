#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise the rpm engine against a canned database

The layout is modeled on an actual fedora host: libraries under {lib64}, arch tagged mpi
include directories, and launchers split into the runtime packages that ride along as
companions of the {-devel} leads
"""

# the fake database, modeled on an actual fedora host
installed = {
    # gsl: the development package and the runtime
    "gsl-devel": ("2.8", "3"),
    "gsl": ("2.8", "3"),
    # mpi: the development package and the runtime that carries the launcher
    "openmpi-devel": ("5.0.9", "1"),
    "openmpi": ("5.0.9", "1"),
}

# the contents of each package
contents = {
    # the development artifacts, with libraries under {lib64}
    "gsl-devel": [
        "/usr/include/gsl/gsl_version.h",
        "/usr/lib64/libgsl.so",
        "/usr/lib64/libgslcblas.so",
    ],
    # the runtime carries only the versioned libraries
    "gsl": ["/usr/lib64/libgsl.so.28"],
    # the development artifacts, with the arch tagged include directory and the flavor home
    "openmpi-devel": [
        "/usr/include/openmpi-aarch64/mpi.h",
        "/usr/lib64/openmpi/lib/libmpi.so",
    ],
    # the runtime carries the launcher in the flavor home
    "openmpi": [
        "/usr/lib64/openmpi/bin/mpirun",
        "/usr/lib64/openmpi/lib/libmpi.so.40",
    ],
}


def test():
    """
    Configure gsl and mpi recipes against the canned database
    """
    # support
    import pyre

    # the engine to fake
    from pyre.platforms.Rpm import Rpm

    # the categories
    from pyre.externals.GSL import GSL
    from pyre.externals.MPI import MPI

    # an engine wired to the canned database instead of an rpm client
    class engine(Rpm):
        """
        An rpm engine over canned data
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

    # instantiate
    rpm = engine(name="rpm.fake")

    # get the gsl recipe
    recipe, *_ = GSL.recipes()
    # the development package must win the resolution
    assert rpm.resolve(recipe=recipe) == "gsl-devel"
    # interpret it
    values = rpm.configure(recipe=recipe)
    # the discovery must succeed
    assert values is not None
    # with the version from the lead
    assert values["version"] == "2.8"
    # the headers in the canonical include directory
    assert [str(f) for f in values["incdir"]] == ["/usr/include"]
    # the libraries under {lib64}
    assert [str(f) for f in values["libdir"]] == ["/usr/lib64"]
    # both stems resolve
    assert values["libraries"] == ["gsl", "gslcblas"]

    # get the openmpi recipe
    openmpi, *_ = MPI.recipes()
    # interpret it
    values = rpm.configure(recipe=openmpi)
    # the discovery must succeed
    assert values is not None
    # the headers in the arch tagged include directory
    assert [str(f) for f in values["incdir"]] == ["/usr/include/openmpi-aarch64"]
    # the library in the flavor home
    assert [str(f) for f in values["libdir"]] == ["/usr/lib64/openmpi/lib"]
    # and the launcher from the runtime companion
    assert values["launcher"] == "mpirun"
    assert [str(f) for f in values["bindir"]] == ["/usr/lib64/openmpi/bin"]

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file

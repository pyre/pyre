#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Exercise multi-package unions against a fake debian database

Debian splits logical packages into pieces: metapackages with no files, versioned {-dev}
packages with the headers and libraries, and sibling packages with the executables. The
engine must reject the empty leads, find the markers in the versioned packages, and fold in
the companions that carry the executables
"""

# the fake database, modeled on an actual ubuntu host
installed = {
    # metapackages: no files
    "python3-dev": ("3.13.7", "meta"),
    "libpython3-dev": ("3.13.7", "meta"),
    # the versioned development package: headers and the link library
    "libpython3.13-dev": ("3.13.7", "1"),
    # the runtime pieces
    "libpython3.13-stdlib": ("3.13.7", "1"),
    "python3.13": ("3.13.7", "1"),
    "python3.13-minimal": ("3.13.7", "1"),
    "python3.13-venv": ("3.13.7", "1"),
    # mpi: the development package and the launcher package
    "libopenmpi-dev": ("5.0.8", "1"),
    "openmpi-bin": ("5.0.8", "1"),
}

# the contents of each package
contents = {
    # nothing in the metapackages
    "python3-dev": [],
    "libpython3-dev": [],
    # the development artifacts
    "libpython3.13-dev": [
        "/usr/include/python3.13/Python.h",
        "/usr/lib/python3.13/config-3.13-x86_64-linux-gnu/libpython3.13.so",
    ],
    # runtime pieces without development value
    "libpython3.13-stdlib": ["/usr/lib/python3.13/os.py"],
    "python3.13": ["/usr/lib/python3.13/lib2to3"],
    "python3.13-minimal": ["/usr/bin/python3.13"],
    "python3.13-venv": ["/usr/lib/python3.13/venv"],
    # mpi
    "libopenmpi-dev": [
        "/usr/lib/x86_64-linux-gnu/openmpi/include/mpi.h",
        "/usr/lib/x86_64-linux-gnu/openmpi/lib/libmpi.so",
    ],
    "openmpi-bin": ["/usr/bin/mpirun.openmpi"],
}


def test():
    """
    Configure python and mpi recipes against the fake database
    """
    # support
    import pyre

    # the engine to fake
    from pyre.platforms.DPkg import DPkg

    # the categories
    from pyre.externals.Python import Python
    from pyre.externals.MPI import MPI

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

    # instantiate
    dpkg = engine(name="dpkg.fake")

    # get the python recipe
    recipe, *_ = Python.recipes()
    # the metapackage lead must be rejected in favor of the versioned package
    values = dpkg.configure(recipe=recipe)
    # the discovery must succeed
    assert values is not None
    # with the version from the winning lead
    assert values["version"] == "3.13.7"
    # the headers from the versioned development package
    assert [str(f) for f in values["incdir"]] == ["/usr/include/python3.13"]
    # the actual library stem
    assert values["libraries"] == ["python3.13"]
    # and the interpreter from the {python3.13-minimal} companion
    assert values["interpreter"] == "python3.13"
    assert [str(f) for f in values["bindir"]] == ["/usr/bin"]

    # get the openmpi recipe
    openmpi, *_ = MPI.recipes()
    # interpret it
    values = dpkg.configure(recipe=openmpi)
    # the discovery must succeed
    assert values is not None
    # the headers and libraries come from the lead
    assert values["libraries"] == ["mpi"]
    # and the launcher from the {openmpi-bin} companion
    assert values["launcher"] == "mpirun.openmpi"
    assert [str(f) for f in values["bindir"]] == ["/usr/bin"]

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file

#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
The debian toolkit split folds back together through the multi-package union
"""

# the fake database: the development artifacts and the compiler in separate packages
installed = {
    # the headers and the runtime
    "nvidia-cuda-dev": ("12.4.131", "1"),
    # the compiler driver
    "nvidia-cuda-toolkit": ("12.4.131", "1"),
}

# the contents of each package; the paths are anchored in the test fixture so that the
# configured directories exist and the installations validate
contents = {
    # the development artifacts
    "nvidia-cuda-dev": [
        "prefix/include/cuda_runtime.h",
        "prefix/lib/libcudart.dylib",
    ],
    # the compiler
    "nvidia-cuda-toolkit": ["prefix/bin/nvcc"],
}


def test():
    """
    Resolve cuda and verify all the pieces arrived
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
    index._engines = (engine(name="dpkg.fake.cuda.split"),)
    # resolve
    report = index.resolve(requested=["cuda"])
    # the toolkit was assembled from its pieces
    cuda = report.selections["cuda"]
    # the version comes from the lead
    assert cuda.version == "12.4.131"
    # the runtime resolved from the development package
    assert list(cuda.libraries) == ["cudart"]
    # and the compiler from its companion
    assert cuda.compiler == "nvcc"

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file

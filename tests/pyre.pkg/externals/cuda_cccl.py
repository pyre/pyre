#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
The cccl subtree of cuda 13 extends the include path, and its absence costs nothing
"""

# the fake cuda 13 database: the core libraries live in their own subtree
modern = {
    "installed": {
        # the development artifacts and the compiler
        "nvidia-cuda-dev": ("13.0.48", "1"),
        "nvidia-cuda-toolkit": ("13.0.48", "1"),
    },
    "contents": {
        # the runtime headers at the top, the core libraries under {cccl}
        "nvidia-cuda-dev": [
            "prefix/include/cuda_runtime.h",
            "prefix/include/cccl/thrust/version.h",
            "prefix/lib/libcudart.dylib",
        ],
        "nvidia-cuda-toolkit": ["prefix/bin/nvcc"],
    },
}

# the fake cuda 12 database: everything at the top, no {cccl}
legacy = {
    "installed": {
        # the development artifacts and the compiler
        "nvidia-cuda-dev": ("12.4.131", "1"),
        "nvidia-cuda-toolkit": ("12.4.131", "1"),
    },
    "contents": {
        # thrust sits directly under the include directory
        "nvidia-cuda-dev": [
            "prefix/include/cuda_runtime.h",
            "prefix/include/thrust/version.h",
            "prefix/lib/libcudart.dylib",
        ],
        "nvidia-cuda-toolkit": ["prefix/bin/nvcc"],
    },
}

# the fake minimal database: a runtime with no thrust at all
minimal = {
    "installed": {
        # just the development artifacts
        "nvidia-cuda-dev": ("13.0.48", "1"),
    },
    "contents": {
        # nothing but the runtime
        "nvidia-cuda-dev": [
            "prefix/include/cuda_runtime.h",
            "prefix/lib/libcudart.dylib",
        ],
    },
}


def engine(db, name):
    """
    Build a dpkg engine over the canned {db}
    """
    # the engine to fake
    from pyre.platforms.DPkg import DPkg

    # an engine wired to the fake database instead of a dpkg client
    class fake(DPkg):
        """
        A dpkg engine over canned data
        """

        # the installed package index
        def getInstalledPackages(self):
            """
            Serve the canned index
            """
            # easy enough
            return db["installed"]

        # package contents
        def retrievePackageContents(self, package):
            """
            Serve the canned contents
            """
            # easy enough
            yield from db["contents"][package]
            # all done
            return

    # instantiate
    return fake(name=name)


def test():
    """
    Interpret the cuda recipe against the three layouts
    """
    # the category
    from pyre.externals.supported.cuda.CUDA import CUDA

    # get the cuda recipe
    recipe, *_ = CUDA.recipes()

    # cuda 13: the {cccl} subtree joins the include path
    values = engine(modern, "dpkg.fake.cuda.modern").configure(recipe=recipe)
    # the discovery must succeed
    assert values is not None
    # with both header roots
    assert [str(f) for f in values["incdir"]] == ["prefix/include", "prefix/include/cccl"]

    # cuda 12: thrust at the top contributes nothing new
    values = engine(legacy, "dpkg.fake.cuda.legacy").configure(recipe=recipe)
    # the discovery must succeed
    assert values is not None
    # with the single header root
    assert [str(f) for f in values["incdir"]] == ["prefix/include"]

    # a runtime with no thrust: the optional marker must not veto
    values = engine(minimal, "dpkg.fake.cuda.minimal").configure(recipe=recipe)
    # the discovery must still succeed
    assert values is not None
    # with the single header root
    assert [str(f) for f in values["incdir"]] == ["prefix/include"]

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file

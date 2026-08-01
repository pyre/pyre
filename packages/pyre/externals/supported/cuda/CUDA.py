# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# access to the framework
import pyre

# superclasses
from ...Library import Library
from ...Tool import Tool

# the flavor description
from ...Recipe import Recipe


# the cuda package category
class CUDA(Tool, Library, family="pyre.externals.cuda"):
    """
    The CUDA toolkit: the compiler driver and the runtime
    """

    # constants
    category = "cuda"

    # user configurable state
    compiler = pyre.properties.str(default="nvcc")
    compiler.doc = "the name of the cuda compiler driver"

    # interface
    @classmethod
    def recipes(cls):
        """
        Generate the sequence of recipes for my known flavors

        The toolkit is shipped in pieces almost everywhere: debian splits the development
        artifacts from the compiler, and the nvidia/conda-forge channels shatter it into
        {cuda-*} fragments, some with versioned or arch-tagged names that only prefix
        matching can reach; the multi-package unions fold the pieces back together, and
        the contents-driven discovery absorbs the conda-forge {targets/<arch>} layout
        """
        # get the implementations
        from .Default import Default

        # there is only one flavor
        yield Recipe(
            # of this category
            category=cls.category,
            # realized by the generic installation
            factory=Default,
            # provable by the runtime header, wherever the layout puts it
            headers=("cuda_runtime.h",),
            # the cuda 13 {cccl} reorganization moved thrust, cub, and libcu++ into their
            # own subtree; its marker extends the include path when present, and older
            # toolkits that keep the headers at the top are not penalized
            extras=("thrust/version.h",),
            # the runtime is the only library every consumer needs; the rest of the
            # toolkit (cublas, cufft, ...) is configuration users add to {libraries}
            libraries=("cudart",),
            # the compiler driver, split off into its own package on most databases
            binaries={"compiler": "nvcc"},
            # the marker for the compile line
            defines=("WITH_CUDA",),
            # with database specific names where the category name isn't enough
            natives={
                # debian: the development artifacts, with the compiler riding along
                "dpkg": (("nvidia-cuda-dev", "nvidia-cuda-toolkit"),),
                # the nvidia rhel repo: versioned names, reachable by prefix
                "rpm": (("cuda-cudart-devel", "cuda-nvcc"),),
                # the nvidia and conda-forge channels: the runtime fragment leads, the
                # compiler and the core libraries ride along; the monolithic
                # {cudatoolkit} is the legacy fallback
                "conda": (("cuda-cudart-dev", "cuda-nvcc", "cuda-cccl"), "cudatoolkit"),
            },
        )
        # all done
        return


# end of file

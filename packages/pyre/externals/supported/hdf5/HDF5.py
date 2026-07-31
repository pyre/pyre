# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclasses
from ...Library import Library

# the flavor description
from ...Recipe import Recipe

# the content checks
from ...Proof import Proof


# the hdf5 package category
class HDF5(Library, family="pyre.externals.hdf5"):
    """
    The HDF5 data model and file format
    """

    # constants
    category = "hdf5"

    # interface
    @classmethod
    def recipes(cls):
        """
        Generate the sequence of recipes for my known flavors, in order of preference

        The flavor axis mirrors mm: serial first, so it stays preferred when several
        flavors are installed, then the mpi aware builds, each inducing a requirement on
        the matching mpi implementation so the two selections stay aligned
        """
        # get the implementations
        from .Default import Default
        from .OpenMPI import OpenMPI
        from .MPICH import MPICH

        # the serial flavor
        yield Recipe(
            # of this category
            category=cls.category,
            # answering to the serial tag
            tags=("serial",),
            # realized by the generic installation
            factory=Default,
            # provable by the top level header
            headers=("hdf5.h",),
            # contributing these libraries to the link line
            libraries=("hdf5_cpp", "hdf5"),
            # and this marker to the compile line
            defines=("WITH_HDF5",),
            # settled by the build configuration header, regardless of who packaged it:
            # a serial build must not be mpi aware, and it reveals its version
            proofs=(
                Proof(header="H5pubconf.h", pattern=r"#\s*define\s+H5_HAVE_PARALLEL\s+1", forbid=True),
                Proof(header="H5pubconf.h", pattern=r'#\s*define\s+H5_VERSION\s+"([^"]+)"', harvest="version"),
            ),
            # with database specific names where the category name isn't enough
            natives={
                "dpkg": ("libhdf5-dev",),
                "rpm": ("hdf5-devel",),
            },
        )
        # the openmpi flavor; the tag carries the instance name, qualified with the
        # category so it doesn't collide with the mpi selection in the configuration
        # store, while the tags carry the user facing vocabulary
        yield Recipe(
            # of this category
            category=cls.category,
            # the flavor tag
            flavor="hdf5-openmpi",
            # answering to the parallel class and the mpi implementation name
            tags=("parallel", "openmpi"),
            # realized by the openmpi installation
            factory=OpenMPI,
            # provable by the top level header, wherever the variant subdirectory puts it
            headers=("hdf5.h",),
            # contributing these libraries to the link line
            libraries=("hdf5_cpp", "hdf5"),
            # and this marker to the compile line
            defines=("WITH_HDF5",),
            # requiring the matching mpi implementation
            dependencies=("mpi[openmpi]",),
            # settled by the build configuration header, regardless of who packaged it:
            # conda and macports name every flavor {hdf5}, so the proof of mpi awareness
            # carries the whole classification there
            proofs=(
                Proof(header="H5pubconf.h", pattern=r"#\s*define\s+H5_HAVE_PARALLEL\s+1"),
                Proof(header="H5pubconf.h", pattern=r'#\s*define\s+H5_VERSION\s+"([^"]+)"', harvest="version"),
            ),
            # with database specific names where the flavor name isn't enough
            natives={
                "dpkg": ("libhdf5-openmpi-dev",),
                "rpm": ("hdf5-openmpi-devel",),
            },
        )
        # the mpich flavor
        yield Recipe(
            # of this category
            category=cls.category,
            # the flavor tag, qualified like its openmpi sibling
            flavor="hdf5-mpich",
            # answering to the parallel class and the mpi implementation name
            tags=("parallel", "mpich"),
            # realized by the mpich installation
            factory=MPICH,
            # provable by the top level header, wherever the variant subdirectory puts it
            headers=("hdf5.h",),
            # contributing these libraries to the link line
            libraries=("hdf5_cpp", "hdf5"),
            # and this marker to the compile line
            defines=("WITH_HDF5",),
            # requiring the matching mpi implementation
            dependencies=("mpi[mpich]",),
            # settled by the build configuration header, like its openmpi sibling
            proofs=(
                Proof(header="H5pubconf.h", pattern=r"#\s*define\s+H5_HAVE_PARALLEL\s+1"),
                Proof(header="H5pubconf.h", pattern=r'#\s*define\s+H5_VERSION\s+"([^"]+)"', harvest="version"),
            ),
            # with database specific names where the flavor name isn't enough
            natives={
                "dpkg": ("libhdf5-mpich-dev",),
                "rpm": ("hdf5-mpich-devel",),
            },
        )
        # all done
        return


# end of file

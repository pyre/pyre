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


# the mpi package category
class MPI(Tool, Library, family="pyre.externals.mpi"):
    """
    The message passing interface
    """

    # constants
    category = "mpi"

    # user configurable state
    launcher = pyre.properties.str(default="mpirun")
    launcher.doc = "the name of the launcher of parallel jobs"

    # interface
    @classmethod
    def recipes(cls):
        """
        Generate the sequence of recipes for my known flavors, in order of preference
        """
        # get the implementations
        from .OpenMPI import OpenMPI
        from .MPICH import MPICH

        # openmpi
        yield Recipe(
            # of this category
            category=cls.category,
            # the flavor tag
            flavor="openmpi",
            # realized by the openmpi installation
            factory=OpenMPI,
            # a selection group on package managers with alternatives
            group="mpi",
            # provable by the top level header
            headers=("mpi.h",),
            # contributing this library to the link line
            libraries=("mpi",),
            # the launcher executable, possibly decorated with the flavor
            binaries={"launcher": r"mpirun(\.openmpi)?"},
            # the markers for the compile line
            defines=("WITH_MPI", "WITH_OPENMPI"),
            # with database specific names where the flavor name isn't enough; debian and
            # fedora both split the launcher into runtime packages, so they ride along as
            # companions
            natives={
                "dpkg": (("libopenmpi-dev", "openmpi-bin"),),
                "rpm": (("openmpi-devel", "openmpi"),),
            },
        )
        # mpich
        yield Recipe(
            # of this category
            category=cls.category,
            # the flavor tag
            flavor="mpich",
            # realized by the mpich installation
            factory=MPICH,
            # a selection group on package managers with alternatives
            group="mpi",
            # provable by the top level header
            headers=("mpi.h",),
            # contributing this library to the link line
            libraries=("mpich",),
            # the launcher executable, possibly decorated with the flavor
            binaries={"launcher": r"mpirun(\.mpich)?"},
            # the markers for the compile line
            defines=("WITH_MPI", "WITH_MPICH"),
            # with database specific names where the flavor name isn't enough; debian and
            # fedora both split the launcher into the {mpich} runtime package, so it rides
            # along as a companion
            natives={
                "dpkg": (("libmpich-dev", "mpich"),),
                "rpm": (("mpich-devel", "mpich"),),
            },
        )
        # all done
        return


# end of file

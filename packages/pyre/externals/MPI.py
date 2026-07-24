# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# access to the framework
import pyre

# superclasses
from .Library import Library
from .LibraryInstallation import LibraryInstallation
from .Tool import Tool
from .ToolInstallation import ToolInstallation

# the flavor description
from .Recipe import Recipe


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
            # with database specific names where the flavor name isn't enough; debian splits
            # the launcher into {openmpi-bin}, so it rides along as a companion
            natives={"dpkg": (("libopenmpi-dev", "openmpi-bin"),)},
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
            # with database specific names where the flavor name isn't enough; debian splits
            # the launcher into the {mpich} runtime package, so it rides along as a companion
            natives={"dpkg": (("libmpich-dev", "mpich"),)},
        )
        # all done
        return


# the base implementation
class Default(
    ToolInstallation, LibraryInstallation, family="pyre.externals.mpi.default", implements=MPI
):
    """
    A generic MPI installation
    """

    # constants
    category = MPI.category
    flavor = category

    # user configurable state
    launcher = pyre.properties.str(default="mpirun")
    launcher.doc = "the name of the launcher of parallel jobs"


# the openmpi flavor
class OpenMPI(Default, family="pyre.externals.mpi.openmpi"):
    """
    An OpenMPI installation
    """

    # constants
    flavor = "openmpi"


# the mpich flavor
class MPICH(Default, family="pyre.externals.mpi.mpich"):
    """
    An MPICH installation
    """

    # constants
    flavor = "mpich"


# end of file

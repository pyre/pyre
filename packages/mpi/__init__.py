# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# bootstrapping
# the current default builds of openmpi on linux do not link their pluggins against libmpi
# so they all report unresolved symbols; the temporary fix is to change the way python
# dlopens our extension module so the mpi symbols go to the global namespace, where the
# pluggins will be able to find them. hopefully, the openmpi people will fix this soon
# LAST CHECKED: 20120423, revision 1402, openmpi 1.4.3
import sys

if sys.platform.startswith("linux"):
    # that's where the stupid flag value lives...
    import ctypes

    # adjust the {dlopen} flags
    sys.setdlopenflags(sys.getdlopenflags() | ctypes.RTLD_GLOBAL)

# we start out with {world} being a trivial communicator, so that code written against this
# package runs unchanged on a machine with no mpi at all; {init} replaces it with the real one
from .TrivialCommunicator import TrivialCommunicator

world = TrivialCommunicator()

# attempt to load the mpi extension
try:
    # try to load the bindings
    from . import libmpi
# treat any import failure as the absence of mpi: a relative {from . import libmpi} reports a
# missing binding as a plain {ImportError} rather than {ModuleNotFoundError}, and on some
# platforms a binding that is present can still fail to load for benign reasons; until we
# understand that platform behaviour, the safe reading of any failure here is "no mpi runtime"
except ImportError:
    # indicate that there is no runtime support
    libmpi = None

    # and that none of the entities the bindings publish are available
    communicator = None
    cartesian = None
    group = None
    port = None
# otherwise, we have bindings and hence MPI support
else:
    # grab the shell protocol from pyre
    from pyre import foundry, shells

    # the foundries for the shells in this package
    # the default shell is raw {mpirun}
    @foundry(implements=shells.shell)
    def mpirun():
        # get the class
        from .Launcher import Launcher

        # and return it
        return Launcher

    # support for SLURM
    @foundry(implements=shells.shell)
    def slurm():
        # get the class
        from .Slurm import Slurm

        # and return it
        return Slurm

    # the entities the bindings publish
    communicator = libmpi.Communicator
    cartesian = libmpi.Cartesian
    group = libmpi.Group
    port = libmpi.Port

    # the exception hierarchy; a failed mpi call raises one of these, rather than taking the
    # whole job down
    Error = libmpi.Error
    MPIError = libmpi.MPIError
    ShapeError = libmpi.ShapeError

    # the reduction operators, the outcome of a comparison, and the levels of thread support
    Op = libmpi.Op
    Comparison = libmpi.Comparison
    Thread = libmpi.Thread

    # the constants
    undefined = libmpi.undefined
    anySource = libmpi.anySource
    anyTag = libmpi.anyTag
    procNull = libmpi.procNull


# a flag that keeps us from asking the interpreter to shut mpi down more than once
_registered = False


def init(threads=None):
    """
    Initialize the runtime

    This cannot happen as a side effect of importing the package: a process may not fork and
    exec {mpirun} once it has called {MPI_Init}, and {openmpi} forbids it outright. So the
    launcher builds the parallel machine first, and the application calls this afterwards.

    {threads} names the level of thread support to ask for, as one of the {mpi.Thread} values.
    """
    # if we don't have runtime support
    if not libmpi:
        # bail
        return None

    # arrange for the runtime to be shut down when the interpreter exits, but only once, no
    # matter how many times we are called
    global _registered
    # if nobody has done it yet
    if not _registered:
        # get the exit hook
        import atexit

        # and plant our shutdown
        atexit.register(finalize)
        # so that we do not plant it twice
        _registered = True

    # bring mpi up, asking for whatever level of thread support the caller wants; asking twice
    # is harmless, since the runtime declines politely when mpi is already up
    libmpi.initialize() if threads is None else libmpi.initialize(required=threads)

    # replace the trivial communicator with the real one
    global world
    # now that there is a real one to be had
    world = libmpi.world()

    # hand back the bindings, so that callers can tell support apart from its absence
    return libmpi


def finalize() -> None:
    """
    Shutdown mpi
    """
    # if we don't have runtime support
    if not libmpi:
        # bail
        return

    # take mpi down; whatever communicators and groups are still alive may outlive this call
    # and be collected in any order, since a handle whose runtime is gone releases nothing
    libmpi.finalize()

    # all done
    return


# in any case, grab the framework
import pyre

# register the package
package = pyre.executive.registerPackage(name="mpi", file=__file__)
# record the layout
home, prefix, defaults = package.layout()

# the package meta-data
from . import meta


# administrative
def copyright():
    """
    Return the pyre copyright note
    """
    return print(meta.header)


def license():
    """
    Print the pyre license
    """
    # print it
    return print(meta.license)


def version():
    """
    Return the pyre version
    """
    return meta.version


def credits():
    """
    Print the acknowledgments
    """
    # print it
    return print(meta.acknowledgments)


# end of file

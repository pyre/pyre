# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2018 all rights reserved
#


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


# bootstrapping
# version info
from . import meta
# attempt to load the mpi extension
try:
    # the current default builds of openmpi on linux do not link their pluggins against libmpi
    # so they all report unresolved symbols; the temporary fix is to change the way python
    # dlopens our extension module so the mpi symbols go to the global namespace, where the
    # pluggins will be able to find them. hopefully, the openmpi people will fix this soon
    # LAST CHECKED: 20120423, revision 1402, openmpi 1.4.3
    import sys
    if sys.platform.startswith('linux'):
        # that's where the stupid flag value lives...
        import ctypes
        # adjust the {dlopen} flags
        sys.setdlopenflags(sys.getdlopenflags() | ctypes.RTLD_GLOBAL)
    # try to load the extension
    from . import mpi

# if it fails for any reason
except Exception:
    # build {world} out of a trivial communicator
    from .TrivialCommunicator import TrivialCommunicator as world
    # indicate that there is no runtime support
    mpi = None

# otherwise, we have bindings and hence MPI support
else:
    # register the finalization routine to happen when the interpreter exits
    import atexit
    atexit.register(mpi.finalize)

    # provide access to the extension through the base mpi object
    from .Object import Object
    Object.mpi = mpi
    # the communicator factory
    from .Communicator import Communicator as communicator
    # the group factory
    from .Group import Group as group
    # the port factory
    from .Port import Port as port

    # grab the shell protocol form pyre
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


    # build the world communicator
    world = communicator(mpi.world)

# in any case, grab the framework
import pyre
# register the package
package = pyre.executive.registerPackage(name='mpi', file=__file__)
# record the layout
home, prefix, defaults = package.layout()

# end of file

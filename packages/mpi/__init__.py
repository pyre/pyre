# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# attempt to load the mpi extension
try:
    from . import mpi

# if it fails for any reason
except Exception:
    # build {world} out of a trivial communicator
    from .TrivialCommunicator import TrivialCommunicator as world
    # set the number of processes
    processes = 1

# otherwise, we have bindings and hence MPI support
else:
    # access the communicator wrapper
    from .Communicator import Communicator as communicator
    # build world
    world = communicator(mpi.world)
    # set the number of processes
    processes = world.size


# administrative
def copyright():
    """
    Return the pyre mpi copyright note
    """
    return _mpi_copyright


def license():
    """
    Print the pyre mpi license
    """
    print(_mpi_license)
    return


def version():
    """
    Return the pyre mpi version
    """
    return _mpi_version


# license
_mpi_version = (1, 0, 0)

_mpi_copyright = "pyre mpi: Copyright (c) 1998-2011 Michael A.G. Aïvázis"

_mpi_license = """
    pyre mpi 1.0
    Copyright (c) 1998-2011 Michael A.G. Aïvázis
    All Rights Reserved


    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions
    are met:

    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.

    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in
      the documentation and/or other materials provided with the
      distribution.

    * Neither the name pyre nor the names of its contributors may be
      used to endorse or promote products derived from this software
      without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
    FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
    COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
    INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
    BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
    LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
    CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
    LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
    ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
    POSSIBILITY OF SUCH DAMAGE.
    """


# end of file 

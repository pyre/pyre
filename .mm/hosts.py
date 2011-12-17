# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#

# externals
import os


# the builder decorator
def host(builder):
    """
    Decorate the {builder} with host specific options
    """
    # get the host name
    name = builder.host.name
    # print('host:', name)

    # on asap.mit.edu
    if name == 'head.cluster':
        # no gsl
        builder.requirements['gsl'].environ = {}
        # set up mpi
        mpiHome = '/act/openmpi/gnu'
        mpiVersion = 'openmpi'
        builder.requirements['mpi'].environ = {
            'MPI_VERSION': mpiVersion,
            'MPI_DIR': mpiHome,
            'MPI_LIBDIR': os.path.join(mpiHome, 'lib'),
            'MPI_INCDIR': os.path.join(mpiHome, 'include'),
            'MPI_EXECUTIVE': 'mpirun',
            }
        # no postgres
        builder.requirements['libpq'].environ = {}
        # python 3.2 is in /usr/local
        pythonHome = '/usr/local'
        pythonVersion = '3.2'
        python = 'python' + pythonVersion
        builder.requirements['python'].environ = {
            'PYTHON': python,
            'PYTHON_PYCFLAGS': '-b',
            'PYTHON_DIR': pythonHome,
            'PYTHON_LIBDIR': os.path.join(pythonHome, 'lib', python),
            'PYTHON_INCDIR': os.path.join(pythonHome, 'include', python+'m'),
            }

        # all done
        return builder

    # for all other hosts
    return builder


# end of file 

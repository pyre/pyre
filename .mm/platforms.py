# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


import os


def platform(builder):
    """
    Decorate the {builder} with platform specific options
    """
    # get the platform id
    platform = builder.host.system
    # print('platform:', platform)

    # on darwin
    if platform == 'Darwin':
        # assume macports
        systemdir = '/opt/local'
        # set up {gsl}
        builder.requirements['gsl'].environ = {
            'GSL_DIR': systemdir,
            'GSL_LIBDIR': os.path.join(systemdir, 'lib'),
            'GSL_INCDIR': os.path.join(systemdir, 'include'),
            }
        # set up {libpq}
        libpqVersion = 'postgresql91'
        builder.requirements['libpq'].environ = {
            'LIBPQ_DIR': systemdir,
            'LIBPQ_LIBDIR': os.path.join(systemdir, 'lib', libpqVersion),
            'LIBPQ_INCDIR': os.path.join(systemdir, 'include', libpqVersion),
            }
        # set up {mpi}
        mpiVersion = 'openmpi'
        builder.requirements['mpi'].environ = {
            'MPI_VERSION': mpiVersion,
            'MPI_DIR': systemdir,
            'MPI_LIBDIR': os.path.join(systemdir, 'lib'),
            'MPI_INCDIR': os.path.join(systemdir, 'include', mpiVersion),
            'MPI_EXECUTIVE': 'openmpirun',
            }
        # set up {python}
        pythonVersion = '3.3'
        python = 'python' + pythonVersion
        builder.requirements['python'].environ = {
            'PYTHON': python,
            'PYTHON_PYCFLAGS': '-b',
            'PYTHON_DIR': systemdir,
            'PYTHON_LIBDIR': os.path.join(systemdir, 'lib', python),
            'PYTHON_INCDIR': os.path.join(systemdir, 'include', python),
            }
        # all done
        return builder

    # on linux
    if platform == 'Linux':
        # on normal distributions
        systemdir = '/usr'
        # set up {gsl}
        builder.requirements['gsl'].environ = {
            'GSL_DIR': systemdir,
            'GSL_LIBDIR': os.path.join(systemdir, 'lib'),
            'GSL_INCDIR': os.path.join(systemdir, 'include'),
            }
        # set up {libpq}
        libpqVersion = '9.1'
        builder.requirements['libpq'].environ = {
            'LIBPQ_DIR': systemdir,
            'LIBPQ_INCDIR': os.path.join(systemdir, 'include', 'postgresql'),
            'LIBPQ_LIBDIR': os.path.join(systemdir, 'lib'),
            }
        # set up {mpi}
        mpiVersion = 'openmpi'
        builder.requirements['mpi'].environ = {
            'MPI_VERSION': mpiVersion,
            'MPI_DIR': systemdir,
            'MPI_LIBDIR': os.path.join(systemdir, 'lib'),
            'MPI_INCDIR': os.path.join(systemdir, 'include', mpiVersion),
            'MPI_EXECUTIVE': 'mpirun',
            }
        # set up {python}
        pythonVersion = '3.3'
        python = 'python' + pythonVersion
        builder.requirements['python'].environ = {
            'PYTHON': python,
            'PYTHON_PYCFLAGS': '-b',
            'PYTHON_DIR': systemdir,
            'PYTHON_LIBDIR': os.path.join(systemdir, 'lib', python),
            'PYTHON_INCDIR': os.path.join(systemdir, 'include', python),
            }
        # all done
        return builder

    # on all other platforms
    return builder


# end of file 

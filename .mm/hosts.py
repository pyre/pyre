# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#

# externals
import os
import re


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

    # on shc.cacr.caltech.edu
    if name.startswith('shc'):
        systemdir = '/usr'
        # set up {gsl}
        gslHome = os.environ['GSL_HOME']
        builder.requirements['gsl'].environ = {
            'GSL_DIR': gslHome,
            'GSL_LIBDIR': os.path.join(gslHome, 'lib'),
            'GSL_INCDIR': os.path.join(gslHome, 'include'),
            }
        # no {libpq}
        builder.requirements['libpq'].environ = {}
        # set up {mpi}
        mpiVersion = 'openmpi'
        mpiHome = os.environ['OPENMPI_HOME']
        builder.requirements['mpi'].environ = {
            'MPI_VERSION': mpiVersion,
            'MPI_DIR': mpiHome,
            'MPI_BINDIR': os.path.join(mpiHome, 'bin'),
            'MPI_LIBDIR': os.path.join(mpiHome, 'lib'),
            'MPI_INCDIR': os.path.join(mpiHome, 'include'),
            'MPI_EXECUTIVE': 'mpirun',
            }
        # set up {python}
        pythonVersion = '3.2'
        python = 'python' + pythonVersion
        pythonHome = '/usr/local/python-3.2.2'
        builder.requirements['python'].environ = {
            'PYTHON': python,
            'PYTHON_PYCFLAGS': '-b',
            'PYTHON_DIR': pythonHome,
            # 'PYTHON_LIBDIR': os.path.join(pythonHome, 'lib', python),
            'PYTHON_INCDIR': os.path.join(pythonHome, 'include', python+'m'),
            }
        # all done
        return builder
        
    # on fram.gps.caltech.edu
    if re.match(r"(login|compute)-[0-9]+-[0-9]+.local", name):
        # print("fram.gps.caltech.edu")
        # set up {gsl}
        gslVersion = '1.15'
        gslHome = os.path.join('/opt/gsl', gslVersion)
        builder.requirements['gsl'].environ = {
            'GSL_DIR': gslHome,
            'GSL_LIBDIR': os.path.join(gslHome, 'lib'),
            'GSL_INCDIR': os.path.join(gslHome, 'include'),
            }
        # no {libpq}
        builder.requirements['libpq'].environ = {}
        # set up {mpi}
        mpiVersion = 'openmpi'
        mpiHome = '/opt/mpi/gcc46/openmpi-1.5.4'
        builder.requirements['mpi'].environ = {
            'MPI_VERSION': mpiVersion,
            'MPI_DIR': mpiHome,
            'MPI_BINDIR': os.path.join(mpiHome, 'bin'),
            'MPI_LIBDIR': os.path.join(mpiHome, 'lib64'),
            'MPI_INCDIR': os.path.join(mpiHome, 'include'),
            'MPI_EXECUTIVE': 'mpirun',
            }
        # set up {python}
        pythonVersion = '3.2'
        python = 'python' + pythonVersion
        pythonHome = '/opt/python'
        builder.requirements['python'].environ = {
            'PYTHON': python,
            'PYTHON_PYCFLAGS': '-b',
            'PYTHON_DIR': pythonHome,
            'PYTHON_LIBDIR': os.path.join(pythonHome, 'lib'),
            'PYTHON_INCDIR': os.path.join(pythonHome, 'include', python+'m'),
            }
        # all done
        return builder
        
    # for all other hosts
    return builder


# end of file 

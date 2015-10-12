# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2015 all rights reserved
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
        systemlibdir = os.path.join(systemdir, 'lib')
        systemincdir = os.path.join(systemdir, 'include')

        # do we have {gsl}?
        haveGSL = (
            os.path.isfile(os.path.join(systemlibdir, 'libgsl.dylib'))
            and
            os.path.isdir(os.path.join(systemincdir, 'gsl'))
            )
        # if yes
        if haveGSL:
            # get it
            gsl = builder.requirements['gsl']
            # set it up
            gsl.environ = {
                'GSL_DIR': systemdir,
                'GSL_LIBDIR': systemlibdir,
                'GSL_INCDIR': systemincdir
                }
            # and its runtime
            gsl.ldpath = systemlibdir

        # set up {libpq}
        libpqVersion = 'postgresql94'
        # do we have postgres?
        havePostgres = (
            os.path.isdir(os.path.join(systemlibdir, libpqVersion))
            and
            os.path.isdir(os.path.join(systemincdir, libpqVersion))
            )
        # if yes
        if havePostgres:
            # grab it
            libpq = builder.requirements['libpq']
            # set it up
            libpq.environ = {
                'LIBPQ_DIR': systemdir,
                'LIBPQ_LIBDIR': os.path.join(systemlibdir, libpqVersion),
                'LIBPQ_INCDIR': os.path.join(systemincdir, libpqVersion),
                }
            # and its runtime
            libpq.ldpath = os.path.join(systemincdir, libpqVersion)

        # set up {mpi}
        mpiVersion = 'openmpi-gcc5'
        # do we have {mpi}?
        haveMPI = (
            os.path.isdir(os.path.join(systemlibdir, mpiVersion))
            and
            os.path.isdir(os.path.join(systemincdir, mpiVersion))
            )
        # if yes
        if haveMPI:
            # grab it
            mpi = builder.requirements['mpi']
            # set it up
            mpi.environ = {
                'MPI_VERSION': mpiVersion,
                'MPI_DIR': systemdir,
                'MPI_LIBDIR': os.path.join(systemlibdir, mpiVersion),
                'MPI_INCDIR': os.path.join(systemincdir, mpiVersion),
                'MPI_EXECUTIVE': 'mpirun',
                }
            # and its runtime
            mpi.path = os.path.join(systemdir, 'bin')
            mpi.ldpath = systemlibdir

        # set up {python}
        pythonVersion = '3.5'
        pythonMemoryModel = 'm'
        python = 'python' + pythonVersion
        pythonHome = os.path.join(
            systemdir, 'Library/Frameworks/Python.framework/Versions', pythonVersion)
        builder.requirements['python'].environ = {
            'PYTHON': python,
            'PYTHON_PYCFLAGS': '-b',
            'PYTHON_DIR': systemdir,
            'PYTHON_LIBDIR': os.path.join(pythonHome, 'lib'),
            'PYTHON_INCDIR': os.path.join(pythonHome, 'include', python+pythonMemoryModel),
            }

        # the cuda version
        cudaVersion = '5.0'
        # cuda lives elsewhere
        cudaHome = '/Developer/NVIDIA/CUDA-{}'.format(cudaVersion)
        # is it there?
        haveCUDA = os.path.exists(cudaHome)
        # if yes
        if haveCUDA:
            # get it
            cuda = builder.requirements['cuda']
            # set it up
            cuda.environ = {
                'CUDA_DIR': cudaHome,
                'CUDA_INCDIR': os.path.join(cudaHome, 'include'),
                'CUDA_LIBDIR': os.path.join(cudaHome, 'lib')
                }
            # runtime
            cuda.path = os.path.join(cudaHome, 'bin')
            cuda.ldpath = os.path.join(cudaHome, 'lib')

        # all done
        return builder

    # on linux
    if platform == 'Linux':
        # on normal distributions
        systemdir = '/usr'
        systemlibdir = os.path.join(systemdir, 'lib')
        systemincdir = os.path.join(systemdir, 'include')

        # do we have {gsl}?
        haveGSL = (
            os.path.isfile(os.path.join(systemlibdir, 'libgsl.so'))
            and
            os.path.isdir(os.path.join(systemincdir, 'gsl'))
            )
        # if yes
        if haveGSL:
            # get it
            gsl = builder.requirements['gsl']
            # set it up
            gsl.environ = {
                'GSL_DIR': systemdir,
                'GSL_LIBDIR': systemlibdir,
                'GSL_INCDIR': systemincdir,
                }
            # and its runtime
            gsl.ldpath = systemlibdir

        # set up {libpq}
        libpqVersion = 'postgresql'
        # do we have postgres?
        havePostgres = (
            os.path.isfile(os.path.join(systemlibdir, 'libpq.so'))
            and
            os.path.isdir(os.path.join(systemincdir, libpqVersion))
            )
        # if yes
        if havePostgres:
            # grab it
            libpq = builder.requirements['libpq']
            # set it up
            libpq.environ = {
                'LIBPQ_DIR': systemdir,
                'LIBPQ_INCDIR': os.path.join(systemincdir, libpqVersion),
                'LIBPQ_LIBDIR': systemlibdir,
            }
            # and its runtime
            libpq.ldpath = os.path.join(systemincdir, libpqVersion)

        # set up {mpi}
        mpiVersion = 'openmpi'
        # do we have {mpi}?
        haveMPI = (
            os.path.isdir(os.path.join(systemlibdir, mpiVersion))
            and
            os.path.isdir(os.path.join(systemincdir, mpiVersion))
            )
        # if yes
        if haveMPI:
            # grab it
            mpi = builder.requirements['mpi']
            # set it up
            mpi.environ = {
                'MPI_VERSION': mpiVersion,
                'MPI_DIR': systemdir,
                'MPI_LIBDIR': os.path.join(systemdir, 'lib'),
                'MPI_INCDIR': os.path.join(systemdir, 'include', mpiVersion),
                'MPI_EXECUTIVE': 'mpirun',
                }
            # and its runtime
            mpi.path = os.path.join(systemdir, 'bin')
            mpi.ldpath = systemlibdir

        # set up {python}
        pythonVersion = '3.4'
        python = 'python' + pythonVersion
        builder.requirements['python'].environ = {
            'PYTHON': python,
            'PYTHON_PYCFLAGS': '-b',
            'PYTHON_DIR': systemdir,
            'PYTHON_LIBDIR': os.path.join(systemdir, 'lib', python),
            'PYTHON_INCDIR': os.path.join(systemdir, 'include', python),
            }

        # is it there?
        haveCUDA = (
            os.path.isfile(os.path.join(systemincdir, 'cuda.h'))
            )
        # if yes
        if haveCUDA:
            # get it
            cuda = builder.requirements['cuda']
            # set it up
            cuda.environ = {
                'CUDA_DIR': systemdir,
                'CUDA_INCDIR': systemincdir,
                'CUDA_LIBDIR': systemlibdir
                }
            # runtime
            cuda.path = os.path.join(systemdir, 'bin')
            cuda.ldpath = os.path.join(systemdir, 'lib')

        # all done
        return builder

    # on all other platforms
    return builder


# end of file

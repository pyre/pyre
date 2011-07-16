#!/bin/bash
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#

# set up a branch-aware build environment

# get the branch nickname
nickname=$(bzr nick)
echo "setting up development for '${nickname}'"

# set up the build system
export DV_DIR=${HOME}/dv # the source directory
export BLD_CONFIG=${DV_DIR}/config # the home of config
export GNU_MAKE=make # use gnu make
export MM_STOP=1 # stop on all errors
export LOGTAGS=on # turn mm logtags on
export TARGET=shared,debug,mpi # the default build target

# redirect the build temporary files 
export BLD_ROOT=${DV_DIR}/builds/${nickname}
echo "    building in '${BLD_ROOT}'"

# create the directory if it doesn't already exist
if [ ! -d ${BLD_ROOT} ]; then
    echo "    creating '${BLD_ROOT}'"
    mkdir -p ${BLD_ROOT}
fi

# the installation directory
export EXPORT_ROOT=${USER_TOOLS_DIR}/${nickname}
echo "    deploying at '${EXPORT_ROOT}'"

# adjust the python path
export PYTHONPATH=${EXPORT_ROOT}
# adjust the path
export PATH=${EXPORT_ROOT}/bin:${BLD_CONFIG}/make:${PATH}
# and the location of the shared objects
export LD_LIBRARY_PATH=${EXPORT_ROOT}/lib:${LD_LIBRARY_PATH}

# end of file

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

# the source directory
  export DV_DIR=${HOME}/dv
  export BLD_CONFIG=${DV_DIR}/config
  export BLD_ROOT=${DV_DIR}/builds/${nickname}
  echo "    building in '${BLD_ROOT}'"
  # create the directory if it doesn't already exist
  if [ ! -d ${BLD_ROOT} ]; then
      echo "    creating '${BLD_ROOT}'"
      mkdir -p ${BLD_ROOT}
  fi

# the installation directory
  export PYRE_DIR=${USER_TOOLS_DIR}/${nickname}
  export EXPORT_ROOT=${PYRE_DIR}
  echo "    deploying at '${EXPORT_ROOT}'"
  export PYTHONPATH=${EXPORT_ROOT}

# adjust the path
  export PATH=${BLD_CONFIG}/make:${PYRE_DIR}/bin:${PATH}
# and the location of the shared objects
  export LD_LIBRARY_PATH=${EXPORT_ROOT}/lib:${LD_LIBRARY_PATH}

# end of file

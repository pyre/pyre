#!/bin/bash
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#

# set up a branch-aware build environment

# get the branch nickname
  nickname=$(bzr nick)
  echo "setting up development for '${nickname}'"

# the source directory
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
  export PYTHONPATH=${EXPORT_ROOT}/packages

# adjust the path
  export PATH=${PATH}:${PYRE_DIR}/bin

# end of file

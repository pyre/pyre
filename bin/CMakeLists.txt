# -*- cmake -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#

# copy all the configuration files to the install directory
install(
  FILES pyre pyre-config merlin smith.pyre
  DESTINATION ${CMAKE_INSTALL_PREFIX}/bin
  )

# end of file

# -*- cmake -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#

# the pyre enhanced interpreter
add_executable(python.pyre)
# its sources
target_sources(python.pyre PRIVATE
  python.cc
  )
# and libraries
target_link_libraries(python.pyre Python3::Python)

# install the custom python
install(
  TARGETS python.pyre
  RUNTIME
  DESTINATION bin
  )
# install the scripts
install(
  PROGRAMS pyre pyre-config merlin smith.pyre
  DESTINATION bin
  )

# end of file

# -*- cmake -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#

# pyre
# stage into the build area
file(COPY pyre DESTINATION ${PYRE_STAGING_PACKAGES})
# install
install(DIRECTORY pyre DESTINATION ${PYRE_DEST_PACAKGES})

# show me
message("++ in pyre/packages:")
message("++   CMAKE_CURRENT_SOURCE_DIR: ${CMAKE_CURRENT_SOURCE_DIR}")
message("++   CMAKE_CURRENT_BINARY_DIR: ${CMAKE_CURRENT_BINARY_DIR}")


# end of file

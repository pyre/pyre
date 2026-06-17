# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# build the postgres package
function(pyre_postgresPackage)
  # if we have postgres
  if(PostgreSQL_FOUND)
    # install the sources straight from the source directory
    install(
      DIRECTORY packages/postgres
      DESTINATION ${PYRE_DEST_PACKAGES}
      FILES_MATCHING PATTERN *.py
      )
  endif()
  # all done
endfunction(pyre_postgresPackage)


# build the postgres module
function(pyre_postgresModule)
  # if we have postgres
  if(PostgreSQL_FOUND)
    Python_add_library(postgresmodule MODULE WITH_SOABI)
    # adjust the name to match what python expects
    set_target_properties(postgresmodule PROPERTIES LIBRARY_OUTPUT_NAME postgres)
    # specify the directory for the module compilation products
    pyre_library_directory(postgresmodule extensions)
    # set the libraries to link against; PostgreSQL::PostgreSQL carries include dirs and lib paths
    target_link_libraries(
      postgresmodule PRIVATE
      PostgreSQL::PostgreSQL pyre journal
      )
    # add the sources
    target_sources(postgresmodule PRIVATE
      extensions/postgres/postgres.cc
      extensions/postgres/connection.cc
      extensions/postgres/execute.cc
      extensions/postgres/exceptions.cc
      extensions/postgres/interlayer.cc
      extensions/postgres/metadata.cc
      )

    # install the extension
    install(
      TARGETS postgresmodule
      LIBRARY
      DESTINATION ${PYRE_DEST_PACKAGES}/pyre/extensions
      )
  endif()
  # all done
endfunction(pyre_postgresModule)


# end of file

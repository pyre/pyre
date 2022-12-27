# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# build the postgres module
function(pyre_postgresModule)
  # if we have postgres
  if (${PostgreSQL_FOUND})
    Python_add_library(postgresmodule MODULE)
    # adjust the name to match what python expects
    set_target_properties(postgresmodule PROPERTIES LIBRARY_OUTPUT_NAME postgres)
    set_target_properties(postgresmodule PROPERTIES SUFFIX ${PYTHON3_SUFFIX})
    # set the include directories
    target_include_directories(postgresmodule PRIVATE ${PostgreSQL_INCLUDE_DIRS})
    # set the link directories
    target_link_directories(postgresmodule PRIVATE ${PostgreSQL_LIBRARY_DIRS})
    # set the libraries to link against
    target_link_libraries(
      postgresmodule PRIVATE
      ${PostgreSQL_LIBRARIES} pyre journal
      )
    # add the sources
    target_sources(postgresmodule PRIVATE
      postgres/postgres.cc
      postgres/connection.cc
      postgres/execute.cc
      postgres/exceptions.cc
      postgres/interlayer.cc
      postgres/metadata.cc
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

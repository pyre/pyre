# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the pyre::postgres headers
function(pyre_postgresLib)
  # if we have postgres
  if(PostgreSQL_FOUND)
    # copy the postgres headers, staging them under the {pyre} namespace so they never collide
    # in a shared prefix
    file(GLOB_RECURSE files
         RELATIVE ${CMAKE_CURRENT_SOURCE_DIR}/lib/postgres
         CONFIGURE_DEPENDS
         lib/postgres/*.h lib/postgres/*.icc
         )
    foreach(file ${files})
      # skip the gateway header, which is deposited one level up
      if("${file}" STREQUAL "postgres.h")
        continue()
      endif()
      configure_file(lib/postgres/${file} lib/pyre/postgres/${file} COPYONLY)
    endforeach()

    # and the gateway header, as {pyre/postgres.h}
    configure_file(lib/postgres/postgres.h lib/pyre/postgres.h COPYONLY)

    # the postgres target (INTERFACE since it is header-only)
    add_library(postgres INTERFACE)
    # specify the directory for the library compilation products
    pyre_library_directory(postgres lib)
    # it stands on its own over libpq, and leans on journal for its diagnostics
    target_link_libraries(postgres INTERFACE pyre journal ${PostgreSQL_LIBRARIES})
    target_include_directories(postgres INTERFACE
      $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}/lib>
      $<BUILD_INTERFACE:${PostgreSQL_INCLUDE_DIRS}>
      $<INSTALL_INTERFACE:${PYRE_DEST_INCLUDE}>
      )
    add_library(pyre::postgres ALIAS postgres)

  endif(PostgreSQL_FOUND)
  # all done
endfunction(pyre_postgresLib)


# build the postgres module
function(pyre_postgresModule)
  # if we have postgres
  if (PostgreSQL_FOUND)
    Python_add_library(postgresmodule MODULE WITH_SOABI)
    # adjust the name to match what python expects; the module is {postgres}, and it lands in
    # {pyre.extensions}, where the package imports it as {libpq}
    set_target_properties(postgresmodule PROPERTIES LIBRARY_OUTPUT_NAME postgres)
    # specify the directory for the module compilation products
    pyre_library_directory(postgresmodule extensions)
    # link against the header-only library, which drags in libpq and journal
    target_link_libraries(
      postgresmodule PRIVATE pyre::postgres pybind11::module
      )
    # add the sources
    target_sources(postgresmodule PRIVATE
      extensions/postgres/__init__.cc
      extensions/postgres/Connection.cc
      extensions/postgres/Diagnostic.cc
      extensions/postgres/Field.cc
      extensions/postgres/Notification.cc
      extensions/postgres/Result.cc
      extensions/postgres/Row.cc
      extensions/postgres/Transaction.cc
      extensions/postgres/enums.cc
      extensions/postgres/exceptions.cc
      extensions/postgres/utilities.cc
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

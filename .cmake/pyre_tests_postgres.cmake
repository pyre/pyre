# -*- cmake -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the tests that run a postgres cluster need the server programs; the distributions keep them in
# directories named after the major version of the server, so look there too, the newest first
file(GLOB PYRE_POSTGRES_CANDIDATES /usr/lib/postgresql/*/bin /opt/local/lib/postgresql*/bin)
# put the newest first
list(SORT PYRE_POSTGRES_CANDIDATES COMPARE NATURAL ORDER DESCENDING)
# find the program that makes a cluster; {-DPYRE_POSTGRES_INITDB=...} picks another
find_program(PYRE_POSTGRES_INITDB initdb PATHS ${PYRE_POSTGRES_CANDIDATES})

# the clusters can run when both programs are in the same directory
set(PYRE_POSTGRES_CLUSTERS OFF)
# so, if there is an {initdb}
if(PYRE_POSTGRES_INITDB)
  # its directory holds the server programs
  get_filename_component(PYRE_POSTGRES_BIN ${PYRE_POSTGRES_INITDB} DIRECTORY)
  # the server refuses to run as root, so find out who is building
  execute_process(COMMAND id -u OUTPUT_VARIABLE PYRE_POSTGRES_UID OUTPUT_STRIP_TRAILING_WHITESPACE)
  # and when {pg_ctl} is there too
  if(EXISTS ${PYRE_POSTGRES_BIN}/pg_ctl)
    # a build that runs as root has no use for the programs
    if(PYRE_POSTGRES_UID STREQUAL "0")
      # so say why there are no tests that run a cluster
      message(STATUS "the postgres server does not run as root, "
        "so the tests that run a postgres cluster are not registered")
    # the tests can make the environment of their cluster only with ctest 3.22 or later, which
    # can remove a variable from it
    elseif(CMAKE_VERSION VERSION_LESS 3.22)
      # so say why there are none
      message(STATUS "cmake ${CMAKE_VERSION} cannot remove a variable from the environment of "
        "a test, so the tests that run a postgres cluster are not registered")
    # otherwise
    else()
      # they can run
      set(PYRE_POSTGRES_CLUSTERS ON)
    endif()
  # without {pg_ctl}
  else()
    # say why there are none
    message(STATUS "there is no pg_ctl beside ${PYRE_POSTGRES_INITDB}, "
      "so the tests that run a postgres cluster are not registered")
  endif()
# without {initdb}
else()
  # say why there are none
  message(STATUS "there is no initdb, so the tests that run a postgres cluster are not registered")
endif()


# run the tests of the postgres {suite} on a cluster of their own: a test before the first of
# them makes the cluster and starts its server, a test after the last one removes it, and every
# test of the suite talks to that server and no other
function(pyre_test_postgres_cluster suite)
  # the cluster lives in the build tree
  set(data ${PROJECT_BINARY_DIR}/pyre-postgres/${suite}/cluster)
  # its socket lives in a short directory named after the cluster, since the path of a socket is
  # limited to about a hundred characters
  string(MD5 digest ${data})
  # eight hex digits of the digest are enough to tell the clusters apart
  string(SUBSTRING ${digest} 0 8 tag)
  # assemble the directory of the socket
  set(socket /tmp/pyre-${tag})
  # the settings of the cluster
  set(settings
    --cluster.programs=${PYRE_POSTGRES_BIN}
    --cluster.data=${data}
    --cluster.socket=${socket}
    --cluster.user=pyre
    --cluster.locale=C
    --cluster.durable=no
    )
  # the fixture is named after the suite
  set(fixture pyre-postgres.${suite})

  # make the cluster, replacing any that an earlier run left behind, and start its server
  add_test(NAME ${fixture}.start
    COMMAND ${Python_EXECUTABLE} ${PROJECT_SOURCE_DIR}/bin/pyre-postgres restart ${settings}
    )
  # with the installed pyre
  set_property(TEST ${fixture}.start PROPERTY ENVIRONMENT
    PYTHONPATH=${PYRE_DEST_FULL_PACKAGES}
    )
  # before any test of the suite
  set_property(TEST ${fixture}.start PROPERTY FIXTURES_SETUP ${fixture})

  # remove the cluster
  add_test(NAME ${fixture}.stop
    COMMAND ${Python_EXECUTABLE} ${PROJECT_SOURCE_DIR}/bin/pyre-postgres remove ${settings}
    )
  # with the installed pyre
  set_property(TEST ${fixture}.stop PROPERTY ENVIRONMENT
    PYTHONPATH=${PYRE_DEST_FULL_PACKAGES}
    )
  # after every test of the suite, whether they passed or not
  set_property(TEST ${fixture}.stop PROPERTY FIXTURES_CLEANUP ${fixture})

  # the tests of the suite are named after its directory
  get_property(tests DIRECTORY PROPERTY TESTS)
  # so pick them out
  list(FILTER tests INCLUDE REGEX "^tests\\.postgres\\.${suite}\\.")
  # and for each one
  foreach(test ${tests})
    # wait for the cluster
    set_property(TEST ${test} APPEND PROPERTY FIXTURES_REQUIRED ${fixture})
    # talk to its server
    set_property(TEST ${test} APPEND PROPERTY ENVIRONMENT
      PGHOST=${socket} PGPORT=5432 PGUSER=pyre
      )
    # and to no other
    set_property(TEST ${test} APPEND PROPERTY ENVIRONMENT_MODIFICATION
      PGDATABASE=unset: PGPASSWORD=unset: PGSERVICE=unset: PGHOSTADDR=unset:
      )
  endforeach()

  # all done
endfunction()


# end of file

# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# register a postgres library test driver
#
# the plain {pyre_test_driver} links against {pyre} and {journal} only; these drivers also need
# the header-only {pyre::postgres} library, which drags in libpq
function(pyre_test_driver_postgres testfile)
  # generate the name of the testcase
  pyre_test_testcase(testname ${testfile})
  # generate the name of the target
  pyre_target(target ${testfile})

  # schedule it to be compiled
  add_executable(${target} ${testfile})
  # with some macros
  target_compile_definitions(${target} PRIVATE PYRE_CORE)
  # link against the postgres layer, which brings pyre, journal and libpq along
  target_link_libraries(${target} PUBLIC pyre::postgres)

  # make it a test case
  add_test(NAME ${testname} COMMAND ${target})
  # specify the directory for the target compilation products
  pyre_target_directory(${target} tests)

  # all done
endfunction()


# the postgres library tests; each stands on its own over libpq, and none of them loads python
pyre_test_driver_postgres(tests/postgres.lib/sanity.cc)
pyre_test_driver_postgres(tests/postgres.lib/connect.cc)
pyre_test_driver_postgres(tests/postgres.lib/exec.cc)
pyre_test_driver_postgres(tests/postgres.lib/codecs.cc)
pyre_test_driver_postgres(tests/postgres.lib/errors.cc)
pyre_test_driver_postgres(tests/postgres.lib/transaction.cc)
pyre_test_driver_postgres(tests/postgres.lib/async.cc)


# end of file

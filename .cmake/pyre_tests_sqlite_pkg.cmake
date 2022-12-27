# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


#
# sqlite capability tests
#
pyre_test_python_testcase(sqlite.pkg/sanity.py)
pyre_test_python_testcase(sqlite.pkg/sqlite_database.py)
pyre_test_python_testcase(sqlite.pkg/sqlite_attach.py)
pyre_test_python_testcase(sqlite.pkg/sqlite_table.py)
pyre_test_python_testcase(sqlite.pkg/sqlite_references.py)
# cleanup
add_test(NAME sqlite.clean
  WORKING_DIRECTORY "${PYRE_TESTSUITE_DIR}/sqlite.pkg"
  COMMAND ${BASH_PROGRAM} -c "rm pyre.sql")

# make the fixture
set_property(TEST sqlite.pkg.sqlite_attach.py PROPERTY
  FIXTURES_SETUP SQLITE)
set_property(TEST sqlite.clean PROPERTY
  FIXTURES_CLEANUP SQLITE)

# set up the dependencies
set_property(TEST sqlite.pkg.sqlite_table.py PROPERTY
  FIXTURES_REQUIRED SQLITE)

set_property(TEST sqlite.pkg.sqlite_references.py PROPERTY
  FIXTURES_REQUIRED SQLITE)


# end of file

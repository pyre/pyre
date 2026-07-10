# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


#
# postgres capability tests
#
# sanity
pyre_test_python_testcase(tests/postgres.ext/sanity.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_sanity.py)
# the low level interface, over the pybind11 bindings
pyre_test_python_testcase(tests/postgres.ext/libpq_connect.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_execute.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_exceptions.py)
pyre_test_python_testcase(tests/postgres.ext/libpq_async.py)

# components
pyre_test_python_testcase(tests/postgres.ext/postgres_database.py)
pyre_test_python_testcase(tests/postgres.ext/postgres_attach.py)
pyre_test_python_testcase(tests/postgres.ext/postgres_database_create.py)
pyre_test_python_testcase(tests/postgres.ext/postgres_table.py)
pyre_test_python_testcase(tests/postgres.ext/postgres_reserved.py)
pyre_test_python_testcase(tests/postgres.ext/postgres_references.py)
pyre_test_python_testcase(tests/postgres.ext/postgres_database_drop.py)

# the component tests pound on a database they create and drop; the create is a setup fixture,
# the drop a cleanup one, and everything in between requires it
set_property(TEST tests.postgres.ext.postgres_database_create.py PROPERTY
  FIXTURES_SETUP POSTGRES)
set_property(TEST tests.postgres.ext.postgres_database_drop.py PROPERTY
  FIXTURES_CLEANUP POSTGRES)

# set up the dependencies
set_property(TEST tests.postgres.ext.postgres_table.py PROPERTY
  FIXTURES_REQUIRED POSTGRES)

set_property(TEST tests.postgres.ext.postgres_reserved.py PROPERTY
  FIXTURES_REQUIRED POSTGRES)

set_property(TEST tests.postgres.ext.postgres_references.py PROPERTY
  FIXTURES_REQUIRED POSTGRES)


# end of file

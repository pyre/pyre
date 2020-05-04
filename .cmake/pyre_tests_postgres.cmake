# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2020 all rights reserved
#


#
# postgres capability tests
#
# sanity
pyre_test_python_testcase(postgres/sanity.py)
pyre_test_python_testcase(postgres/sanity_pyrepg.py)
# pyrepg
pyre_test_python_testcase(postgres/pyrepg_exceptions.py)
pyre_test_python_testcase(postgres/pyrepg_connect.py)
pyre_test_python_testcase(postgres/pyrepg_execute_badCommand.py)
pyre_test_python_testcase(postgres/pyrepg_submit.py)

# components
pyre_test_python_testcase(postgres/postgres_database.py)
pyre_test_python_testcase(postgres/postgres_attach.py)
pyre_test_python_testcase(postgres/postgres_database_create.py)
pyre_test_python_testcase(postgres/postgres_table.py)
pyre_test_python_testcase(postgres/postgres_reserved.py)
pyre_test_python_testcase(postgres/postgres_references.py)
pyre_test_python_testcase(postgres/postgres_database_drop.py)

# make the fixture
set_property(TEST postgres.postgres_database_create.py PROPERTY
  FIXTURES_SETUP POSTGRES)
set_property(TEST postgres.postgres_database_drop.py PROPERTY
  FIXTURES_CLEANUP POSTGRES)

# set up the dependencies
set_property(TEST postgres.postgres_table.py PROPERTY
  FIXTURES_REQUIRED POSTGRES)

set_property(TEST postgres.postgres_reserved.py PROPERTY
  FIXTURES_REQUIRED POSTGRES)

set_property(TEST postgres.postgres_references.py PROPERTY
  FIXTURES_REQUIRED POSTGRES)


# end of file

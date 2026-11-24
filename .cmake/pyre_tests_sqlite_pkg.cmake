# -*- cmake -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


#
# sqlite capability tests
#
pyre_test_python_testcase(tests/sqlite.pkg/sanity.py)
pyre_test_python_testcase(tests/sqlite.pkg/sqlite_database.py)
pyre_test_python_testcase(tests/sqlite.pkg/sqlite_attach.py)
pyre_test_python_testcase(tests/sqlite.pkg/sqlite_table.py)
pyre_test_python_testcase(tests/sqlite.pkg/sqlite_references.py)
pyre_test_python_testcase(tests/sqlite.pkg/sqlite_where_like_escape.py)
pyre_test_python_testcase(tests/sqlite.pkg/sqlite_defaults.py)
pyre_test_python_testcase(tests/sqlite.pkg/sqlite_values.py)
pyre_test_python_testcase(tests/sqlite.pkg/sqlite_where_date.py)
pyre_test_python_testcase(tests/sqlite.pkg/sqlite_update_nothing.py)
pyre_test_python_testcase(tests/sqlite.pkg/sqlite_transaction.py)
pyre_test_python_testcase(tests/sqlite.pkg/sqlite_insert_defaults.py)
pyre_test_python_testcase(tests/sqlite.pkg/sqlite_cast.py)
pyre_test_python_testcase(tests/sqlite.pkg/sqlite_projection_derived.py)
pyre_test_python_testcase(tests/sqlite.pkg/sqlite_null_text.py)
pyre_test_python_testcase(tests/sqlite.pkg/sqlite_types.py)
pyre_test_python_testcase(tests/sqlite.pkg/sqlite_rollback.py)
pyre_test_python_testcase(tests/sqlite.pkg/sqlite_table_exist_ok.py)
pyre_test_python_testcase(tests/sqlite.pkg/sqlite_table_missing_ok.py)
pyre_test_python_testcase(tests/sqlite.pkg/sqlite_index.py)
pyre_test_python_testcase(tests/sqlite.pkg/sqlite_identity.py)
pyre_test_python_testcase(tests/sqlite.pkg/sqlite_isin.py)
pyre_test_python_testcase(tests/sqlite.pkg/sqlite_paging.py)
pyre_test_python_testcase(tests/sqlite.pkg/sqlite_join.py)
pyre_test_python_testcase(tests/sqlite.pkg/sqlite_isin_query.py)
pyre_test_python_testcase(tests/sqlite.pkg/sqlite_returning_insert.py)
pyre_test_python_testcase(tests/sqlite.pkg/sqlite_returning_foreign.py)
pyre_test_python_testcase(tests/sqlite.pkg/sqlite_upsert_replace.py)
pyre_test_python_testcase(tests/sqlite.pkg/sqlite_upsert_keep.py)
pyre_test_python_testcase(tests/sqlite.pkg/sqlite_floor.py)
pyre_test_python_testcase(tests/sqlite.pkg/sqlite_nested_rollback.py)
pyre_test_python_testcase(tests/sqlite.pkg/sqlite_update_atomic.py)
pyre_test_python_testcase(tests/sqlite.pkg/sqlite_lock_refused.py)
# cleanup
add_test(NAME tests.sqlite.clean
  WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}/tests/sqlite.pkg"
  COMMAND ${BASH_PROGRAM} -c "rm pyre.sql")

# make the fixture
set_property(TEST tests.sqlite.pkg.sqlite_attach.py PROPERTY
  FIXTURES_SETUP SQLITE)
set_property(TEST tests.sqlite.clean PROPERTY
  FIXTURES_CLEANUP SQLITE)

# set up the dependencies
set_property(TEST tests.sqlite.pkg.sqlite_table.py PROPERTY
  FIXTURES_REQUIRED SQLITE)

set_property(TEST tests.sqlite.pkg.sqlite_references.py PROPERTY
  FIXTURES_REQUIRED SQLITE)


# end of file

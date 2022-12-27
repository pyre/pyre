# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


#
# merlin
#
# components
pyre_test_python_testcase(merlin.pkg/components/sanity.py)
pyre_test_python_testcase(merlin.pkg/components/merlin_shell.py)
pyre_test_python_testcase(merlin.pkg/components/merlin_spell.py)
pyre_test_python_testcase(merlin.pkg/components/merlin_curator.py)
pyre_test_python_testcase(merlin.pkg/components/merlin_packages.py)

# cleanup
add_test(NAME merlin.components.clean
  COMMAND ${BASH_PROGRAM} -c "rm .merlin/project.pickle"
  WORKING_DIRECTORY "${PYRE_TESTSUITE_DIR}/merlin.pkg/components"
  )

# fixture
set_property(TEST merlin.components.clean PROPERTY
  FIXTURES_CLEANUP MERLIN_COMPONENTS
  )

# set up the dependencies
set_property(TEST merlin.pkg.components.merlin_curator.py PROPERTY
  FIXTURES_REQUIRED MERLIN_COMPONENTS
  )

# spells
pyre_test_pyre_driver(merlin shallow init merlin.shallow)
pyre_test_pyre_driver(merlin multi init merlin.one merlin.two)
pyre_test_pyre_driver(merlin deep init --create-prefix merlin.deep/this/is/very/deep/ly/buried)

# clean up
add_test(NAME merlin.spells.clean
  COMMAND ${BASH_PROGRAM} -c "rm -rf merlin.*; "
  )

# fixture
set_property(TEST merlin.spells.clean PROPERTY
  FIXTURES_CLEANUP MERLIN_SPELL
  )

# set up the dependencies
set_property(TEST merlin.shallow PROPERTY
  FIXTURES_REQUIRED MERLIN_SPELL
  )

set_property(TEST merlin.multi PROPERTY
  FIXTURES_REQUIRED MERLIN_SPELL
  )

set_property(TEST merlin.deep PROPERTY
  FIXTURES_REQUIRED MERLIN_SPELL
  )


# end of file

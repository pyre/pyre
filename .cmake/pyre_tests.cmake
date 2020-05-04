# -*- cmake -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2020 all rights reserved
#


# create a unique test case name that incorporate the command line arguments
# adapted from code by @rtburns-jpl
function(pyre_test_testcase testcase testfile)
  # the test case stem is its path with path separators replaced by dots
  string(REPLACE "/" "." stem ${testfile})

  # initialize the command line argument pile
  set(args "")
  # if there are command line arguments
  if(ARGN)
    # mangle them
    string(REPLACE ";" "_"  args "_${ARGN}")
  endif()

  # assemble the test name and hand it off
  set(${testcase} "${stem}${args}" PARENT_SCOPE)

  # all done
endfunction()


# attach {setup} and {cleanup} fixtures to a test case
# N.B.: the signature may look backwards, but the {testfile} command line arguments are in
# ${ARGN} so it seemed simpler this way
function(pyre_test_testcase_shell_fixture setup cleanup testfile)
  # create the name of the testcase
  pyre_test_testcase(testname ${testfile} ${ARGN})

  # get the relative path to the test case local directory so we can set the working dir
  get_filename_component(dir ${testfile} DIRECTORY)

  # create the setup test case
  add_test(NAME ${testname}.setup COMMAND
    ${BASH_PROGRAM} -c "${setup}"
    )
  # specify the required working directory
  set_property(TEST ${testname}.setup PROPERTY
    WORKING_DIRECTORY ${PYRE_TESTSUITE_DIR}/${dir}
    )
  # register it as the setup of a fixture
  set_property(TEST ${testname}.setup PROPERTY
    FIXTURES_SETUP ${testname}.fixture
    )

  # create the cleanup test case
  add_test(NAME ${testname}.cleanup COMMAND
    ${BASH_PROGRAM} -c "${cleanup}"
    )
  # specify the required working directory
  set_property(TEST ${testname}.cleanup PROPERTY
    WORKING_DIRECTORY ${PYRE_TESTSUITE_DIR}/${dir}
    )
  # register it as the cleanup of a fixture
  set_property(TEST ${testname}.cleanup PROPERTY
    FIXTURES_CLEANUP ${testname}.fixture
    )

  # attach the fixture to the test case
  set_property(TEST ${testname} PROPERTY
    FIXTURES_REQUIRED "${testname}.fixture"
    )

  # all done
endfunction()


# register a python script as a test case; use a path relative to {PYRE_TESTSUITE_DIR}
function(pyre_test_python_testcase testfile)
  # create the name of the testcase
  pyre_test_testcase(testname ${testfile} ${ARGN})

  # we run the test cases in their local directory, so we need the base name
  get_filename_component(base ${testfile} NAME)
  # get the relative path to the test case local directory so we can set the working dir
  get_filename_component(dir ${testfile} DIRECTORY)

  # set up the harness
  add_test(NAME ${testname}
    COMMAND ${Python3_EXECUTABLE} ./${base} ${ARGN})
  # register the runtime environment requirements
  set_property(TEST ${testname} PROPERTY ENVIRONMENT
    LD_LIBRARY_PATH=${CMAKE_INSTALL_PREFIX}/lib
    PYTHONPATH=${CMAKE_INSTALL_PREFIX}/${PYRE_DEST_PACKAGES}
    )
  # launch from the location of the testcase
  set_property(TEST ${testname} PROPERTY
    WORKING_DIRECTORY ${PYRE_TESTSUITE_DIR}/${dir}
    )

  # all done
endfunction()


# register a python script as a parallel test case
function(pyre_test_python_testcase_mpi testfile slots)
  # create the name of the testcase
  pyre_test_testcase(testname ${testfile} ${slots} ${ARGN})

  # we run the test cases in their local directory, so we need the base name
  get_filename_component(base ${testfile} NAME)
  # get the relative path to the test case local directory so we can set the working dir
  get_filename_component(dir ${testfile} DIRECTORY)

  # set up the harness
  add_test(NAME ${testname}
    COMMAND
    ${MPIEXEC} ${MPIEXEC_NUMPROC_FLAG} ${slots} --hostfile localhost
    ${MPIEXEC_PREFLAGS}
    ${Python3_EXECUTABLE} ./${base}
    ${MPIEXEC_POSTFLAGS}
    ${ARGN}
    )
  # register the runtime environment requirements
  set_property(TEST ${testname} PROPERTY ENVIRONMENT
    LD_LIBRARY_PATH=${CMAKE_INSTALL_PREFIX}/lib
    PYTHONPATH=${CMAKE_INSTALL_PREFIX}/${PYRE_DEST_PACKAGES}
    )
  # launch from the location of the testcase
  set_property(TEST ${testname} PROPERTY
    WORKING_DIRECTORY ${PYRE_TESTSUITE_DIR}/${dir}
    )

  # all done
endfunction()


# register a python script as a test case; use a path relative to {PYRE_TESTSUITE_DIR}
function(pyre_test_python_testcase_envvar env testfile)
  # create the name of the testcase
  pyre_test_testcase(testname ${testfile} ${ARGN})

  # we run the test cases in their local directory, so we need the base name
  get_filename_component(base ${testfile} NAME)
  # get the relative path to the test case local directory so we can set the working dir
  get_filename_component(dir ${testfile} DIRECTORY)

  # set up the harness
  add_test(NAME ${testname}
    COMMAND ${BASH_PROGRAM} -c "${env} ${Python3_EXECUTABLE} ./${base} ${ARGN}")
  # register the runtime environment requirements
  set_property(TEST ${testname} PROPERTY ENVIRONMENT
    LD_LIBRARY_PATH=${CMAKE_INSTALL_PREFIX}/lib
    PYTHONPATH=${CMAKE_INSTALL_PREFIX}/${PYRE_DEST_PACKAGES}
    )
  # launch from the location of the testcase
  set_property(TEST ${testname} PROPERTY
    WORKING_DIRECTORY ${PYRE_TESTSUITE_DIR}/${dir}
    )

  # all done
endfunction()


# end of file

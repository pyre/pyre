set(testfiles
communicator.cc
group-exclude.cc
group-include.cc
group-setops.cc
group.cc
sanity.cc
world.cc
)

foreach(testfile ${testfiles})
    # generate target and test names from file/directory
    get_filename_component(name ${testfile} NAME_WE)
    set(target test.libpyre.mpi.${name})

    add_executable(${target} ${testfile})
    target_link_libraries(${target} PRIVATE pyre::mpi)
    add_test(NAME libpyre.mpi.${name} COMMAND
        ${MPIEXEC_EXECUTABLE}
            ${MPIEXEC_NUMPROC_FLAG} ${MPIEXEC_MAX_NUMPROCS}
            ${MPIEXEC_PREFLAGS} ./${target} ${MPIEXEC_POSTFLAGS}
            --hostfile localhost
        )
endforeach()

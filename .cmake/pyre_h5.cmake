# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# add the pyre::h5 c++ wrappers to libpyre; they wrap the hdf5 C api and need hdf5
function(pyre_h5Lib)
  if(HDF5_FOUND)
    # the wrappers live in a top-level {lib/h5}; copy their headers, staging them under the
    # {pyre} namespace so they never collide in a shared prefix
    file(GLOB_RECURSE files
         RELATIVE ${CMAKE_CURRENT_SOURCE_DIR}/lib/h5
         CONFIGURE_DEPENDS
         lib/h5/*.h lib/h5/*.icc
         )
    foreach(file ${files})
      # skip the gateway header, which is deposited one level up
      if("${file}" STREQUAL "h5.h")
        continue()
      endif()
      configure_file(lib/h5/${file} lib/pyre/h5/${file} COPYONLY)
    endforeach()

    # and the gateway header, as {pyre/h5.h}
    configure_file(lib/h5/h5.h lib/pyre/h5.h COPYONLY)

    # the pyre-owned wrappers over the hdf5 c api
    target_sources(pyre PRIVATE
      lib/h5/Identifier.cc
      lib/h5/DataSpace.cc
      lib/h5/Location.cc
      lib/h5/Attribute.cc
      lib/h5/Group.cc
      lib/h5/File.cc
      lib/h5/DataSet.cc
      # property lists
      lib/h5/properties/List.cc
      lib/h5/properties/OCPL.cc
      lib/h5/properties/STRCPL.cc
      lib/h5/properties/ACPL.cc
      lib/h5/properties/DAPL.cc
      lib/h5/properties/DCPL.cc
      lib/h5/properties/DXPL.cc
      lib/h5/properties/FAPL.cc
      lib/h5/properties/FCPL.cc
      lib/h5/properties/GCPL.cc
      lib/h5/properties/LAPL.cc
      lib/h5/properties/LCPL.cc
      # datatypes
      lib/h5/types/Datatype.cc
      lib/h5/types/Atom.cc
      lib/h5/types/Predefined.cc
      lib/h5/types/Int.cc
      lib/h5/types/Float.cc
      lib/h5/types/String.cc
      lib/h5/types/Compound.cc
      lib/h5/types/Enum.cc
      lib/h5/types/Array.cc
      lib/h5/types/VarLen.cc
      )
    # libpyre now needs the hdf5 c library; the plain signature (matching {pyre_pyreLib}) links
    # it transitively, so consumers whose header templates call the hdf5 c api get it too
    target_link_libraries(pyre HDF5::HDF5)
    # which puts it in our exported link interface, so downstream projects have to be able to
    # resolve it before they load our targets; teach the package configuration to do it for them
    # {FindHDF5} probes the hdf5 c toolchain with its {h5cc} wrapper and needs a c compiler to
    # do it; a consumer whose own project is c++ only would otherwise be told, from deep inside
    # the module, that the wrapper cannot compile a minimal hdf5 program
    pyre_exportPrologue(
"if(NOT CMAKE_C_COMPILER_LOADED)
  enable_language(C)
endif()")
    # steer them towards the same flavour of hdf5 we linked; without this a consumer of a
    # parallel build resolves whichever hdf5 the module prefers, and a serial one against our
    # parallel headers is a mismatch they have to diagnose themselves
    if(HDF5_IS_PARALLEL)
      pyre_exportPrologue("set(HDF5_PREFER_PARALLEL ON)")
    endif()
    pyre_exportRequirement(HDF5 HDF5::HDF5 "COMPONENTS C HL")
    # a parallel build of hdf5 exposes {mpi.h} through its public headers, so anything that
    # includes them needs the mpi usage requirements; the plain signature propagates them to
    # every consumer of {pyre}, including the {h5} bindings; this restores the handling that
    # was lost when the deprecated mpi c++ bindings were retired
    if(HDF5_IS_PARALLEL AND MPI_FOUND)
      target_link_libraries(pyre MPI::MPI_CXX)
      # and, again, downstream projects inherit the obligation to resolve it
      pyre_exportRequirement(MPI MPI::MPI_CXX "COMPONENTS CXX")
    endif()
  endif(HDF5_FOUND)
endfunction(pyre_h5Lib)


# build the h5 python extension
function(pyre_h5Module)
  if(HDF5_FOUND)
    # h5
    Python_add_library(h5module MODULE WITH_SOABI)
    # adjust the name to match what python expects
    set_target_properties(h5module PROPERTIES LIBRARY_OUTPUT_NAME h5)
    # specify the directory for the module compilation products
    pyre_library_directory(h5module extensions)
    # set the libraries to link against; the wrappers live in libpyre
    target_link_libraries(h5module PRIVATE pyre journal pybind11::module HDF5::HDF5)
    # add the sources
    target_sources(h5module PRIVATE
      extensions/h5/__init__.cc
      extensions/h5/api.cc
      extensions/h5/Attribute.cc
      extensions/h5/DataSet.cc
      extensions/h5/DataSpace.cc
      extensions/h5/enums.cc
      extensions/h5/File.cc
      extensions/h5/Group.cc
      extensions/h5/mosaics.cc
      # property lists
      extensions/h5/properties/__init__.cc
      extensions/h5/properties/List.cc
      extensions/h5/properties/OCPL.cc
      extensions/h5/properties/STRCPL.cc
      extensions/h5/properties/ACPL.cc
      extensions/h5/properties/DAPL.cc
      extensions/h5/properties/DCPL.cc
      extensions/h5/properties/DXPL.cc
      extensions/h5/properties/FAPL.cc
      extensions/h5/properties/FCPL.cc
      extensions/h5/properties/GCPL.cc
      extensions/h5/properties/LAPL.cc
      extensions/h5/properties/LCPL.cc
      # datatypes
      extensions/h5/types/__init__.cc
      extensions/h5/types/Datatype.cc
      extensions/h5/types/Atom.cc
      extensions/h5/types/Predefined.cc
      extensions/h5/types/Int.cc
      extensions/h5/types/Float.cc
      extensions/h5/types/String.cc
      extensions/h5/types/Compound.cc
      extensions/h5/types/Enum.cc
      extensions/h5/types/Array.cc
      extensions/h5/types/VarLen.cc
      # the predefined-type collections
      extensions/h5/types/native.cc
      extensions/h5/types/std.cc
      extensions/h5/types/big.cc
      extensions/h5/types/little.cc
      extensions/h5/types/alpha.cc
      extensions/h5/types/ieee.cc
      extensions/h5/types/intel.cc
      extensions/h5/types/mips.cc
      extensions/h5/types/unix.cc
      )
    # install
    install(
      TARGETS h5module
      LIBRARY
      DESTINATION ${PYRE_DEST_PACKAGES}/pyre/extensions
      )
  endif(HDF5_FOUND)
endfunction(pyre_h5Module)


# end of file

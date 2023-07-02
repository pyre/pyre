# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# build the h5 python extension
function(pyre_h5Module)
  if(HDF5_FOUND)
    # h5
    Python_add_library(h5module MODULE)
    # adjust the name to match what python expects
    set_target_properties(h5module PROPERTIES LIBRARY_OUTPUT_NAME h5)
    set_target_properties(h5module PROPERTIES SUFFIX ${PYTHON3_SUFFIX})
    # specify the directory for the module compilation products
    pyre_library_directory(h5module extensions)
    # set the libraries to link against
    if(HDF5_IS_PARALLEL)
      target_link_libraries(h5module PRIVATE journal pybind11::module HDF5::HDF5 MPI::MPI_CXX)
    else(HDF5_IS_PARALLEL)
      target_link_libraries(h5module PRIVATE journal pybind11::module HDF5::HDF5)
    endif(HDF5_IS_PARALLEL)
    # add the sources
    target_sources(h5module PRIVATE
      extensions/h5/__init__.cc
      extensions/h5/api.cc
      extensions/h5/DAPL.cc
      extensions/h5/DataSet.cc
      extensions/h5/DataSpace.cc
      extensions/h5/DCPL.cc
      extensions/h5/DXPL.cc
      extensions/h5/enums.cc
      extensions/h5/FAPL.cc
      extensions/h5/FCPL.cc
      extensions/h5/File.cc
      extensions/h5/Group.cc
      extensions/h5/LAPL.cc
      extensions/h5/LCPL.cc
      extensions/h5/PropList.cc
      extensions/h5/datatypes/__init__.cc
      extensions/h5/datatypes/ArrayType.cc
      extensions/h5/datatypes/AtomType.cc
      extensions/h5/datatypes/CompType.cc
      extensions/h5/datatypes/DataType.cc
      extensions/h5/datatypes/EnumType.cc
      extensions/h5/datatypes/FloatType.cc
      extensions/h5/datatypes/IntType.cc
      extensions/h5/datatypes/PredType.cc
      extensions/h5/datatypes/StrType.cc
      extensions/h5/datatypes/VarLenType.cc
      extensions/h5/datatypes/alpha.cc
      extensions/h5/datatypes/big.cc
      extensions/h5/datatypes/ieee.cc
      extensions/h5/datatypes/intel.cc
      extensions/h5/datatypes/little.cc
      extensions/h5/datatypes/mips.cc
      extensions/h5/datatypes/native.cc
      extensions/h5/datatypes/std.cc
      extensions/h5/datatypes/unix.cc
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

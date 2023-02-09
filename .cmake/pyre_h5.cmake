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
    # set the libraries to link against
    if(HDF5_IS_PARALLEL)
      target_link_libraries(h5module PRIVATE journal pybind11::module HDF5::HDF5 MPI::MPI_CXX)
    else(HDF5_IS_PARALLEL)
      target_link_libraries(h5module PRIVATE journal pybind11::module HDF5::HDF5)
    endif(HDF5_IS_PARALLEL)
    # add the sources
    target_sources(h5module PRIVATE
      h5/__init__.cc
      h5/api.cc
      h5/DataSet.cc
      h5/DataSpace.cc
      h5/enums.cc
      h5/File.cc
      h5/FileAccessPropertyList.cc
      h5/Group.cc
      h5/datatypes/__init__.cc
      h5/datatypes/ArrayType.cc
      h5/datatypes/AtomType.cc
      h5/datatypes/CompType.cc
      h5/datatypes/DataType.cc
      h5/datatypes/EnumType.cc
      h5/datatypes/FloatType.cc
      h5/datatypes/IntType.cc
      h5/datatypes/native.cc
      h5/datatypes/PredType.cc
      h5/datatypes/StrType.cc
      h5/datatypes/VarLenType.cc
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

# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# build the h5 python extension
function(pyre_h5Module)
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
    h5/h5.cc
    h5/api.cc
    h5/dataset.cc
    h5/dataspace.cc
    h5/datatypes/compound.cc
    h5/datatypes/datatype.cc
    h5/datatypes/datatypes.cc
    h5/datatypes/native.cc
    h5/datatypes/predefined.cc
    h5/file.cc
    h5/group.cc
    )
  # install
  install(
    TARGETS h5module
    LIBRARY
    DESTINATION ${PYRE_DEST_PACKAGES}/pyre/extensions
    )
endfunction(pyre_h5Module)


# end of file

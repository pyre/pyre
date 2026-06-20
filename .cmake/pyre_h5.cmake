# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# add the pyre::h5 c++ wrappers to libpyre; they wrap the hdf5 C api and need hdf5
function(pyre_h5Lib)
  if(HDF5_FOUND)
    # the pyre-owned wrappers over the hdf5 c api
    target_sources(pyre PRIVATE
      lib/pyre/h5/Identifier.cc
      lib/pyre/h5/DataSpace.cc
      lib/pyre/h5/Location.cc
      lib/pyre/h5/Attribute.cc
      lib/pyre/h5/Group.cc
      lib/pyre/h5/File.cc
      lib/pyre/h5/DataSet.cc
      # property lists
      lib/pyre/h5/properties/List.cc
      lib/pyre/h5/properties/DAPL.cc
      lib/pyre/h5/properties/DCPL.cc
      lib/pyre/h5/properties/DXPL.cc
      lib/pyre/h5/properties/FAPL.cc
      lib/pyre/h5/properties/FCPL.cc
      lib/pyre/h5/properties/LAPL.cc
      lib/pyre/h5/properties/LCPL.cc
      # datatypes
      lib/pyre/h5/types/Datatype.cc
      lib/pyre/h5/types/Atom.cc
      lib/pyre/h5/types/Predefined.cc
      lib/pyre/h5/types/Int.cc
      lib/pyre/h5/types/Float.cc
      lib/pyre/h5/types/String.cc
      lib/pyre/h5/types/Compound.cc
      lib/pyre/h5/types/Enum.cc
      lib/pyre/h5/types/Array.cc
      lib/pyre/h5/types/VarLen.cc
      )
    # libpyre now needs the hdf5 c library; the plain signature (matching {pyre_pyreLib}) links
    # it transitively, so consumers whose header templates call the hdf5 c api get it too
    target_link_libraries(pyre HDF5::HDF5)
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
      # property lists
      extensions/h5/properties/__init__.cc
      extensions/h5/properties/List.cc
      extensions/h5/properties/DAPL.cc
      extensions/h5/properties/DCPL.cc
      extensions/h5/properties/DXPL.cc
      extensions/h5/properties/FAPL.cc
      extensions/h5/properties/FCPL.cc
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

// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_h5_external_h)
#define pyre_h5_external_h


// externals
#include <algorithm>
#include <array>
#include <complex>
// support
#include <pyre/journal.h>
// the hdf5 api
#include <H5Cpp.h>


// aliases
namespace pyre::h5 {
    // from {hdf5}
    using dataset_t = H5::DataSet;
    using dataspace_t = H5::DataSpace;
    using datatype_t = H5::DataType;
    using comptype_t = H5::CompType;
    using predtype_t = H5::PredType;
    // for specifying dataspace coordinates and shapes
    using shape_t = std::vector<hsize_t>;
    using index_t = shape_t;
    using offsets_t = std::vector<hssize_t>;
} // namespace pyre::h5


#endif

// end of file

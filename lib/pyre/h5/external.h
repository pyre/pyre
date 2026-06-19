// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// externals
#include <algorithm>
#include <array>
#include <complex>
#include <cstdint>
#include <utility>
#include <vector>
// support
#include <pyre/journal.h>
// the hdf5 api
#include <H5Cpp.h>


// aliases
namespace pyre::h5 {
    // from {hdf5}
    using file_t = H5::H5File;
    using group_t = H5::Group;
    using dataset_t = H5::DataSet;
    using dataspace_t = H5::DataSpace;
    using dapl_t = H5::DSetAccPropList;
    using dcpl_t = H5::DSetCreatPropList;
    using fapl_t = H5::FileAccPropList;
    using fcpl_t = H5::FileCreatPropList;
    using datatype_t = H5::DataType;
    using comptype_t = H5::CompType;
    using predtype_t = H5::PredType;
    // for specifying dataspace coordinates and shapes
    using shape_t = std::vector<hsize_t>;
    using index_t = shape_t;
    using offsets_t = std::vector<hssize_t>;
    // a collection of dataspace coordinates, e.g. a set of selected points
    using points_t = std::vector<shape_t>;
    // a hyperslab as a (begin, end) corner pair, and a collection of them
    using slab_t = std::pair<shape_t, shape_t>;
    using slabs_t = std::vector<slab_t>;
} // namespace pyre::h5


// end of file

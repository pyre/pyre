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
#include <tuple>
#include <utility>
#include <vector>
// support
#include <pyre/journal.h>
// the hdf5 api
#include <H5Cpp.h>


// forward declarations of the pyre-owned wrappers, so the aliases below can name them before
// their full definitions are pulled in by {public.h}
namespace pyre::h5 {
    class DataSet;
} // namespace pyre::h5

namespace pyre::h5::types {
    class Datatype;
    class Compound;
    class Predefined;
} // namespace pyre::h5::types


// aliases
namespace pyre::h5 {
    // from {hdf5}
    using file_t = H5::H5File;
    using group_t = H5::Group;
    // the dataset is now a pyre-owned wrapper; the dataspace machinery below is still {H5::}
    using dataset_t = pyre::h5::DataSet;
    using dataspace_t = H5::DataSpace;
    // pyre-owned datatypes over the hdf5 c api
    using datatype_t = pyre::h5::types::Datatype;
    using comptype_t = pyre::h5::types::Compound;
    using predtype_t = pyre::h5::types::Predefined;
    // names and other text
    using string_t = std::string;
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

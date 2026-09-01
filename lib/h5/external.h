// -*- C++ -*-
// -*- coding: utf-8 -*-
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
#include <optional>
#include <tuple>
#include <utility>
#include <vector>
// support
#include <pyre/journal.h>
// the grid vocabulary that carries dataset geometry
#include <pyre/grid.h>
// and the storage strategies a mosaic is assembled over
#include <pyre/memory.h>
// the hdf5 c api; pyre::h5 no longer depends on the hdf5 c++ layer
#include <hdf5.h>

// the oldest hdf5 we build against: 1.14.4 repaired S3 access through the ros3 driver, and
// everything below it is missing pieces this layer uses unconditionally; say so here rather
// than let an older library fail somewhere deep in a translation unit
#if !H5_VERSION_GE(1, 14, 4)
#error "pyre::h5 requires HDF5 1.14.4 or newer"
#endif


// forward declarations of the pyre-owned wrappers, so the aliases below can name them before
// their full definitions are pulled in by {public.h}
namespace pyre::h5 {
    class DataSpace;
    class DataSet;
} // namespace pyre::h5

namespace pyre::h5::types {
    class Datatype;
    class Compound;
    class Predefined;
} // namespace pyre::h5::types


// aliases
namespace pyre::h5 {
    // now pyre-owned wrappers over the hdf5 c api
    using dataset_t = pyre::h5::DataSet;
    using dataspace_t = pyre::h5::DataSpace;
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
    // an opaque run of bytes: a chunk in the form it is stored in, still carrying whatever
    // the filter pipeline did to it, and therefore not cells of anything until it is decoded
    using bytes_t = std::vector<char>;

    // the grid descriptions handed out by dataspaces and datasets: dataset and chunk shapes
    // are facts discovered at runtime, so they travel as the runtime-rank flavors of the
    // {pyre::grid} vocabulary; cell types, by contrast, stay compile time, since whoever
    // receives the data must name the type in source in order to allocate for it
    using packing_t = pyre::grid::dynamic_canonical_t;
    using tiling_t = pyre::grid::dynamic_chunked_t;
    // the out-of-core grid a chunked dataset assembles over its own tiling: one
    // demand-materialized page per chunk; only the cell type is the caller's to name
    template <class cellT>
    using mosaic_t = pyre::grid::grid_t<tiling_t, pyre::memory::paged_t<cellT>>;
} // namespace pyre::h5


// end of file

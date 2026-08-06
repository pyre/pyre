// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// externals
#include "external.h"
// namespace setup
#include "forward.h"
// the type-erased grid and mosaic, from the library's python-support tier; they are
// header-only precisely so that every extension can compile them in and register its own
// module-local flavors, instead of trafficking in types registered by another module
#include <pyre/py/grid/AnyGrid.h>
#include <pyre/py/grid/AnyMosaic.h>


// the mosaic machinery
namespace pyre::h5::py {
    // the borrowed type-erased classes
    using anygrid_t = pyre::py::grid::AnyGrid;
    using anymosaic_t = pyre::py::grid::AnyMosaic;

    // choose a cell type from its pyre memory cell name and hand it to a callable that is
    // templated on that type; this keeps the twelve-way dispatch in one place
    template <class F>
    inline auto dispatchCell(const string_t & cell, F && f);

    // build an out-of-core mosaic over a dataset's own chunking, wired to move chunks
    // through the dataset
    template <class cellT>
    inline auto makeMosaic(const DataSet & dataset, string_t cell) -> anymosaic_t;
    // the window flavor: the smallest mosaic that covers the window at {base}+{extent}
    template <class cellT>
    inline auto makeMosaic(
        const DataSet & dataset, string_t cell, const anymosaic_t::index_type & base,
        const anymosaic_t::shape_type & extent) -> anymosaic_t;

    // register the {mosaic} factories with the dataset class
    inline auto bindMosaics(py::class_<DataSet> & cls) -> void;
} // namespace pyre::h5::py


// the inline implementations
#include "mosaics.icc"


// end of file

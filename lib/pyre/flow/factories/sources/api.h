// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// the forward declarations of {pyre::flow::factories::sources}
#include "forward.h"


// sources
namespace pyre::flow::factories::sources {
    // a window of a raster, as a tile
    template <class sourceT, class sliceT>
    using slice_t = Slice<sourceT, sliceT>;
} // namespace pyre::flow::factories::sources


// end of file

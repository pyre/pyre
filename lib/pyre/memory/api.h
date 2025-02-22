// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved

// code guard
#pragma once

// external
#include "externals.h"
// forward declarations
#include "forward.h"


// user facing types
namespace pyre::memory {
    // normalized type access
    template <typename T, bool isConst>
    using cell_t = Cell<T, isConst>;

    // helper that generates a human readable name for each supported datatype
    template <typename T>
    using cellname_t = CellName<T>;

    // block on the stack
    template <int D, typename T>
    using stack_t = Stack<D, T, false>;
    // read-only version
    template <int D, typename T>
    using conststack_t = Stack<D, T, true>;

    // block on the heap
    template <typename T>
    using heap_t = Heap<T, false>;
    // read-only version
    template <typename T>
    using constheap_t = Heap<T, true>;

    // file-backed blocks of cells
    template <typename T>
    using map_t = Map<T, false>;
    // file-backed blocks of const cells
    template <typename T>
    using constmap_t = Map<T, true>;

    // view to someone else's data
    template <typename T>
    using view_t = View<T, false>;

    // const view to someone else's data
    template <typename T>
    using constview_t = View<T, true>;
} // namespace pyre::memory


// low level entities; you should probably stay away from them
namespace pyre::memory {
    // support for managing file-backed memory undifferentiated blocks
    // used by {map_t} and {constmap_t} above
    using filemap_t = FileMap;
} // namespace pyre::memory


// end of file

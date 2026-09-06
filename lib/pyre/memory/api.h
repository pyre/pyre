// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

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

    // a scalar stored in a fixed byte order; it collapses to the plain scalar when that order is
    // the host's, or when the scalar is a single byte, so only cells that actually need swapping
    // pay for the wrapper
    template <typename T, std::endian order>
    using ordered_t =
        std::conditional_t<order == std::endian::native || sizeof(T) == 1, T, Ordered<T, order>>;
    // big endian, the network and IEEE order
    template <typename T>
    using big_t = ordered_t<T, std::endian::big>;
    // little endian, the intel order
    template <typename T>
    using little_t = ordered_t<T, std::endian::little>;
    // whichever order the host does not use; the one that always needs swapping
    template <typename T>
    using foreign_t = ordered_t<
        T, std::endian::native == std::endian::big ? std::endian::little : std::endian::big>;
    // the native scalar behind a cell value type
    template <typename T>
    using native_t = typename Native<T>::type;

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

    // block of cells assembled out of fixed-size pages
    template <typename T>
    using paged_t = Paged<T, false>;
    // read-only version
    template <typename T>
    using constpaged_t = Paged<T, true>;
} // namespace pyre::memory


// low level entities; you should probably stay away from them
namespace pyre::memory {
    // the base buffer types
    // mutable version
    template <typename T>
    using buffer_t = Buffer<T, false>;
    // read-only version
    template <typename T>
    using constbuffer_t = Buffer<T, true>;

    // support for managing file-backed memory undifferentiated blocks
    // used by {map_t} and {constmap_t} above
    using filemap_t = FileMap;
} // namespace pyre::memory


// end of file

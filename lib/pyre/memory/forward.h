// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "externals.h"


// set up the namespace
namespace pyre::memory {
    // utility that normalizes type access
    template <typename T, bool isConst>
    class Cell;

    // a scalar stored in a fixed byte order, whatever the host's
    template <typename T, std::endian order>
    class Ordered;

    // block on the stack
    template <int D, typename T, bool isConst>
    class Stack;

    // block on the heap
    template <typename T, bool isConst>
    class Heap;

    // file-backed block of undifferentiated memory
    class FileMap;
    // file-backed block of cells
    template <typename T, bool isConst>
    class Map;

    // a view to someone else's data
    template <typename T, bool isConst>
    class View;

    // block of cells assembled out of fixed-size pages, each a separate allocation
    template <typename T, bool isConst>
    class Paged;

    // iterator
    template <class memT>
    class Slice;
} // namespace pyre::memory


// global operators
namespace pyre::memory {
    // equality
    template <class memT>
    constexpr auto operator==(const Slice<memT> &, const Slice<memT> &) -> bool;
    // inequality
    template <class memT>
    constexpr auto operator!=(const Slice<memT> &, const Slice<memT> &) -> bool;

    // byte ordered cells compare through their native values
    template <typename T, std::endian order>
    constexpr auto operator==(const Ordered<T, order> &, const Ordered<T, order> &) -> bool;
    // also against a native value
    template <typename T, std::endian order>
    constexpr auto operator==(const Ordered<T, order> &, const T &) -> bool;
} // namespace pyre::memory


// helpers
namespace pyre::memory {
    // the base buffer type; not really useful on its own
    template <typename T, bool isConst>
    class Buffer;

    // a generalized iterator
    template <class memT>
    class Slice;

    // generator of a human readable name for each supported datatype
    template <typename T>
    struct CellName;

    // the native scalar behind a cell value type: the type itself, unless it is a byte ordered
    // wrapper, in which case the scalar it wraps
    template <typename T>
    struct Native;

    // recognize complex scalars, whose two components swap bytes independently
    template <typename T>
    concept complex_c = requires { typename T::value_type; }
                     && std::same_as<T, std::complex<typename T::value_type>>;
} // namespace pyre::memory


// end of file

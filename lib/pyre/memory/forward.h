// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved

// code guard
#pragma once


// set up the namespace
namespace pyre::memory {
    // utility that normalizes type access
    template <typename T, bool isConst>
    class Cell;

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
} // namespace pyre::memory

// end of file

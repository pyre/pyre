// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2024 all rights reserved

// code guard
#if !defined(pyre_memory_forward_h)
#define pyre_memory_forward_h


// set up the namespace
namespace pyre::memory {
    // utility that normalizes type access
    template <typename T, bool isConst>
    class Cell;

    // helper that generates a human readable name for each supported datatype
    template <typename T>
    struct CellName;
    // a compile-time container with type choices
    template <typename... cellT>
    struct CellTypes;

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
}; // namespace pyre::memory


#endif

// end of file

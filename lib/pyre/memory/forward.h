// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_memory_forward_h)
#define pyre_memory_forward_h


// set up the namespace
namespace pyre::memory {
    // utility that normalizes type access
    template <typename T, bool isConst> class Cell;

    // block on the stack
    template <int D, typename T, bool isConst> class Stack;

    // block on the heap
    template <typename T, bool isConst> class Heap;

    // file-backed block of undifferentiated memory
    class FileMap;
    // file-backed block of cells
    template <typename T, bool isConst> class Map;

    // a view to someone else's data
    template <typename T, bool isConst> class View;
};


#endif

// end of file

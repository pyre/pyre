// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"

// the common storage binders
#include "bindings.h"
// buffer protocol
#include "buffer_protocol.h"
// my heaps
#include "heaps.h"


// wrappers over {pyre::memory::heap} template expansions
// build the submodule
void
pyre::py::memory::heaps(py::module & m)
{
    // heaps
    // c
    heap<char>(
        // in scope
        m,
        // class name
        "CharHeap",
        // docstring
        "a read/write memory buffer of {char}");
    // i1
    heap<int8_t>(
        // in scope
        m,
        // class name
        "Int8Heap",
        // docstring
        "a read/write memory buffer of {int8_t}");
    heap<uint8_t>(
        // in scope
        m,
        // class name
        "UInt8Heap",
        // docstring
        "a read/write memory buffer of {uint8_t}");
    // i2
    heap<int16_t>(
        // in scope
        m,
        // class name
        "Int16Heap",
        // docstring
        "a read/write memory buffer of {int16_t}");
    heap<uint16_t>(
        // in scope
        m,
        // class name
        "UInt16Heap",
        // docstring
        "a read/write memory buffer of {uint16_t}");
    // i4
    heap<int32_t>(
        // in scope
        m,
        // class name
        "Int32Heap",
        // docstring
        "a read/write memory buffer of {int32_t}");
    heap<uint32_t>(
        // in scope
        m,
        // class name
        "UInt32Heap",
        // docstring
        "a read/write memory buffer of {uint32_t}");
    // i8
    heap<int64_t>(
        // in scope
        m,
        // class name
        "Int64Heap",
        // docstring
        "a read/write memory buffer of {int64_t}");
    heap<uint64_t>(
        // in scope
        m,
        // class name
        "UInt64Heap",
        // docstring
        "a read/write memory buffer of {uint64_t}");
    // d4
    heap<float>(
        // in scope
        m,
        // class name
        "FloatHeap",
        // docstring
        "a read/write memory buffer of {float}");
    // d8
    heap<double>(
        // in scope
        m,
        // class name
        "DoubleHeap",
        // docstring
        "a read/write memory buffer of {double}");
    // c4
    heap<std::complex<float>>(
        // in scope
        m,
        // class name
        "ComplexFloatHeap",
        // docstring
        "a read/write memory buffer of {std::complex<float>}");
    // c8
    heap<std::complex<double>>(
        // in scope
        m,
        // class name
        "ComplexDoubleHeap",
        // docstring
        "a read/write memory buffer of {std::complex<double>}");

    // all done
    return;
}


// end of file

// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"

// the common storage binders
#include "bindings.h"
// buffer protocol
#include "buffer_protocol.h"
// my views
#include "views.h"


// wrappers over {pyre::memory::view} template expansions
// build the submodule
void
pyre::py::memory::views(py::module & m)
{
    // views
    // c
    view<char>(
        // in scope
        m,
        // class name
        "CharView",
        // docstring
        "a read/write borrowed memory buffer of {char}");
    // i1
    view<int8_t>(
        // in scope
        m,
        // class name
        "Int8View",
        // docstring
        "a read/write borrowed memory buffer of {int8_t}");
    view<uint8_t>(
        // in scope
        m,
        // class name
        "UInt8View",
        // docstring
        "a read/write borrowed memory buffer of {uint8_t}");
    // i2
    view<int16_t>(
        // in scope
        m,
        // class name
        "Int16View",
        // docstring
        "a read/write borrowed memory buffer of {int16_t}");
    view<uint16_t>(
        // in scope
        m,
        // class name
        "UInt16View",
        // docstring
        "a read/write borrowed memory buffer of {uint16_t}");
    // i4
    view<int32_t>(
        // in scope
        m,
        // class name
        "Int32View",
        // docstring
        "a read/write borrowed memory buffer of {int32_t}");
    view<uint32_t>(
        // in scope
        m,
        // class name
        "UInt32View",
        // docstring
        "a read/write borrowed memory buffer of {uint32_t}");
    // i8
    view<int64_t>(
        // in scope
        m,
        // class name
        "Int64View",
        // docstring
        "a read/write borrowed memory buffer of {int64_t}");
    view<uint64_t>(
        // in scope
        m,
        // class name
        "UInt64View",
        // docstring
        "a read/write borrowed memory buffer of {uint64_t}");
    // d4
    view<float>(
        // in scope
        m,
        // class name
        "FloatView",
        // docstring
        "a read/write borrowed memory buffer of {float}");
    // d8
    view<double>(
        // in scope
        m,
        // class name
        "DoubleView",
        // docstring
        "a read/write borrowed memory buffer of {double}");
    // c4
    view<std::complex<float>>(
        // in scope
        m,
        // class name
        "ComplexFloatView",
        // docstring
        "a read/write borrowed memory buffer of {std::complex<float>}");
    // c8
    view<std::complex<double>>(
        // in scope
        m,
        // class name
        "ComplexDoubleView",
        // docstring
        "a read/write borrowed memory buffer of {std::complex<double>}");

    // all done
    return;
}


// end of file

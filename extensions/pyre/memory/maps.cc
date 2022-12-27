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
// my maps
#include "maps.h"


// wrappers over {pyre::memory::map} template expansions
// build the submodule
void
pyre::py::memory::maps(py::module & m)
{
    // const maps
    // c
    constmap<char>(
        // in scope
        m,
        // class name
        "ByteConstMap",
        // docstring
        "a read-only file backed memory buffer of {char}");
    constmap<unsigned char>(
        // in scope
        m,
        // class name
        "UInt8ConstMap",
        // docstring
        "a read-only file backed memory buffer of {uint8_t}");
    // i2
    constmap<int16_t>(
        // in scope
        m,
        // class name
        "Int16ConstMap",
        // docstring
        "a read-only file backed memory buffer of {int16_t}");
    // i4
    constmap<int32_t>(
        // in scope
        m,
        // class name
        "Int32ConstMap",
        // docstring
        "a read-only file backed memory buffer of {int32_t}");
    // i8
    constmap<int64_t>(
        // in scope
        m,
        // class name
        "Int64ConstMap",
        // docstring
        "a read-only file backed memory buffer of {int64_t}");
    // d4
    constmap<float>(
        // in scope
        m,
        // class name
        "FloatConstMap",
        // docstring
        "a read-only file backed memory buffer of {float}");
    // d8
    constmap<double>(
        // in scope
        m,
        // class name
        "DoubleConstMap",
        // docstring
        "a read-only file backed memory buffer of {double}");
    // c4
    constmap<std::complex<float>>(
        // in scope
        m,
        // class name
        "ComplexFloatConstMap",
        // docstring
        "a read-only file backed memory buffer of {std::complex<float>}");
    // c8
    constmap<std::complex<double>>(
        // in scope
        m,
        // class name
        "ComplexDoubleConstMap",
        // docstring
        "a read-only file backed memory buffer of {std::complex<double>}");

    // maps
    // c
    map<char>(
        // in scope
        m,
        // class name
        "ByteMap",
        // docstring
        "a read/write file backed memory buffer of {char}");
    map<unsigned char>(
        // in scope
        m,
        // class name
        "UInt8Map",
        // docstring
        "a read/write file backed memory buffer of {uint8_t}");
    // i2
    map<int16_t>(
        // in scope
        m,
        // class name
        "Int16Map",
        // docstring
        "a read/write file backed memory buffer of {int16_t}");
    // i4
    map<int32_t>(
        // in scope
        m,
        // class name
        "Int32Map",
        // docstring
        "a read/write file backed memory buffer of {int32_t}");
    // i8
    map<int64_t>(
        // in scope
        m,
        // class name
        "Int64Map",
        // docstring
        "a read/write file backed memory buffer of {int64_t}");
    // d4
    map<float>(
        // in scope
        m,
        // class name
        "FloatMap",
        // docstring
        "a read/write file backed memory buffer of {float}");
    // d8
    map<double>(
        // in scope
        m,
        // class name
        "DoubleMap",
        // docstring
        "a read/write file backed memory buffer of {double}");
    // c4
    map<std::complex<float>>(
        // in scope
        m,
        // class name
        "ComplexFloatMap",
        // docstring
        "a read/write file backed memory buffer of {std::complex<float>}");
    // c8
    map<std::complex<double>>(
        // in scope
        m,
        // class name
        "ComplexDoubleMap",
        // docstring
        "a read/write file backed memory buffer of {std::complex<double>}");

    // all done
    return;
}


// end of file

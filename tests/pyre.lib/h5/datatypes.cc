// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include <cassert>
// get the h5 support
#include <pyre/h5.h>


// check that {datatype<T>()} deduces the correct native hdf5 datatype
int
main()
{
    // each deduced type is a pyre-owned copy of a native hdf5 type; {H5Tequal} confirms it
    // describes the same type as the matching {H5T_NATIVE_*} constant
    // unsigned
    assert((H5Tequal(pyre::h5::datatype<std::uint8_t>().id(), H5T_NATIVE_UINT8) > 0));
    assert((H5Tequal(pyre::h5::datatype<std::uint16_t>().id(), H5T_NATIVE_UINT16) > 0));
    assert((H5Tequal(pyre::h5::datatype<std::uint32_t>().id(), H5T_NATIVE_UINT32) > 0));
    assert((H5Tequal(pyre::h5::datatype<std::uint64_t>().id(), H5T_NATIVE_UINT64) > 0));

    // signed
    assert((H5Tequal(pyre::h5::datatype<std::int8_t>().id(), H5T_NATIVE_INT8) > 0));
    assert((H5Tequal(pyre::h5::datatype<std::int16_t>().id(), H5T_NATIVE_INT16) > 0));
    assert((H5Tequal(pyre::h5::datatype<std::int32_t>().id(), H5T_NATIVE_INT32) > 0));
    assert((H5Tequal(pyre::h5::datatype<std::int64_t>().id(), H5T_NATIVE_INT64) > 0));

    // floating point
    assert((H5Tequal(pyre::h5::datatype<float>().id(), H5T_NATIVE_FLOAT) > 0));
    assert((H5Tequal(pyre::h5::datatype<double>().id(), H5T_NATIVE_DOUBLE) > 0));

    // all done
    return 0;
}


// end of file

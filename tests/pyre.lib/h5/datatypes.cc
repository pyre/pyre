// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include <cassert>
// get the h5 support
#include <pyre/h5.h>


// check we can build the native datatypes
int
main()
{
    // instantiate the native types that are supported by {hdf5} out of the box
    // unsigned
    assert((pyre::h5::datatype<std::uint8_t>() == H5::PredType::NATIVE_UINT8));
    assert((pyre::h5::datatype<std::uint16_t>() == H5::PredType::NATIVE_UINT16));
    assert((pyre::h5::datatype<std::uint32_t>() == H5::PredType::NATIVE_UINT32));
    assert((pyre::h5::datatype<std::uint64_t>() == H5::PredType::NATIVE_UINT64));

    // signed
    assert((pyre::h5::datatype<std::int8_t>() == H5::PredType::NATIVE_INT8));
    assert((pyre::h5::datatype<std::int16_t>() == H5::PredType::NATIVE_INT16));
    assert((pyre::h5::datatype<std::int32_t>() == H5::PredType::NATIVE_INT32));
    assert((pyre::h5::datatype<std::int64_t>() == H5::PredType::NATIVE_INT64));

    // floating point
    assert((pyre::h5::datatype<float>() == H5::PredType::NATIVE_FLOAT));
    assert((pyre::h5::datatype<double>() == H5::PredType::NATIVE_DOUBLE));

    // all done
    return 0;
}


// end of file

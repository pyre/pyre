// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// externals
#include <cassert>
// get the h5 support
#include <pyre/h5.h>


// check we can build the native datatypes
int
main()
{
    // instantiate the native types that are supported by {hdf5} out of the box
    auto charTp = pyre::h5::datatype<char>();
    auto shortTp = pyre::h5::datatype<short>();
    auto intTp = pyre::h5::datatype<int>();
    auto longTp = pyre::h5::datatype<long>();
    auto floatTp = pyre::h5::datatype<float>();
    auto doubleTp = pyre::h5::datatype<double>();

    // check them against the {H5} singletons
    assert((charTp == H5::PredType::NATIVE_CHAR));
    assert((shortTp == H5::PredType::NATIVE_SHORT));
    assert((intTp == H5::PredType::NATIVE_INT));
    assert((longTp == H5::PredType::NATIVE_LONG));
    assert((floatTp == H5::PredType::NATIVE_FLOAT));
    assert((doubleTp == H5::PredType::NATIVE_DOUBLE));

    // all done
    return 0;
}


// end of file

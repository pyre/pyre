// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2022 all rights reserved


// get the h5 support
#include <pyre/h5.h>


// heck we can build the native datatypes
int
main()
{
    // instantiate the native types
    [[maybe_unused]] auto charTp = pyre::h5::datatype<char>();
    [[maybe_unused]] auto shortTp = pyre::h5::datatype<short>();
    [[maybe_unused]] auto intTp = pyre::h5::datatype<int>();
    [[maybe_unused]] auto longTp = pyre::h5::datatype<long>();
    [[maybe_unused]] auto floatTp = pyre::h5::datatype<float>();
    [[maybe_unused]] auto doubleTp = pyre::h5::datatype<double>();

    // all done
    return 0;
}


// end of file

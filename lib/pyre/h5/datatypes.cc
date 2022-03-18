// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2022 all rights reserved


// grab my stuff
#include "public.h"


// forward declarations of my helper
template <typename valueT>
auto
make_complex() -> H5::CompType;


// my singletons
auto pyre::h5::NATIVE_COMPLEX_FLOAT = make_complex<float>();
auto pyre::h5::NATIVE_COMPLEX_DOUBLE = make_complex<double>();


// implementation of the type compositor
template <typename valueT>
auto
make_complex() -> H5::CompType
{
    // alias my {std::complex} instantiation
    using complex_t = std::complex<valueT>;

    // make a composite type of the right size
    H5::CompType complexTp(sizeof(complex_t));

    // add the real part
    complexTp.insertMember(
        // the name of the member
        "real",
        // its offset
        0,
        // and its type
        pyre::h5::datatype<typename complex_t::value_type>());

    // add the imaginary part
    complexTp.insertMember(
        // the name of the member
        "imag",
        // its offset
        sizeof(typename complex_t::value_type),
        // and its type
        pyre::h5::datatype<typename complex_t::value_type>());

    // all done
    return complexTp;
}


// end of file

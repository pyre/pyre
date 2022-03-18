// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2022 all rights reserved

// code guard
#if !defined(pyre_h5_forward_h)
#define pyre_h5_forward_h


// datatypes
namespace pyre::h5 {
    // the generic case
    template <typename cellT>
    auto datatype(const cellT * = nullptr) -> const H5::DataType &;

    // and its specializations
    template <>
    auto datatype(const char *) -> const H5::DataType &;
    template <>
    auto datatype(const short *) -> const H5::DataType &;
    template <>
    auto datatype(const int *) -> const H5::DataType &;
    template <>
    auto datatype(const long *) -> const H5::DataType &;
    template <>
    auto datatype(const float *) -> const H5::DataType &;
    template <>
    auto datatype(const double *) -> const H5::DataType &;
    template <>
    auto datatype(const std::complex<float> *) -> const H5::DataType &;
    template <>
    auto datatype(const std::complex<double> *) -> const H5::DataType &;

    // support for the two common {std::complex} instantiations
    extern H5::CompType NATIVE_COMPLEX_FLOAT;
    extern H5::CompType NATIVE_COMPLEX_DOUBLE;
} // namespace pyre::h5


#endif

// end of file

// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2022 all rights reserved

// code guard
#if !defined(pyre_h5_datatypes_h)
#define pyre_h5_datatypes_h

// and its specializations
template <>
auto
pyre::h5::datatype(const char *) -> const H5::DataType &
{
    // build a NATIVE char
    return H5::PredType::NATIVE_CHAR;
}

template <>
auto
pyre::h5::datatype(const short *) -> const H5::DataType &
{
    // build a NATIVE short
    return H5::PredType::NATIVE_SHORT;
}

template <>
auto
pyre::h5::datatype(const int *) -> const H5::DataType &
{
    // build a NATIVE int
    return H5::PredType::NATIVE_INT;
}

template <>
auto
pyre::h5::datatype(const long *) -> const H5::DataType &
{
    // build a NATIVE long
    return H5::PredType::NATIVE_LONG;
}

template <>
auto
pyre::h5::datatype(const float *) -> const H5::DataType &
{
    // build a NATIVE float
    return H5::PredType::NATIVE_FLOAT;
}

template <>
auto
pyre::h5::datatype(const double *) -> const H5::DataType &
{
    // build a NATIVE double
    return H5::PredType::NATIVE_DOUBLE;
}


#if 0
template <>
auto
pyre::h5::datatype(const std::complex<float> *) -> const H5::DataType &
{}

template <>
auto
pyre::h5::datatype(const std::complex<double> *) -> const H5::DataType &
{}
#endif


#endif

// end of file

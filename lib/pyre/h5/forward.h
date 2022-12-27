// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_h5_forward_h)
#define pyre_h5_forward_h


// datatypes
namespace pyre::h5 {
    // the generic case
    template <typename cellT>
    inline auto datatype(const cellT * = nullptr) -> const datatype_t &;

    // and its specializations
    template <>
    inline auto datatype(const char *) -> const datatype_t &;
    template <>
    inline auto datatype(const short *) -> const datatype_t &;
    template <>
    inline auto datatype(const int *) -> const datatype_t &;
    template <>
    inline auto datatype(const long *) -> const datatype_t &;
    template <>
    inline auto datatype(const float *) -> const datatype_t &;
    template <>
    inline auto datatype(const double *) -> const datatype_t &;
    template <>
    inline auto datatype(const std::complex<float> *) -> const datatype_t &;
    template <>
    inline auto datatype(const std::complex<double> *) -> const datatype_t &;

} // namespace pyre::h5


#endif

// end of file

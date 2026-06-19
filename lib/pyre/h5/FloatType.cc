// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// my declarations
#include "FloatType.h"
// the predefined type i can copy
#include "PredType.h"


// adopt an existing raw handle
pyre::h5::FloatType::FloatType(id_type id) : AtomType(id) {}


// make an independent copy of a predefined float type
pyre::h5::FloatType::FloatType(const PredType & type) :
    AtomType(static_cast<id_type>(H5Tcopy(type.id())))
{}


// my exponent bias
auto
pyre::h5::FloatType::bias() const -> std::size_t
{
    // ask the library
    return H5Tget_ebias(id());
}


// set my exponent bias
auto
pyre::h5::FloatType::setBias(std::size_t bias) -> void
{
    // hand it to the library
    H5Tset_ebias(id(), bias);
    // all done
    return;
}


// my mantissa normalization strategy
auto
pyre::h5::FloatType::normalization() const -> norm_type
{
    // ask the library
    return H5Tget_norm(id());
}


// set my mantissa normalization strategy
auto
pyre::h5::FloatType::setNorm(norm_type norm) -> void
{
    // hand it to the library
    H5Tset_norm(id(), norm);
    // all done
    return;
}


// my internal padding strategy
auto
pyre::h5::FloatType::inpad() const -> pad_type
{
    // ask the library
    return H5Tget_inpad(id());
}


// set my internal padding strategy
auto
pyre::h5::FloatType::setInpad(pad_type pad) -> void
{
    // hand it to the library
    H5Tset_inpad(id(), pad);
    // all done
    return;
}


// my bit layout
auto
pyre::h5::FloatType::fields() const -> fields_type
{
    // make room for the answer
    std::size_t spos, epos, esize, mpos, msize;
    // ask the library
    H5Tget_fields(id(), &spos, &epos, &esize, &mpos, &msize);
    // pack and ship
    return { spos, epos, esize, mpos, msize };
}


// set my bit layout
auto
pyre::h5::FloatType::setFields(
    std::size_t spos, std::size_t epos, std::size_t esize, std::size_t mpos,
    std::size_t msize) -> void
{
    // hand them to the library
    H5Tset_fields(id(), spos, epos, esize, mpos, msize);
    // all done
    return;
}


// end of file

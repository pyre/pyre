// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// my declarations
#include "Float.h"
// the predefined type i can copy
#include "Predefined.h"


// adopt an existing raw handle
pyre::h5::types::Float::Float(id_type id) : Atom(id) {}


// make an independent copy of a predefined float type
pyre::h5::types::Float::Float(const Predefined & type) :
    Atom(static_cast<id_type>(H5Tcopy(type.id())))
{}


// my exponent bias
auto
pyre::h5::types::Float::bias() const -> std::size_t
{
    // ask the library
    return H5Tget_ebias(id());
}


// set my exponent bias
auto
pyre::h5::types::Float::setBias(std::size_t bias) -> void
{
    // hand it to the library
    H5Tset_ebias(id(), bias);
    // all done
    return;
}


// my mantissa normalization strategy
auto
pyre::h5::types::Float::normalization() const -> norm_type
{
    // ask the library
    return H5Tget_norm(id());
}


// set my mantissa normalization strategy
auto
pyre::h5::types::Float::setNorm(norm_type norm) -> void
{
    // hand it to the library
    H5Tset_norm(id(), norm);
    // all done
    return;
}


// my internal padding strategy
auto
pyre::h5::types::Float::inpad() const -> pad_type
{
    // ask the library
    return H5Tget_inpad(id());
}


// set my internal padding strategy
auto
pyre::h5::types::Float::setInpad(pad_type pad) -> void
{
    // hand it to the library
    H5Tset_inpad(id(), pad);
    // all done
    return;
}


// my bit layout
auto
pyre::h5::types::Float::fields() const -> fields_type
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
pyre::h5::types::Float::setFields(
    std::size_t spos, std::size_t epos, std::size_t esize, std::size_t mpos,
    std::size_t msize) -> void
{
    // hand them to the library
    H5Tset_fields(id(), spos, epos, esize, mpos, msize);
    // all done
    return;
}


// end of file

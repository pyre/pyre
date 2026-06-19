// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// my declarations
#include "AtomType.h"


// adopt an existing raw handle
pyre::h5::AtomType::AtomType(id_type id) : DataType(id) {}


// my byte order
auto
pyre::h5::AtomType::order() const -> order_type
{
    // ask the library
    return H5Tget_order(id());
}


// set my byte order
auto
pyre::h5::AtomType::setOrder(order_type order) -> void
{
    // hand it to the library
    H5Tset_order(id(), order);
    // all done
    return;
}


// the bit offset of my first significant bit
auto
pyre::h5::AtomType::offset() const -> std::size_t
{
    // ask the library
    return H5Tget_offset(id());
}


// set the bit offset of my first significant bit
auto
pyre::h5::AtomType::setOffset(std::size_t offset) -> void
{
    // hand it to the library
    H5Tset_offset(id(), offset);
    // all done
    return;
}


// my (lsb, msb) padding strategy
auto
pyre::h5::AtomType::pad() const -> padding_type
{
    // make room for the answer
    pad_type lsb, msb;
    // ask the library
    H5Tget_pad(id(), &lsb, &msb);
    // pack and ship
    return { lsb, msb };
}


// set my (lsb, msb) padding strategy
auto
pyre::h5::AtomType::setPad(pad_type lsb, pad_type msb) -> void
{
    // hand them to the library
    H5Tset_pad(id(), lsb, msb);
    // all done
    return;
}


// my precision, in bits
auto
pyre::h5::AtomType::precision() const -> std::size_t
{
    // ask the library
    return H5Tget_precision(id());
}


// set my precision, in bits
auto
pyre::h5::AtomType::setPrecision(std::size_t precision) -> void
{
    // hand it to the library
    H5Tset_precision(id(), precision);
    // all done
    return;
}


// end of file

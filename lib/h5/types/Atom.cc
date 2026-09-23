// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// my declarations
#include "Atom.h"
// the reporting of library refusals
#include "../diagnostics.h"


// adopt an existing raw handle
pyre::h5::types::Atom::Atom(id_type id) : Datatype(id) {}


// my byte order
auto
pyre::h5::types::Atom::order() const -> order_type
{
    // ask the library
    auto answer = H5Tget_order(id());
    // if it refused
    if (answer == H5T_ORDER_ERROR) {
        // complain
        complain("pyre.h5.types", "retrieving the byte order of a datatype");
        // and hand back nothing
        return H5T_ORDER_ERROR;
    }
    // otherwise, report
    return answer;
}


// set my byte order
auto
pyre::h5::types::Atom::setOrder(order_type order) -> void
{
    // hand it to the library
    if (H5Tset_order(id(), order) < 0) {
        // and complain if it refused
        complain("pyre.h5.types", "setting the byte order of a datatype");
    }
    // all done
    return;
}


// the bit offset of my first significant bit
auto
pyre::h5::types::Atom::offset() const -> std::size_t
{
    // ask the library
    auto answer = H5Tget_offset(id());
    // if it refused
    if (answer < 0) {
        // complain
        complain("pyre.h5.types", "retrieving the bit offset of a datatype");
        // and hand back nothing
        return 0;
    }
    // otherwise, report
    return answer;
}


// set the bit offset of my first significant bit
auto
pyre::h5::types::Atom::setOffset(std::size_t offset) -> void
{
    // hand it to the library
    if (H5Tset_offset(id(), offset) < 0) {
        // and complain if it refused
        complain("pyre.h5.types", "setting the bit offset of a datatype");
    }
    // all done
    return;
}


// my (lsb, msb) padding strategy
auto
pyre::h5::types::Atom::pad() const -> padding_type
{
    // make room for the answer
    pad_type lsb, msb;
    // ask the library; an answer it refuses to give is not one to read
    if (H5Tget_pad(id(), &lsb, &msb) < 0) {
        // so complain
        complain("pyre.h5.types", "retrieving the padding of a datatype");
        // and hand back the error markers
        return { H5T_PAD_ERROR, H5T_PAD_ERROR };
    }
    // pack and ship
    return { lsb, msb };
}


// set my (lsb, msb) padding strategy
auto
pyre::h5::types::Atom::setPad(pad_type lsb, pad_type msb) -> void
{
    // hand them to the library
    if (H5Tset_pad(id(), lsb, msb) < 0) {
        // and complain if it refused
        complain("pyre.h5.types", "setting the padding of a datatype");
    }
    // all done
    return;
}


// my precision, in bits
auto
pyre::h5::types::Atom::precision() const -> std::size_t
{
    // ask the library
    auto answer = H5Tget_precision(id());
    // if it refused
    if (answer == 0) {
        // complain
        complain("pyre.h5.types", "retrieving the precision of a datatype");
        // and hand back nothing
        return 0;
    }
    // otherwise, report
    return answer;
}


// set my precision, in bits
auto
pyre::h5::types::Atom::setPrecision(std::size_t precision) -> void
{
    // hand it to the library
    if (H5Tset_precision(id(), precision) < 0) {
        // and complain if it refused
        complain("pyre.h5.types", "setting the precision of a datatype");
    }
    // all done
    return;
}


// end of file

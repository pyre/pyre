// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// my declarations
#include "String.h"
// the predefined type i can copy
#include "Predefined.h"


// adopt an existing raw handle
pyre::h5::types::String::String(id_type id) : Atom(id) {}


// make an independent copy of a predefined string type
pyre::h5::types::String::String(const Predefined & type) :
    Atom(static_cast<id_type>(H5Tcopy(type.id())))
{}


// make a native c-style string of the given number of {cells}
pyre::h5::types::String::String(int, std::size_t cells) :
    Atom(static_cast<id_type>(H5Tcopy(H5T_C_S1)))
{
    // size the fresh copy of the native c-string type
    setBytes(cells);
}


// my character set
auto
pyre::h5::types::String::charset() const -> cset_type
{
    // ask the library
    return H5Tget_cset(id());
}


// set my character set
auto
pyre::h5::types::String::setCset(cset_type cset) -> void
{
    // hand it to the library
    H5Tset_cset(id(), cset);
    // all done
    return;
}


// my padding strategy
auto
pyre::h5::types::String::strpad() const -> strpad_type
{
    // ask the library
    return H5Tget_strpad(id());
}


// set my padding strategy
auto
pyre::h5::types::String::setStrpad(strpad_type strpad) -> void
{
    // hand it to the library
    H5Tset_strpad(id(), strpad);
    // all done
    return;
}


// end of file

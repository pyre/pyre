// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// my declarations
#include "String.h"
// the reporting of library refusals
#include "../diagnostics.h"
// the predefined type i can copy
#include "Predefined.h"


// adopt an existing raw handle
pyre::h5::types::String::String(id_type id) : Atom(id) {}


// make an independent copy of a predefined string type
pyre::h5::types::String::String(const Predefined & type) :
    Atom(static_cast<id_type>(H5Tcopy(type.id())))
{
    // if the library refused
    if (!valid()) {
        // complain
        complain("pyre.h5.types", "copying a predefined string type");
    }
}


// make a native c-style string of the given number of {cells}
pyre::h5::types::String::String(int, std::size_t cells) :
    Atom(static_cast<id_type>(H5Tcopy(H5T_C_S1)))
{
    // if the library refused to copy the native c-string type
    if (!valid()) {
        // complain
        complain("pyre.h5.types", "copying the native c-string type");
        // and leave the size alone, since there is nothing to size
        return;
    }
    // size the fresh copy of the native c-string type
    setBytes(cells);
}


// my character set
auto
pyre::h5::types::String::charset() const -> cset_type
{
    // ask the library
    auto answer = H5Tget_cset(id());
    // if it refused
    if (answer == H5T_CSET_ERROR) {
        // complain
        complain("pyre.h5.types", "retrieving the character set of a string type");
        // and hand back nothing
        return H5T_CSET_ERROR;
    }
    // otherwise, report
    return answer;
}


// set my character set
auto
pyre::h5::types::String::setCset(cset_type cset) -> void
{
    // hand it to the library
    if (H5Tset_cset(id(), cset) < 0) {
        // and complain if it refused
        complain("pyre.h5.types", "setting the character set of a string type");
    }
    // all done
    return;
}


// my padding strategy
auto
pyre::h5::types::String::strpad() const -> strpad_type
{
    // ask the library
    auto answer = H5Tget_strpad(id());
    // if it refused
    if (answer == H5T_STR_ERROR) {
        // complain
        complain("pyre.h5.types", "retrieving the padding of a string type");
        // and hand back nothing
        return H5T_STR_ERROR;
    }
    // otherwise, report
    return answer;
}


// set my padding strategy
auto
pyre::h5::types::String::setStrpad(strpad_type strpad) -> void
{
    // hand it to the library
    if (H5Tset_strpad(id(), strpad) < 0) {
        // and complain if it refused
        complain("pyre.h5.types", "setting the padding of a string type");
    }
    // all done
    return;
}


// end of file

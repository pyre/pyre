// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// my declarations
#include "Int.h"
// the reporting of library refusals
#include "../diagnostics.h"
// the predefined type i can copy
#include "Predefined.h"


// adopt an existing raw handle
pyre::h5::types::Int::Int(id_type id) : Atom(id) {}


// make an independent copy of a predefined integer type
pyre::h5::types::Int::Int(const Predefined & type) : Atom(static_cast<id_type>(H5Tcopy(type.id())))
{
    // if the library refused
    if (!valid()) {
        // complain
        complain("pyre.h5.types", "copying a predefined integer type");
    }
}


// my sign type
auto
pyre::h5::types::Int::sign() const -> sign_type
{
    // ask the library
    auto answer = H5Tget_sign(id());
    // if it refused
    if (answer == H5T_SGN_ERROR) {
        // complain
        complain("pyre.h5.types", "retrieving the sign of an integer type");
        // and hand back nothing
        return H5T_SGN_ERROR;
    }
    // otherwise, report
    return answer;
}


// set my sign type
auto
pyre::h5::types::Int::setSign(sign_type sign) -> void
{
    // hand it to the library
    if (H5Tset_sign(id(), sign) < 0) {
        // and complain if it refused
        complain("pyre.h5.types", "setting the sign of an integer type");
    }
    // all done
    return;
}


// end of file

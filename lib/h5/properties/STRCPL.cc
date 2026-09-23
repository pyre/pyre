// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// my declarations
#include "STRCPL.h"
// the reporting of library refusals
#include "../diagnostics.h"


// adopt an existing raw handle
pyre::h5::properties::STRCPL::STRCPL(id_type id) : List(id) {}


// the character set the names i create are recorded in
auto
pyre::h5::properties::STRCPL::charEncoding() const -> H5T_cset_t
{
    // make room for the answer
    H5T_cset_t encoding = H5T_CSET_ASCII;
    // ask the library
    if (H5Pget_char_encoding(id(), &encoding) < 0) {
        // complain if it refused
        complain("pyre.h5.strcpl", "retrieving the character encoding");
        // and report the library default
        return H5T_CSET_ASCII;
    }
    // otherwise, report
    return encoding;
}


// set the character set
auto
pyre::h5::properties::STRCPL::charEncoding(H5T_cset_t encoding) -> void
{
    // hand it to the library
    if (H5Pset_char_encoding(id(), encoding) < 0) {
        // and complain if it refused
        complain("pyre.h5.strcpl", "setting the character encoding");
    }
    // all done
    return;
}


// end of file

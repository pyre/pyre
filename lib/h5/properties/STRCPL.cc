// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// my declarations
#include "STRCPL.h"


// adopt an existing raw handle
pyre::h5::properties::STRCPL::STRCPL(id_type id) : List(id) {}


// the character set the names i create are recorded in
auto
pyre::h5::properties::STRCPL::charEncoding() const -> H5T_cset_t
{
    // make room for the answer
    H5T_cset_t encoding = H5T_CSET_ASCII;
    // ask the library
    H5Pget_char_encoding(id(), &encoding);
    // and report
    return encoding;
}


// set the character set
auto
pyre::h5::properties::STRCPL::setCharEncoding(H5T_cset_t encoding) -> void
{
    // hand it to the library
    H5Pset_char_encoding(id(), encoding);
    // all done
    return;
}


// end of file

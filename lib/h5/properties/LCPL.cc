// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// my declarations
#include "LCPL.h"
// the reporting of library refusals
#include "../diagnostics.h"


// make a fresh link creation property list
pyre::h5::properties::LCPL::LCPL() : STRCPL(H5Pcreate(H5P_LINK_CREATE))
{
    // if the library refused to make it
    if (!valid()) {
        // complain
        complain("pyre.h5.lcpl", "creating a link creation property list");
    }
}


// adopt an existing raw handle
pyre::h5::properties::LCPL::LCPL(id_type id) : STRCPL(id) {}


// the shared default link creation property list
auto
pyre::h5::properties::LCPL::theDefault() -> const LCPL &
{
    // {H5P_DEFAULT} is a sentinel, not a live object, so wrapping it is inert
    static const LCPL theDefault { static_cast<id_type>(H5P_DEFAULT) };
    // hand it off
    return theDefault;
}


// whether missing intermediate groups are created on demand
auto
pyre::h5::properties::LCPL::intermediateGroupCreation() const -> bool
{
    // make room for the answer
    unsigned int create = 0;
    // ask the library
    if (H5Pget_create_intermediate_group(id(), &create) < 0) {
        // complain if it refused
        complain("pyre.h5.lcpl", "retrieving the intermediate group creation setting");
        // and report that none are created
        return false;
    }
    // otherwise, report
    return create != 0;
}


// set whether missing intermediate groups are created on demand
auto
pyre::h5::properties::LCPL::intermediateGroupCreation(bool create) -> void
{
    // hand it to the library
    if (H5Pset_create_intermediate_group(id(), create ? 1 : 0) < 0) {
        // and complain if it refused
        complain("pyre.h5.lcpl", "setting the intermediate group creation");
    }
    // all done
    return;
}


// end of file

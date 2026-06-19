// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// my declarations
#include "LCPL.h"


// make a fresh link creation property list
pyre::h5::properties::LCPL::LCPL() : List(H5Pcreate(H5P_LINK_CREATE)) {}


// adopt an existing raw handle
pyre::h5::properties::LCPL::LCPL(id_type id) : List(id) {}


// the shared default link creation property list
auto
pyre::h5::properties::LCPL::theDefault() -> const LCPL &
{
    // {H5P_DEFAULT} is a sentinel, not a live object, so wrapping it is inert
    static const LCPL theDefault { static_cast<id_type>(H5P_DEFAULT) };
    // hand it off
    return theDefault;
}


#if H5_VERSION_GE(1, 12, 0)
// whether missing intermediate groups are created on demand
auto
pyre::h5::properties::LCPL::createIntermediateGroup() const -> bool
{
    // make room for the answer
    unsigned int create = 0;
    // ask the library
    H5Pget_create_intermediate_group(id(), &create);
    // and report
    return create != 0;
}


// set whether missing intermediate groups are created on demand
auto
pyre::h5::properties::LCPL::setCreateIntermediateGroup(bool create) -> void
{
    // hand it to the library
    H5Pset_create_intermediate_group(id(), create ? 1 : 0);
    // all done
    return;
}
#endif


// the string character encoding
auto
pyre::h5::properties::LCPL::charEncoding() const -> H5T_cset_t
{
    // make room for the answer
    H5T_cset_t encoding = H5T_CSET_ASCII;
    // ask the library
    H5Pget_char_encoding(id(), &encoding);
    // and report
    return encoding;
}


// set the string character encoding
auto
pyre::h5::properties::LCPL::setCharEncoding(H5T_cset_t encoding) -> void
{
    // hand it to the library
    H5Pset_char_encoding(id(), encoding);
    // all done
    return;
}


// end of file

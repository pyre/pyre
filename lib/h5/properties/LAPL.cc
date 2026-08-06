// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// my declarations
#include "LAPL.h"


// make a fresh link access property list
pyre::h5::properties::LAPL::LAPL() : List(H5Pcreate(H5P_LINK_ACCESS)) {}


// adopt an existing raw handle
pyre::h5::properties::LAPL::LAPL(id_type id) : List(id) {}


// the shared default link access property list
auto
pyre::h5::properties::LAPL::theDefault() -> const LAPL &
{
    // {H5P_DEFAULT} is a sentinel, not a live object, so wrapping it is inert
    static const LAPL theDefault { static_cast<id_type>(H5P_DEFAULT) };
    // hand it off
    return theDefault;
}


// the number of allowed link traversals
auto
pyre::h5::properties::LAPL::traversalLimit() const -> std::size_t
{
    // make room for the answer
    std::size_t links = 0;
    // ask the library
    H5Pget_nlinks(id(), &links);
    // and report
    return links;
}


// set the number of allowed link traversals
auto
pyre::h5::properties::LAPL::traversalLimit(std::size_t links) -> void
{
    // hand it to the library
    H5Pset_nlinks(id(), links);
    // all done
    return;
}



// the prefix prepended to the filename an external link names
auto
pyre::h5::properties::LAPL::externalPrefix() const -> string_t
{
    // find out how long the prefix is
    auto len = H5Pget_elink_prefix(id(), nullptr, 0);
    // if there is none
    if (len <= 0) {
        // there is nothing to report
        return {};
    }
    // make room for it, plus the terminating null
    string_t buffer(len + 1, '\0');
    // retrieve it
    H5Pget_elink_prefix(id(), buffer.data(), len + 1);
    // trim the terminator and report
    buffer.resize(len);
    return buffer;
}


// set the prefix prepended to external link filenames
auto
pyre::h5::properties::LAPL::externalPrefix(const string_t & prefix) -> void
{
    // hand it to the library
    H5Pset_elink_prefix(id(), prefix.data());
    // all done
    return;
}


// end of file

// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2018 all rights reserved


// code guard
#if !defined(pyre_version_h)
#define pyre_version_h

// support
#include <array>

// my declarations
namespace pyre {
    // my version is an array of three integers
    typedef std::array<int, 3> version_t;

    // access to the version number of the {pyre} library
    version_t version();
}

#endif

// end of file

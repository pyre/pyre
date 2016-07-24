// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2016 all rights reserved
//

// code guard
#if !defined(pyre_memory_public_h)
#define pyre_memory_public_h

// externals
#include <stdexcept>
#include <utility>
// support
#include <pyre/journal.h>

// forward declarations
namespace pyre {
    namespace memory {
        // local type aliases
        // for filenames
        typedef std::string uri_t;
        // for describing shapes and regions
        typedef off_t offset_t;
        typedef std::size_t size_t;

        class Direct;
        class MemoryMap;
    }
}

// type aliases for the above
namespace pyre {
    namespace memory {
        // buffer types
        typedef Direct direct_t; // memory mapped file
    }
}


// the object model
#include "MemoryMap.h"
#include "Direct.h"

// the implementations
// memory mapping
#define pyre_memory_Direct_icc
#include "Direct.icc"
#undef pyre_memory_Direct_icc

#endif

// end of file

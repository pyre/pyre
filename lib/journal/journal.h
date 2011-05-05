// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
//


#if !defined(pyre_journal_h)
#define pyre_journal_h

// allow journal code to compile even without the runtime support
#if defined(WITHOUT_JOURNAL)


// ok: we have journal!
#else

// external packages
#include <map>
#include <vector>
#include <string>
#include <sstream>

// local declarations
// infrastructure
#include "journal/macros.h"
#include "journal/Inventory.h"
#include "journal/Index.h"
#include "journal/Channel.h"
#include "journal/Diagnostic.h"
// the predefined diagnostics
#include "journal/Debug.h"
// manipulators
#include "journal/Locator.h"
#include "journal/Selector.h"
#include "journal/manipulators.h"

// typedefs for convenience
namespace pyre {
    namespace journal {
        // diagnostics
        typedef Debug debug_t;

        // locators
        typedef Locator at;
        typedef Selector set;
    }
}

#endif // WITHOUT_JOURNAL

#endif // pyre_journal_h

// end of file

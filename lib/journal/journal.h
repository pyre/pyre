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
#include <string>

// local declarations
#include "journal/macros.h"
#include "journal/Inventory.h"
#include "journal/Index.h"
#include "journal/Channel.h"
#include "journal/Diagnostic.h"
#include "journal/Debug.h"

#include "journal/manipulators-0.h"
#include "journal/manipulators-1.h"
#include "journal/manipulators-3.h"

// typedefs for convenience
namespace pyre {
    namespace journal {
        typedef Debug debug_t;
    }
}

#endif // WITHOUT_JOURNAL

#endif // pyre_journal_h

// end of file

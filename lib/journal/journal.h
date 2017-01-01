// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2017 all rights reserved
//


#if !defined(pyre_journal_h)
#define pyre_journal_h

// external packages
#include <map>
#include <vector>
#include <string>
#include <sstream>

// local declarations
// infrastructure
#include "journal/Device.h"
#include "journal/Chronicler.h"
#include "journal/Inventory.h"
#include "journal/Index.h"
#include "journal/Channel.h"
#include "journal/Diagnostic.h"
// the predefined diagnostics
#include "journal/Debug.h"
#include "journal/Error.h"
#include "journal/Firewall.h"
#include "journal/Informational.h"
#include "journal/Null.h"
#include "journal/Warning.h"
// manipulators and associated support
#include "journal/macros.h"
#include "journal/Locator.h"
#include "journal/Selector.h"
#include "journal/manipulators.h"

// typedefs for convenience
// debugging support
namespace pyre {
    namespace journal {

        // debug
#if defined(DEBUG)
        typedef Debug debug_t;
#else
        typedef Null debug_t;
#endif

        // firewalls
#if defined(DEBUG)
        typedef Firewall firewall_t;
#else
        typedef Null firewall_t;
#endif
    }
}

// diagnostics
namespace pyre {
    namespace journal {
        // diagnostics
        typedef Error error_t;
        typedef Informational info_t;
        typedef Warning warning_t;

        // locators
        typedef Locator at;
        typedef Selector set;
    }
}

#endif // pyre_journal_h

// end of file

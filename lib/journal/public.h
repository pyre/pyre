// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2018 all rights reserved
//


#if !defined(pyre_journal_public_h)
#define pyre_journal_public_h

// external packages
#include <map>
#include <vector>
#include <string>
#include <sstream>

// local declarations
// infrastructure
#include "Device.h"
#include "Chronicler.h"
#include "Inventory.h"
#include "Index.h"
#include "Channel.h"
#include "Diagnostic.h"
// the predefined diagnostics
#include "Debug.h"
#include "Error.h"
#include "Firewall.h"
#include "Informational.h"
#include "Null.h"
#include "Warning.h"
// manipulators and associated support
#include "macros.h"
#include "Locator.h"
#include "Selector.h"
#include "manipulators.h"

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

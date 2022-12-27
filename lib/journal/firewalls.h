// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

#if !defined(pyre_journal_firewalls_h)
#define pyre_journal_firewalls_h


// the macros
#include "macros.h"


/* build the declarations of the bindings in a C-compatible way */
#ifdef __cplusplus
extern "C" {
#endif

    void firewall_hit(const char * channel, __HERE_DECL__, const char * fmt, ...);
    void firewall_check(const char * channel, int condition, __HERE_DECL__, const char * fmt, ...);

#ifdef __cplusplus
}
#endif


# endif

/* end of file */

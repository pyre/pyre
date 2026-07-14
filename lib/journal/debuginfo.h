// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// the macros
#include "macros.h"


/* build the declarations of the bindings in a C-compatible way */
#ifdef __cplusplus
extern "C" {
#endif

int
debuginfo_active(const char * name);
void
debuginfo_activate(const char * name);
void
debuginfo_deactivate(const char * name);
void
debuginfo_out(const char * name, __HERE_DECL__, const char * fmt, ...);

#ifdef __cplusplus
}
#endif


// end of file

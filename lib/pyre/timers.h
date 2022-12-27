// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_timers_h)
#define pyre_timers_h


// DESIGN NOTES

// The overarching goal is to simplify adding permanent instrumentation to gather timing
// information, e.g. for generating progress reports from long running processes, monitoring
// performance when the call stack based model supported by most profilers is not adequate,
// etc.

// Timer instances have names. The first time a name is encountered, the internal state of a
// timer is constructed and placed in a registry. Subsequent instantiations of timers of the
// same name anywhere in the program gain access to that shared state. This enables non-local
// access and frees the programmer from having to pass timers around. The caveat is that some
// effort must go into designing timer names so that they are intuitive and memorable. A useful
// trick is to construct name hierarchies using periods as the separators, and to name levels
// after execution phases rather that adhering to the call stack.

// Timers require clocks. Wherever supported, there are three types of clocks: wall time,
// process execution time, and thread execution time. Each type of timer keeps its own
// registry, so it is possible to reuse timer names.

// The package api consists of a set of type aliases that grant access to the supported
// timers. These aliases are defined in "timers/api.h". Anything else should be considered an
// implementation detail and may change.


// publish the interface
// the api is in "timers/api.h"
#include "timers/public.h"


#endif

// end of file

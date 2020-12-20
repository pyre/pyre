// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2020 all rights reserved

// code guard
#if !defined(pyre_memory_h)
#define pyre_memory_h


// Encapsulation of allocation, ownership, and access policies for memory blocks

// This package was born while implementing {grid}, a flexible multi-dimensional array. It
// became apparent very quickly that the implementation of multi-dimensional arrays can be
// factored into two distinct parts: the indexing problem that is responsible for mapping index
// tuples into linear offsets, and the memory problem where the issue is where the information
// is stored, what the access privileges are, and who owns and therefore is responsible for the
// clean up.

// The current implementation supports
// - allocation on the heap
// - views to memory owned by foreign entities, as long as they can expose it
// - memory mapped files, a technique that provide significant performance improvements over
//   file IO when accessing large objects

// publish the interface
// the api is in "memory/api.h"
#include "memory/public.h"


#endif

// end of file

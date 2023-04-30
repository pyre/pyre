// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_memory_h)
#define pyre_memory_h


// Encapsulation of allocation, ownership, and access policies for memory blocks

// This package was born while implementing {grid}, a flexible multidimensional array. It
// became apparent very quickly that the implementation of multidimensional arrays can be
// factored into two distinct parts: the indexing problem that is responsible for mapping index
// tuples into linear offsets, and the memory problem where the issue is where the information
// is stored, what the access privileges are, and who owns and therefore is responsible for the
// clean up.

// The current implementation supports
//
// - allocation on the heap; see {heap_t}
// - allocation on the stack; see {stack_t}
// - memory mapped files, a technique that provides significant performance improvements over
//   file IO when accessing large objects; see {map_t}
// - views to memory owned by other entities, as long as they can expose it; see {view_t}
//
// there are {const} versions of all of the above that support read-only buffers

// publish the interface
// the api is in "memory/api.h"
#include "memory/public.h"


#endif

// end of file

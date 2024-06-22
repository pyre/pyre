// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2024 all rights reserved

// code guard
#if !defined(pyre_memory_expansions_h)
#define pyre_memory_expansions_h


// template expansion machinery
namespace pyre::memory {
    // a compile-time container with type choices
    template <typename... typeT>
    struct Types;

    // the container with the strategy choices
    template <template <typename typeT> class... strategyT>
    struct StorageStrategies;

    // type list concatenation
    template <typename... listsT>
    struct Concat;

    // compose a storage strategy with a set of types
    template <template <typename> class strategyT, typename... cellsT>
    struct Compose;

    // a helper that expands a set of strategies and a set of cells
    template <typename strategiesT, typename cellsT>
    struct Expand;
} // namespace pyre::memory


// get the inline definitions
#define pyre_memory_expansions_icc
#include "expansions.icc"
#undef pyre_memory_expansions_icc


#endif

// end of file

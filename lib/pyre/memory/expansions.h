// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


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
    struct ComposeStorageStrategy;

    // a helper that expands a set of strategies and a set of cells
    template <typename strategiesT, typename cellsT>
    struct ExpandStorageStrategies;
} // namespace pyre::memory


// get the inline definitions
#include "expansions.icc"


// end of file

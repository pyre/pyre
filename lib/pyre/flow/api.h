// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "forward.h"


// publicly visible types
namespace pyre::flow {

    // base classes
    using node_t = protocols::Node;
    using factory_t = protocols::Factory;
    using product_t = protocols::Product;

    // shared pointers
    using node_ref_t = std::shared_ptr<node_t>;
    using factory_ref_t = std::shared_ptr<factory_t>;
    using product_ref_t = std::shared_ptr<product_t>;

    // weak pointers
    using node_weakref_t = std::weak_ptr<node_t>;
    using factory_weakref_t = std::weak_ptr<factory_t>;
    using product_weakref_t = std::weak_ptr<product_t>;

} // namespace pyre::flow

// the api of each sub-namespace
#include "protocols/api.h"
#include "products/api.h"
#include "factories/api.h"
#include "catalog/api.h"


// end of file

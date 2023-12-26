// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#pragma once

// publicly visible types
namespace pyre::flow {

    // base classes
    using node_t = protocol::Node;
    using factory_t = protocol::Factory;
    using product_t = protocol::Product;

    // shared pointers
    using node_ref_t = std::shared_ptr<node_t>;
    using factory_ref_t = std::shared_ptr<factory_t>;
    using product_ref_t = std::shared_ptr<product_t>;

    // weak pointers
    using node_weakref_t = std::weak_ptr<node_t>;
    using factory_weakref_t = std::weak_ptr<factory_t>;
    using product_weakref_t = std::weak_ptr<product_t>;

} // namespace pyre::flow

// end of file

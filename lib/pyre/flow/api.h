// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#pragma once

// publicly visible types
namespace pyre::flow {

    // base classes
    using node_t = Node;
    using factory_t = Factory;
    using product_t = Product;

    // shared pointers
    using node_ref_t = std::shared_ptr<Node>;
    using factory_ref_t = std::shared_ptr<Factory>;
    using product_ref_t = std::shared_ptr<Product>;

    // weak pointers
    using node_weakref_t = std::weak_ptr<Node>;
    using factory_weakref_t = std::weak_ptr<Factory>;
    using product_weakref_t = std::weak_ptr<Product>;

} // namespace pyre::flow

// end of file

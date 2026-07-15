// -*- C++ -*-
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

// products
namespace pyre::flow::products {
    // atoms
    template <typename valueT>
    using var_t = Variable<valueT>;
    // tiles
    template <class gridT>
    using tile_t = Tile<gridT>;
} // namespace pyre::flow::products

// factories
namespace pyre::flow::factories {
    // addition
    // atoms
    template <class op1T, class op2T = op1T, class resultT = op1T>
    using add_variables_t = Add<products::Variable, op1T, op2T, resultT>;
    // tiles
    template <class op1T, class op2T = op1T, class resultT = op1T>
    using add_tiles_t = Add<products::Tile, op1T, op2T, resultT>;

    // multiplication
    // atoms
    template <class op1T, class op2T = op1T, class resultT = op1T>
    using multiply_variables_t = Multiply<products::Variable, op1T, op2T, resultT>;
    // tiles
    template <class op1T, class op2T = op1T, class resultT = op1T>
    using multiply_tiles_t = Multiply<products::Tile, op1T, op2T, resultT>;
} // namespace pyre::flow::factories

// end of file

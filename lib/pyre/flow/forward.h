// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2024 all rights reserved

// code guard
#pragma once

// base classes
namespace pyre::flow::protocol {

    // base classes
    class Node;
    class Product;
    class Factory;

} // namespace pyre::flow::protocol

// products
namespace pyre::flow::products {

    // atoms
    template <typename valueT>
    class Variable;

    // tiles over grids
    template <class gridT>
    class Tile;

} // namespace pyre::flow::products

// factories
namespace pyre::flow::factories {
    // arithmetic

    // binary operators
    template <template <typename> class categoryT, class op1T, class op2T, class resultT>
    class Binary;

    // addition
    // the general case; not implemented
    template <template <typename> class categoryT, class op1T, class op2T, class resultT>
    class Add;
    // adding tiles
    template <class op1T, class op2T, class resultT>
    class Add<products::Tile, op1T, op2T, resultT>;
    // adding variables
    template <class op1T, class op2T, class resultT>
    class Add<products::Variable, op1T, op2T, resultT>;

    // multiplication
    // the general case; not implemented
    template <template <typename> class categoryT, class op1T, class op2T, class resultT>
    class Multiply;
    // adding tiles
    template <class op1T, class op2T, class resultT>
    class Multiply<products::Tile, op1T, op2T, resultT>;
    // adding variables
    template <class op1T, class op2T, class resultT>
    class Multiply<products::Variable, op1T, op2T, resultT>;

} // namespace pyre::flow::factories

// end of file

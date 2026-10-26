// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "../../externals.h"
#include "../../products/forward.h"
// the operations
#include "Operation.h"


// the rules of arithmetic among products
namespace pyre::flow::factories::operators {
    // the numbers the arithmetic works with: the reals and the complex numbers, which are
    // fields; the integers are not, since they do not divide, so they are left out
    template <typename T>
    concept number_c = std::floating_point<T>
                    || (pyre::memory::complex_c<T> && std::floating_point<typename T::value_type>);

    // a scalar is a product that holds a single number
    template <class productT>
    concept scalar_c = requires { typename productT::cell_type; }
                    && std::same_as<productT, products::Variable<typename productT::cell_type>>
                    && number_c<typename productT::cell_type>;

    // a tile is a product that holds a grid of numbers, one in each of its cells; the tiles
    // form a vector space over the scalars
    template <class productT>
    concept tile_c = requires { typename productT::grid_type; }
                  && std::same_as<productT, products::Tile<typename productT::grid_type>>
                  && number_c<typename productT::cell_type>;

    // two tiles are on the same footing when they lay out their cells the same way
    template <class tile1T, class tile2T>
    concept aligned_c = std::same_as<typename tile1T::packing_type, typename tile2T::packing_type>;

    // the result of an operation on two operands holds exactly the number the operation makes
    // of a cell of each, so that nothing is narrowed on the way
    template <class operationT, class op1T, class op2T, class resultT>
    concept exact_c = std::same_as<
        std::invoke_result_t<operationT, typename op1T::cell_type, typename op2T::cell_type>,
        typename resultT::cell_type>;

    // the combinations of operands the math allows: two scalars make a scalar, whatever the
    // operation; tiles combine with tiles to make a tile, when the operation says so; and a
    // tile and a scalar make a tile, on whichever side the operation allows the scalar to be
    template <class operationT, class op1T, class op2T, class resultT>
    concept arithmetic_c =
        // the cells of the result
        exact_c<operationT, op1T, op2T, resultT>
        && (
            // two scalars
            (scalar_c<op1T> && scalar_c<op2T> && scalar_c<resultT>)
            // two tiles
            || (tile_c<op1T> && tile_c<op2T> && tile_c<resultT> && aligned_c<op1T, resultT>
                && aligned_c<op2T, resultT> && Operation<operationT>::tiles)
            // a tile and a scalar
            || (tile_c<op1T> && scalar_c<op2T> && tile_c<resultT> && aligned_c<op1T, resultT>
                && Operation<operationT>::tileScalar)
            // a scalar and a tile
            || (scalar_c<op1T> && tile_c<op2T> && tile_c<resultT> && aligned_c<op2T, resultT>
                && Operation<operationT>::scalarTile));
} // namespace pyre::flow::factories::operators


// end of file

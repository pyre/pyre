// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_grid_Shape_h)
#define pyre_grid_Shape_h


// the specification of the number of possible index values along each dimension
// this class stores the {s_i} in
//
//     Z_s_0 x ... x Z_s_{n-1}
//
template <class containerT>
class pyre::grid::Shape : public Product<containerT> {
    // types
public:
    // alias for me
    using shape_type = Shape<containerT>;
    // alias for my base
    using rep_type = Product<containerT>;
    // individual axis values
    using rank_type = typename rep_type::value_type;
    using rank_reference = rank_type &;
    using rank_const_reference = const rank_type &;

    // metamethods
public:
    // constructor; works with initializer lists
    template <typename... argT>
    constexpr Shape(argT... args);

    // interface
public:
    // the total number of addressable values
    constexpr auto cells() const -> std::size_t;

    // default metamethods
public:
    // destructor
    ~Shape() = default;
    // constructors
    Shape(const Shape &) = default;
    Shape(Shape &&) = default;
    Shape & operator=(const Shape &) = default;
    Shape & operator=(Shape &&) = default;
};


// get the inline definitions
#define pyre_grid_Shape_icc
#include "Shape.icc"
#undef pyre_grid_Shape_icc


#endif

// end of file

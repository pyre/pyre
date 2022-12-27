// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_grid_Index_h)
#define pyre_grid_Index_h


// storage for a multidimensional index
// resist the temptation to use unsigned types as the fundamental representation type; they
// complicate index arithmetic unnecessarily

// basic index type
template <class containerT>
class pyre::grid::Index : public Product<containerT> {
    // types
public:
    // alias for me
    using index_type = Index<containerT>;
    // alias for my base
    using rep_type = Product<containerT>;
    // individual axis values
    using rank_type = typename rep_type::value_type;
    using rank_reference = rank_type &;
    using rank_const_reference = const rank_type &;

    // metamethods
public:
    // constructor that fills an index with a given {value}
    constexpr explicit Index(rank_type);

    // constructor; a variadic template to enable initializer lists
    template <typename... argT>
    constexpr Index(argT...);

    // default metamethods
public:
    // destructor
    ~Index() = default;
    // constructors
    Index(const Index &) = default;
    Index(Index &&) = default;
    Index & operator=(const Index &) = default;
    Index & operator=(Index &&) = default;
};


// get the inline definitions
#define pyre_grid_Index_icc
#include "Index.icc"
#undef pyre_grid_Index_icc


#endif

// end of file

// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2017 all rights reserved
//

// code guard
#if !defined(pyre_grid_Slice_h)
#define pyre_grid_Slice_h


// declaration
template <typename indexT, typename orderT>
class pyre::grid::Slice {
    // types
public:
    // for sizing things
    typedef std::size_t size_type;
    // aliases for my parts
    typedef indexT index_type;
    typedef orderT order_type;
    // alias for me
    typedef Slice<index_type, order_type> slice_type;
    // iterators
    typedef Iterator<slice_type> iterator_type;

    // meta-methods
public:
    // a slice is the set of indices [low, high) visited in a given order
    Slice(const index_type & low, const index_type & high, const order_type & order);

    // interface
public:
    inline const auto & low() const;
    inline const auto & high() const;
    inline const auto & order() const;

    // iteration support
    inline auto begin() const;
    inline auto end() const;

    // implementation details
private:
    const index_type _low;
    const index_type _high;
    const order_type _order;
};


# endif

// end of file

// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2016 all rights reserved
//

// code guard
#if !defined(pyre_geometry_Slice_h)
#define pyre_geometry_Slice_h


// declaration
template <typename tileT>
class pyre::geometry::Slice {
    // types
public:
    // for sizing things
    typedef std::size_t size_type;
    // alias for my template parameter
    typedef tileT tile_type;
    // easy access to deduced types
    typedef typename tile_type::index_type index_type;
    typedef typename tile_type::order_type order_type;
    typedef typename tile_type::iterator_type iterator_type;

    // meta-methods
public:
    // slice the whole tile but change the order
    Slice(const tile_type & tile, const order_type & order);

    // slice the tile between {low} and {high}, and visit with the given {order}
    Slice(const tile_type & tile,
          const index_type & low, const index_type & high,
          const order_type & order);

    // interface
public:
    inline const auto & low() const;
    inline const auto & high() const;
    inline const auto & order() const;

    // compute the pixel offset implied by a given index
    // compute the index that corresponds to a given offset
    inline auto offset(const index_type & index) const;
    inline auto index(size_type offset) const;

    // syntactic sugar for the pair above
    inline auto operator[](const index_type & index) const;
    inline auto operator[](size_type offset) const;

    // iteration support
    inline auto begin() const;
    inline auto end() const;

    // implementation details
private:
    const tile_type _tile;
    const index_type _low;
    const index_type _high;
    const order_type _order;
};


# endif

// end of file

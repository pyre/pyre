// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2016 all rights reserved
//

// code guard
#if !defined(pyre_geometry_Tile_h)
#define pyre_geometry_Tile_h

// declaration
template <typename indexT, typename orderT>
class pyre::geometry::Tile {
    // types
public:
    // for sizing things
    typedef std::size_t size_type;
    // aliases for my parts
    typedef indexT index_type;
    typedef orderT order_type;
    // slices
    typedef Slice<Tile> slice_type;
    // iterator
    typedef Iterator<index_type, order_type> iterator_type;

    // meta-methods
public:
    Tile(index_type shape, order_type order);

    // interface
public:
    // accessors
    inline const auto & shape() const;
    inline const auto & order() const;

    // the number of cells in this tile
    inline auto size() const;

    // compute the pixel offset implied by a given index
    inline auto offset(const index_type & index) const;
    // compute the index that corresponds to a given offset
    inline auto index(size_type offset) const;

    // syntactic sugar for the pair above
    inline auto operator[](const index_type & index) const;
    inline auto operator[](size_type offset) const;

    // iteration support
    inline auto begin() const;
    inline auto end() const;

    // iterating over slices in arbitrary order
    auto slice(const order_type & order) const;
    auto slice(const index_type & begin, const index_type & end) const;
    auto slice(const index_type & begin, const index_type & end, const order_type & order) const;

    // implementation details
private:
    const index_type _shape;
    const order_type _order;
};


#endif

// end of file

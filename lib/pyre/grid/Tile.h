// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2016 all rights reserved
//

// code guard
#if !defined(pyre_grid_Tile_h)
#define pyre_grid_Tile_h

// declaration
template <typename indexT, typename orderT>
class pyre::grid::Tile : public Slice<indexT, orderT> {
    // types
public:
    // for sizing things
    typedef std::size_t size_type;
    // aliases for my parts
    typedef indexT index_type;
    typedef orderT order_type;
    typedef Slice<indexT, orderT> slice_type;

    // meta-methods
public:
    // a tile with index ordering supplied by the caller
    Tile(index_type shape, order_type order = order_type::rowMajor());

    // interface
public:
    // accessors
    inline const auto & shape() const;

    // the number of cells in this tile
    inline auto size() const;

    // compute the pixel offset implied by a given index
    inline auto offset(const index_type & index) const;
    // compute the index that corresponds to a given offset
    inline auto index(size_type offset) const;

    // syntactic sugar for the pair above
    inline auto operator[](const index_type & index) const;
    inline auto operator[](size_type offset) const;

    // iterating over slices in arbitrary order
    auto slice(const order_type & order) const;
    auto slice(const index_type & begin, const index_type & end) const;
    auto slice(const index_type & begin, const index_type & end, const order_type & order) const;
};


#endif

// end of file

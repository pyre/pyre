// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2017 all rights reserved
//

// A grid

// code guard
#if !defined(pyre_grid_Grid_h)
#define pyre_grid_Grid_h

// declaration
template <typename cellT, typename tileT, typename storageT>
class pyre::grid::Grid {
    // types
public:
    // aliases for my template parameters
    typedef cellT cell_type;
    typedef tileT tile_type;
    typedef storageT storage_type;
    // dependent types
    typedef typename tile_type::index_type index_type;
    typedef typename tile_type::packing_type packing_type;

    // other help
    typedef std::size_t size_type;

    // meta-methods
public:
    // given a shape and a storage solution managed by someone else
    inline Grid(tile_type shape, const storage_type & storage);
    // given a shape and a storage solution managed by me
    inline Grid(tile_type shape, storage_type && storage);
    // given a shape and a storage solution that can be instantiated using my shape info
    inline Grid(tile_type shape);
    // given just the index extents
    inline Grid(index_type shape);

    // interface
public:
    // access to my shape
    inline const auto & shape() const;
    // access to my memory location
    inline const auto data() const;

    // read and write access using offsets
    inline auto & operator[](size_type offset);
    inline const auto & operator[](size_type offset) const;

    // read and write access using indices
    inline auto & operator[](const index_type & index);
    inline const auto & operator[](const index_type & index) const;

    // implementation details - data
private:
    const tile_type _shape;
    const storage_type _storage;
};


#endif

// end of file

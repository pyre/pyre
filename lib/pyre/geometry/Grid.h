// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2016 all rights reserved
//

// A grid

// declaration
template <typename cellT, typename tileT, typename storageT>
class pyre::geometry::Grid {
    // types
public:
    // aliases for my template parameters
    typedef cellT cell_type;
    typedef tileT tile_type;
    typedef storageT storage_type;
    // dependent types
    typedef typename tile_type::index_type index_type;
    typedef typename tile_type::order_type order_type;

    // othe help
    typedef std::size_t size_type;

    // meta-methods
public:
    inline Grid(tile_type shape, const storage_type & storage);
    inline Grid(tile_type shape, storage_type && storage);

    // interface
public:
    // access to my shape
    auto shape() const;

    // read and write access using offsets
    inline auto & operator[](size_type offset);
    inline auto operator[](size_type offset) const;

    // read and write access using indices
    inline auto & operator[](const index_type & index);
    inline auto operator[](const index_type & index) const;

    // implementation details - data
private:
    const tile_type _shape;
    const storage_type _storage;
    cell_type * const _cells;
};


// end of file

// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2018 all rights reserved
//

// A grid

// code guard
#if !defined(pyre_grid_Grid_h)
#define pyre_grid_Grid_h

// declaration
template <typename cellT, typename layoutT, typename storageT>
class pyre::grid::Grid {
    // types
public:
    // aliases for my template parameters
    typedef cellT cell_type;
    typedef layoutT layout_type;
    typedef storageT storage_type;
    // dependent types
    typedef typename layout_type::index_type index_type;
    typedef typename layout_type::shape_type shape_type;
    typedef typename layout_type::packing_type packing_type;

    // other help
    typedef std::size_t size_type;

    // meta-methods
public:
    // given a layout and a storage solution managed by someone else
    inline Grid(layout_type layout, const storage_type & storage);
    // given a layout and a storage solution managed by me
    inline Grid(layout_type layout, storage_type && storage);
    // given a layout and a storage solution that can be instantiated using my shape info
    inline Grid(layout_type layout);
    // given just the index extents
    inline Grid(shape_type shape);

    // interface
public:
    // the dimensionality of my index
    inline static constexpr auto dim();

    // access to my shape
    inline const auto & layout() const;
    // access to my memory location
    inline auto data() const;
    // access to my storage strategy
    inline const auto & storage() const;

    // read and write access using offsets
    inline auto & operator[](size_type offset);
    inline auto & operator[](size_type offset) const;

    // read and write access using indices
    inline auto & operator[](const index_type & index);
    inline const auto & operator[](const index_type & index) const;

    // implementation details - data
private:
    const layout_type _layout;
    const storage_type _storage;
};


#endif

// end of file

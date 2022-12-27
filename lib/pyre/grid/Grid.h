// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_grid_Grid_h)
#define pyre_grid_Grid_h


template <class packingT, class storageT>
class pyre::grid::Grid {
    // types
public:
    // aliases for my template parameters
    using packing_type = packingT;
    using storage_type = storageT;

    // me
    using grid_type = Grid<packing_type, storage_type>;

    // my value
    using value_type = typename storage_type::value_type;
    using pointer = typename storage_type::pointer;
    using const_pointer = typename storage_type::const_pointer;
    using reference = typename storage_type::reference;
    using const_reference = typename storage_type::const_reference;
    // distances
    using difference_type = typename storage_type::difference_type;

    // my parts
    using storage_pointer = std::shared_ptr<storage_type>;
    using packing_const_reference = const packing_type &;
    // my shape
    using shape_type = typename packing_type::shape_type;
    using shape_const_reference = const shape_type &;
    // my index
    using index_type = typename packing_type::index_type;
    using index_const_reference = const index_type &;
    // iterators
    using index_iterator = typename packing_type::index_iterator;
    using iterator = GridIterator<grid_type, index_iterator, false>;
    using const_iterator = GridIterator<grid_type, index_iterator, true>;

    // metamethods
public:
    // constructor that makes a grid using the supplied packing and storage strategies
    constexpr Grid(packing_const_reference, storage_pointer);

    // constructor that forwards its extra arguments to the storage strategy
    template <typename... Args>
    constexpr Grid(packing_const_reference, Args &&...);

    // accessors
public:
    constexpr auto data() const -> storage_pointer;
    constexpr auto layout() const -> packing_const_reference;

    // interface: data access
public:
    // with bounds check
    constexpr auto at(difference_type) const -> reference;
    constexpr auto at(index_const_reference) const -> reference;
    // without bounds check
    constexpr auto operator[](difference_type) const -> reference;
    constexpr auto operator[](index_const_reference) const -> reference;

    // interface: iteration support
public:
    // whole grid iteration: visit every value in my native packing order
    constexpr auto begin() -> iterator;
    constexpr auto begin(index_type) -> iterator;
    constexpr auto end() -> iterator;
    // const
    constexpr auto begin() const -> const_iterator;
    constexpr auto begin(index_type) const -> const_iterator;
    constexpr auto end() const -> const_iterator;
    // and again, for non-const grids
    constexpr auto cbegin() const -> const_iterator;
    constexpr auto cbegin(index_type) const -> const_iterator;
    constexpr auto cend() const -> const_iterator;

    // iterate over a portion of the grid
    constexpr auto box(packing_const_reference) const -> grid_type;
    constexpr auto box(index_const_reference, shape_const_reference) const -> grid_type;

    // slicing: create subgrids of a given shape anchored at the given index; rank reduction is
    // achieved by zeroing out the ranks to be skipped in the shape specification
public:
    template <int sliceRank = packing_type::rank()>
    constexpr auto slice(index_const_reference, shape_const_reference) const;

    // implementation details: data
private:
    const packing_type _layout;
    const storage_pointer _data;

    // default metamethods
public:
    // destructor
    ~Grid() = default;
    // constructors
    Grid(const Grid &) = default;
    Grid(Grid &&) = default;
    Grid & operator=(const Grid &) = default;
    Grid & operator=(Grid &&) = default;
};


// get the inline definitions
#define pyre_grid_Grid_icc
#include "Grid.icc"
#undef pyre_grid_Grid_icc


#endif

// end of file

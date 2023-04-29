// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_grid_GridIterator_h)
#define pyre_grid_GridIterator_h


// in iterator that visit the cells of a grid in a specific order
template <class gridT, class indexIteratorT, bool isConst>
class pyre::grid::GridIterator : public iterator_base<gridT, isConst> {
    // types
public:
    // my template parameters
    using grid_type = gridT;
    using index_iterator = indexIteratorT;
    // me
    using iterator = GridIterator<grid_type, indexIteratorT, isConst>;
    using iterator_reference = iterator &;
    // my base class
    using iterbase = iterator_base<grid_type, isConst>;
    // my parts
    using grid_reference = std::conditional_t<isConst, const grid_type &, grid_type &>;
    using grid_const_reference = const grid_type &;
    using index_const_iterator_reference = const index_iterator &;
    // what i point to
    using value_type = typename iterbase::value_type;
    using pointer = typename iterbase::pointer;
    using reference = typename iterbase::reference;

    // metamethods
public:
    // constructor
    constexpr GridIterator(grid_reference, index_const_iterator_reference);

    // iterator protocol
public:
    // dereference
    constexpr auto operator*() const -> reference;
    // arithmetic
    constexpr auto operator++() -> iterator_reference;
    constexpr auto operator++(int) -> iterator;

    // accessors: needed so {operator==} doesn't have to be a friend
public:
    constexpr auto grid() const -> grid_const_reference;
    constexpr auto iter() const -> index_const_iterator_reference;

    // implementation details: data
private:
    grid_reference _grid;
    index_iterator _idxptr;

    // default metamethods
public:
    // destructor
    ~GridIterator() = default;
    // let the compiler write the rest
    constexpr GridIterator(const GridIterator &) = default;
    constexpr GridIterator(GridIterator &&) = default;
    constexpr GridIterator & operator=(const GridIterator &) = default;
    constexpr GridIterator & operator=(GridIterator &&) = default;
};


// get the inline definitions
#define pyre_grid_GridIterator_icc
#include "GridIterator.icc"
#undef pyre_grid_GridIterator_icc


#endif

// end of file

// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_grid_IndexIterator_h)
#define pyre_grid_IndexIterator_h


// iterators generate sequences of indices from a packing strategy according to a specific
// order
template <class packingT>
class pyre::grid::IndexIterator : public base_index_iterator<packingT> {
    // types
public:
    // my template parameter
    using packing_type = packingT;
    // alias for me
    using iterator = IndexIterator<packing_type>;
    // references to me
    using iterator_reference = iterator &;
    // and my base
    using base_type = base_index_iterator<packing_type>;
    // my parts
    using index_type = typename packing_type::index_type;
    using shape_type = typename packing_type::shape_type;
    using order_type = typename packing_type::order_type;
    // my value type
    using index_const_reference = const index_type &;
    using shape_const_reference = const shape_type &;
    using order_const_reference = const order_type &;
    // ranks
    using rank_type = typename index_type::rank_type;

    // metamethods
public:
    // constructors
    // shape, order, origin
    constexpr IndexIterator(shape_const_reference, order_const_reference, index_const_reference);
    // shape, order, origin, step
    constexpr IndexIterator(shape_const_reference, order_const_reference,
                            index_const_reference, index_const_reference);

    // iterator protocol
public:
    // dereference
    constexpr auto operator*() const -> index_const_reference;
    // arithmetic
    constexpr auto operator++() -> iterator_reference;
    constexpr auto operator++(int) -> iterator;

    // implementation details: data
private:
    index_type _current;            // the current value of the index
    const shape_type _shape;        // the shape of the packing
    const order_type _order;        // the index ordering determines the iteration order
    const index_type _origin;       // the lowest possible value
    const index_type _step;         // the desired increment along each rank

    // default metamethods
public:
    // destructor
    ~IndexIterator() = default;
    // let the compiler write the rest
    constexpr IndexIterator(const IndexIterator &) = default;
    constexpr IndexIterator(IndexIterator &&) = default;
    constexpr IndexIterator & operator=(const IndexIterator &) = default;
    constexpr IndexIterator & operator=(IndexIterator &&) = default;
};


// get the inline definitions
#define pyre_grid_IndexIterator_icc
#include "IndexIterator.icc"
#undef pyre_grid_IndexIterator_icc


#endif

// end of file

// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// support
#include "forward.h"


// iterator that generates the sequence of indices that visit every point in a box
// in a traversal order determined by an {Order}
template <std::size_t Rank>
class pyre::grid::IndexIterator {
    // types
public:
    // myself
    using self_type = IndexIterator<Rank>;
    // my parts
    using index_type = Index<Rank>;
    using shape_type = Shape<Rank>;
    using order_type = Order<Rank>;
    // iterator traits for STL compatibility
    using value_type = index_type;
    using reference = const index_type &;
    using pointer = const index_type *;
    using difference_type = std::ptrdiff_t;
    using iterator_category = std::forward_iterator_tag;

    // metamethods
public:
    // singular iterator; satisfies the std::regular requirement on forward iterators
    constexpr IndexIterator() noexcept = default;
    // construct from a shape, a traversal order, and a starting index
    constexpr IndexIterator(
        const shape_type &, const order_type &, const index_type &) noexcept;

    // default metamethods
public:
    ~IndexIterator() = default;
    IndexIterator(const IndexIterator &) noexcept = default;
    IndexIterator(IndexIterator &&) noexcept = default;
    auto operator=(const IndexIterator &) noexcept -> self_type & = default;
    auto operator=(IndexIterator &&) noexcept -> self_type & = default;

    // iterator protocol
public:
    [[nodiscard]] constexpr auto operator*() const noexcept -> reference;
    constexpr auto operator++() noexcept -> self_type &;
    constexpr auto operator++(int) noexcept -> self_type;

    // implementation details
private:
    index_type _current {};
    shape_type _shape {};
    order_type _order {};
    index_type _origin {};
};


// get the inline implementations
#include "IndexIterator.icc"


// end of file

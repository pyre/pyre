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
    // iterator traits for STL compatibility
    using value_type = Index<Rank>;
    using reference = const Index<Rank> &;
    using pointer = const Index<Rank> *;
    using difference_type = std::ptrdiff_t;
    using iterator_category = std::forward_iterator_tag;

    // metamethods
public:
    // singular iterator; satisfies the std::regular requirement on forward iterators
    constexpr IndexIterator() noexcept = default;
    // construct from a shape, a traversal order, and a starting index
    constexpr IndexIterator(
        const Shape<Rank> &, const Order<Rank> &, const Index<Rank> &) noexcept;

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
    Index<Rank> _current {};
    Shape<Rank> _shape {};
    Order<Rank> _order {};
    Index<Rank> _origin {};
};


// get the inline implementations
#include "IndexIterator.icc"


// end of file

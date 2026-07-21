// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// Diagonal.h includes its dependencies directly so the type aliases in the class body refer to
// complete types
#include "Shape.h"
#include "Index.h"
#include "Order.h"
#include "IndexIterator.h"


// the diagonal packing strategy
// only the {Rank} cells on the main diagonal are stored, in one contiguous run; every off
// diagonal index shares a single extra cell, so that a client reading an off diagonal entry
// finds the value that belongs there, which for a diagonal object is zero
// storing that sink cell is what lets {offset} stay total: every index in the box has a home,
// even the ones the diagonal does not distinguish
template <std::size_t Rank>
class pyre::grid::Diagonal {
    // types
public:
    // myself
    using self_type = Diagonal<Rank>;
    // parts
    using index_type = Index<Rank>;
    using shape_type = Shape<Rank>;
    using order_type = Order<Rank>;
    // scalars
    using size_type = size_t;
    using difference_type = std::ptrdiff_t;
    // iterator
    using iterator_type = IndexIterator<Rank>;

    // metamethods
public:
    // the origin must lie on the diagonal, so that shifting an index by it keeps the diagonal
    // structure intact
    // there is no packing order to choose: only the diagonal is stored, and its single run is
    // indexed by position along the diagonal, which no permutation of the axes can rearrange
    constexpr explicit Diagonal(
        const shape_type &, const index_type & = index_type::zero()) noexcept;

    // default metamethods
public:
    ~Diagonal() = default;
    Diagonal(const Diagonal &) = default;
    Diagonal(Diagonal &&) = default;
    auto operator=(const Diagonal &) noexcept -> self_type & = default;
    auto operator=(Diagonal &&) noexcept -> self_type & = default;

    // accessors
public:
    [[nodiscard]] constexpr auto shape() const noexcept -> shape_type;
    [[nodiscard]] constexpr auto origin() const noexcept -> index_type;
    [[nodiscard]] constexpr auto nudge() const noexcept -> difference_type;
    // the memory footprint: the diagonal cells plus the shared sink cell
    [[nodiscard]] constexpr auto cells() const noexcept -> difference_type;
    static consteval auto rank() noexcept -> size_type;

    // packing isomorphism
public:
    // the cell an index lands on: its own diagonal cell, or the shared sink if it is off diagonal
    [[nodiscard]] constexpr auto offset(const index_type &) const noexcept -> difference_type;
    // the diagonal index that a stored offset came from; a partial inverse, since off diagonal
    // indices were never told apart
    [[nodiscard]] constexpr auto index(difference_type) const noexcept -> index_type;
    // syntactic sugar
    [[nodiscard]] constexpr auto operator[](const index_type &) const noexcept -> difference_type;
    [[nodiscard]] constexpr auto operator[](difference_type) const noexcept -> index_type;

    // iteration: visit every index in the box, the same way {Canonical} would
    // most of those indices are off diagonal and so land on the sink, which is exactly what a
    // client walking a diagonal object to read its dense form expects
public:
    [[nodiscard]] constexpr auto begin() const noexcept -> iterator_type;
    [[nodiscard]] constexpr auto begin(const index_type &) const noexcept -> iterator_type;
    [[nodiscard]] constexpr auto end() const noexcept -> iterator_type;

    // implementation details
private:
    shape_type _shape {};
    index_type _origin {};
    // deduced: the number of cells on the diagonal, i.e. the extent along one axis
    difference_type _D {};
    // deduced: the offset correction that sends {_origin} to offset zero
    difference_type _nudge {};

    // static helpers
private:
    // the offset of the origin, which must sit on the diagonal
    static constexpr auto _initShift(const index_type &) noexcept -> difference_type;
    // whether every coordinate of an index agrees, i.e. the index is on the diagonal
    static constexpr auto _isDiagonal(const index_type &) noexcept -> bool;
};


// get the inline implementations
#include "Diagonal.icc"


// end of file

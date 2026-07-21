// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// Symmetric.h includes its dependencies directly so the type aliases in the class body refer to
// complete types
#include "Shape.h"
#include "Index.h"
#include "Order.h"
#include "IndexIterator.h"


// the symmetric packing strategy
// only one of the two triangular halves is stored; an index and any permutation of its
// coordinates name the same cell, which is exactly the value a symmetric object holds there
// this makes {offset} many-to-one rather than a sink: a client reading an entry the strategy
// does not store separately finds the stored value that, by symmetry, belongs there
// there is no packing order to choose: the coordinates are sorted before they are packed, so no
// permutation of the axes can change where an index lands
template <std::size_t Rank>
class pyre::grid::Symmetric {
    // types
public:
    // myself
    using self_type = Symmetric<Rank>;
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
    // a symmetric layout is a cube: every axis shares the extent {shape[0]}
    constexpr explicit Symmetric(
        const shape_type &, const index_type & = index_type::zero()) noexcept;

    // default metamethods
public:
    ~Symmetric() = default;
    Symmetric(const Symmetric &) = default;
    Symmetric(Symmetric &&) = default;
    auto operator=(const Symmetric &) noexcept -> self_type & = default;
    auto operator=(Symmetric &&) noexcept -> self_type & = default;

    // accessors
public:
    [[nodiscard]] constexpr auto shape() const noexcept -> shape_type;
    [[nodiscard]] constexpr auto origin() const noexcept -> index_type;
    // the memory footprint: the number of entries in one triangular half
    [[nodiscard]] constexpr auto cells() const noexcept -> difference_type;
    static consteval auto rank() noexcept -> size_type;

    // packing isomorphism
public:
    // the cell an index lands on, after its coordinates are sorted into the stored triangle
    [[nodiscard]] constexpr auto offset(const index_type &) const noexcept -> difference_type;
    // the sorted representative index that a stored offset came from; a partial inverse, since
    // the permutations of an index were never told apart
    [[nodiscard]] constexpr auto index(difference_type) const noexcept -> index_type;
    // syntactic sugar
    [[nodiscard]] constexpr auto operator[](const index_type &) const noexcept -> difference_type;
    [[nodiscard]] constexpr auto operator[](difference_type) const noexcept -> index_type;

    // iteration: visit every index in the box, the same way {Canonical} would
    // many of those indices are permutations of one another and so coincide in memory, which is
    // what a client walking a symmetric object to read its dense form expects
public:
    [[nodiscard]] constexpr auto begin() const noexcept -> iterator_type;
    [[nodiscard]] constexpr auto begin(const index_type &) const noexcept -> iterator_type;
    [[nodiscard]] constexpr auto end() const noexcept -> iterator_type;

    // implementation details
private:
    shape_type _shape {};
    index_type _origin {};
    // deduced: the extent shared by every axis, i.e. the dimension of the cube
    difference_type _D {};

    // static helpers: the combinatorics of triangular packing, all recursive on the rank {M}
private:
    // the number of entries in a symmetric packing of rank {M} and dimension {D}
    template <std::size_t M>
    static constexpr auto _entries(difference_type D) noexcept -> difference_type
        requires(M == 1);
    template <std::size_t M>
    static constexpr auto _entries(difference_type D) noexcept -> difference_type
        requires(M > 1);

    // the number of entries in all leading coordinates below {i}, at rank {M} and dimension {D}
    template <std::size_t M>
    static constexpr auto _entriesBeforeRank(difference_type i, difference_type D) noexcept
        -> difference_type;

    // the offset of the sorted, shifted coordinates {i, j...} at rank {M} and dimension {D}
    template <std::size_t M, class... S>
    static constexpr auto _offset(difference_type D, difference_type i, S... j) noexcept
        -> difference_type
        requires(sizeof...(S) == M - 1 && M > 1);
    template <std::size_t M>
    static constexpr auto _offset(difference_type D, difference_type i) noexcept -> difference_type
        requires(M == 1);

    // the leading coordinate that {offset} decomposes to, at rank {M} and dimension {D};
    // consumes the part of {offset} it accounts for
    template <std::size_t M>
    static constexpr auto _leadingCoordinate(difference_type D, difference_type & offset) noexcept
        -> difference_type
        requires(M > 1);
    template <std::size_t M>
    static constexpr auto _leadingCoordinate(difference_type D, difference_type & offset) noexcept
        -> difference_type
        requires(M == 1);
};


// get the inline implementations
#include "Symmetric.icc"


// end of file

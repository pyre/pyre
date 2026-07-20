// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// dependencies
#include "Shape.h"
#include "Index.h"
#include "Order.h"
#include "IndexIterator.h"


// the canonical packing strategy: the isomorphism
//   Z_{s0} x ... x Z_{s_{N-1}} -> Z_{s0 * ... * s_{N-1}}
// parameterized by the traversal order of the axes
template <std::size_t Rank>
class pyre::grid::Canonical {
    // types
public:
    // myself
    using self_type = Canonical<Rank>;
    // parts
    using index_type = Index<Rank>;
    using shape_type = Shape<Rank>;
    using order_type = Order<Rank>;
    // strides are non-negative axis increments; same representation as shape
    using strides_type = Shape<Rank>;
    // scalars
    using size_type = size_t;
    using difference_type = std::ptrdiff_t;
    // iterator
    using iterator_type = IndexIterator<Rank>;

    // metamethods
public:
    // primary constructor: deduce strides and nudge from shape, origin, and order
    constexpr explicit Canonical(
        const shape_type &, const index_type & = index_type::zero(),
        const order_type & = order_type::c()) noexcept;
    // full constructor: explicit layout specification, for derived layouts such as slices
    constexpr Canonical(
        const shape_type &, const index_type &, const order_type &, const strides_type &,
        difference_type) noexcept;

    // default metamethods
public:
    // destructor
    ~Canonical() = default;
    // a layout is a value: it copies and moves freely
    Canonical(const Canonical &) = default;
    Canonical(Canonical &&) = default;
    auto operator=(const Canonical &) noexcept -> self_type & = default;
    auto operator=(Canonical &&) noexcept -> self_type & = default;

    // accessors
public:
    // the extent of the index box along each axis
    [[nodiscard]] constexpr auto shape() const noexcept -> shape_type;
    // the smallest addressable index
    [[nodiscard]] constexpr auto origin() const noexcept -> index_type;
    // the permutation of the axes that says which one varies fastest in memory
    [[nodiscard]] constexpr auto order() const noexcept -> order_type;
    // the distance in memory between consecutive cells along each axis
    [[nodiscard]] constexpr auto strides() const noexcept -> strides_type;
    // the correction that places {origin} at the beginning of the memory block
    [[nodiscard]] constexpr auto nudge() const noexcept -> difference_type;
    // the number of addressable cells
    [[nodiscard]] constexpr auto cells() const noexcept -> size_type;
    // my rank, as a compile time constant
    static consteval auto rank() noexcept -> size_type;

    // mutators: return a new {Canonical} with a different traversal order
public:
    // repack my index box using the given order, deducing fresh strides and nudge
    [[nodiscard]] constexpr auto order(const order_type &) const noexcept -> self_type;

    // packing isomorphism
public:
    // the offset in memory of the cell at the given index
    [[nodiscard]] constexpr auto offset(const index_type &) const noexcept -> difference_type;
    // the inverse map: the index of the cell that lives at the given offset
    [[nodiscard]] constexpr auto index(difference_type) const noexcept -> index_type;
    // syntactic sugar
    [[nodiscard]] constexpr auto operator[](const index_type &) const noexcept -> difference_type;
    [[nodiscard]] constexpr auto operator[](difference_type) const noexcept -> index_type;

    // iteration: visit every index in the box in packing order
public:
    // a cursor at {origin} that visits every index one cell at a time
    [[nodiscard]] constexpr auto begin() const noexcept -> iterator_type;
    // a cursor at {origin} that advances by the given step along each axis
    [[nodiscard]] constexpr auto begin(const index_type &) const noexcept -> iterator_type;
    // the cursor that marks the end of the traversal
    [[nodiscard]] constexpr auto end() const noexcept -> iterator_type;

    // sub-layout: constrain to a sub-box, inheriting the physical layout
public:
    // the layout of the tile anchored at the given index with the given shape
    [[nodiscard]] constexpr auto box(index_type, shape_type) const noexcept -> self_type;

    // hyperplane extraction: fix all axes not in {FreeAxes} at {base};
    // the result shares the parent's physical memory layout
    template <std::size_t... FreeAxes>
        requires(sizeof...(FreeAxes) <= Rank && ((FreeAxes < Rank) && ...))
    [[nodiscard]] constexpr auto slice(const index_type &) const noexcept
        -> Canonical<sizeof...(FreeAxes)>;

    // implementation details
private:
    // the extent along each axis
    shape_type _shape {};
    // which axis varies fastest in memory
    order_type _order {};
    // the smallest addressable index; may be negative
    index_type _origin {};
    // deduced: the memory distance between consecutive cells along each axis
    strides_type _strides {};
    // deduced: the offset correction that sends {_origin} to offset zero
    difference_type _nudge {};
    // deduced: the offset at which my own first cell sits
    // a layout that anchors itself is at zero here, but a derived one addresses the memory of
    // the parent it came from, so its cells begin further in; {index} measures from this mark
    difference_type _anchor {};

    // static helpers
private:
    // deduce the strides implied by tight packing of {shape} in the given {order}
    static constexpr auto _initStrides(const shape_type &, const order_type &) noexcept
        -> strides_type;
    // compute the raw offset of {origin} under the given strides
    static constexpr auto _initShift(const index_type &, const strides_type &) noexcept
        -> difference_type;
};


// get the inline implementations
#include "Canonical.icc"


// end of file

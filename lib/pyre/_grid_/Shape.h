// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// support
#include "forward.h"


// the extent of a grid along each one of its axes
// this is the user facing description of how big a grid is, in the spirit of a numpy shape; it is
// a fixed rank container, so the number of axes is known at compile time
// together with {Index} and {Order} it supports {Canonical}, the packing strategy that maps an
// index to an offset in memory
template <std::size_t Rank>
class pyre::grid::Shape {
    // types
public:
    // myself
    using self_type = Shape<Rank>;
    // the type that labels my axes, and so subscripts me
    using size_type = size_t;
    // extents are signed, even though a negative one is meaningless
    // an extent takes part in the offset arithmetic that addresses cells, and mixing an unsigned
    // extent into that arithmetic converts the signed side rather than the other way round; a
    // subtraction that ought to report a negative difference would instead wrap to something
    // enormous, turning a detectable mistake into an undetectable one
    using value_type = std::ptrdiff_t;
    // and the usual family of ways to refer to one
    using pointer = value_type *;
    using const_pointer = const value_type *;
    using reference = value_type &;
    using const_reference = const value_type &;
    using rvalue_reference = value_type &&;
    using const_rvalue_reference = const value_type &&;
    // the extents live in a fixed size array, one slot per axis
    using storage_type = std::array<value_type, Rank>;
    // and i hand out the iterators of my backing array
    using iterator = typename storage_type::iterator;
    using const_iterator = typename storage_type::const_iterator;
    using reverse_iterator = typename storage_type::reverse_iterator;
    using const_reverse_iterator = typename storage_type::const_reverse_iterator;

    // metamethods
public:
    // default constructor: all zeroes that can be programmatically set
    constexpr Shape() noexcept;
    // construct from a backing array
    explicit constexpr Shape(storage_type) noexcept;
    // construct from exactly {Rank} extents
    template <std::integral... Ts>
        requires(sizeof...(Ts) == Rank)
    explicit constexpr Shape(Ts...) noexcept;
    // construct from an initializer list
    constexpr Shape(std::initializer_list<value_type> ilist) noexcept;

    // default metamethods
public:
    // destructor
    ~Shape() = default;
    // copy/move
    Shape(const Shape &) noexcept = default;
    Shape(Shape &&) noexcept = default;
    auto operator=(const Shape &) noexcept -> Shape & = default;
    auto operator=(Shape &&) noexcept -> Shape & = default;

    // accessors
public:
    // my rank as a compile time constant
    static consteval auto rank() noexcept -> size_type;

    // element access
    constexpr auto operator[](size_type idx) noexcept -> reference;
    constexpr auto operator[](size_type idx) const noexcept -> const_reference;

    // bounds-checked element access; throws {std::out_of_range}
    constexpr auto at(size_type idx) -> reference;
    constexpr auto at(size_type idx) const -> const_reference;

    // access to the underlying storage
    constexpr auto data() noexcept -> pointer;
    constexpr auto data() const noexcept -> const_pointer;

    // factories
public:
    // a shape with all extents zeroed out
    static constexpr auto zero() noexcept -> self_type;
    // a shape with all extents set to one
    static constexpr auto one() noexcept -> self_type;
    // a shape with all extents set to a given value
    static constexpr auto fill(value_type) noexcept -> self_type;

    // interface
public:
    // the total number of addressable values
    constexpr auto cells() const noexcept -> size_type;

    // the smallest and largest extent
    [[nodiscard]] constexpr auto min() const noexcept -> value_type;
    [[nodiscard]] constexpr auto max() const noexcept -> value_type;

    // iteration support
    // visit the extents from the leading axis to the trailing one
public:
    constexpr auto begin() noexcept -> iterator;
    constexpr auto end() noexcept -> iterator;
    constexpr auto begin() const noexcept -> const_iterator;
    constexpr auto end() const noexcept -> const_iterator;
    constexpr auto cbegin() const noexcept -> const_iterator;
    constexpr auto cend() const noexcept -> const_iterator;

    // reverse iteration support
    // visit the extents from the trailing axis back to the leading one
public:
    constexpr auto rbegin() noexcept -> reverse_iterator;
    constexpr auto rend() noexcept -> reverse_iterator;
    constexpr auto rbegin() const noexcept -> const_reverse_iterator;
    constexpr auto rend() const noexcept -> const_reverse_iterator;
    constexpr auto crbegin() const noexcept -> const_reverse_iterator;
    constexpr auto crend() const noexcept -> const_reverse_iterator;

    // implementation details - data
private:
    // one extent per axis, zeroed out unless someone says otherwise
    storage_type _extents {};
};


// get the inline implementations
#include "Shape.icc"


// end of file

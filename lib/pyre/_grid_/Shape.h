// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved

// code guard
#pragma once


// support
#include "forward.h"


// storage for the index packing shape
template <std::size_t Rank>
class pyre::grid::Shape {
    // types
public:
    // myself
    using self_type = Shape<Rank>;
    // basic
    using size_type = size_t;
    // cell type and access
    using value_type = size_t;
    using pointer = value_type *;
    using const_pointer = const value_type *;
    using reference = value_type &;
    using const_reference = const value_type &;
    // storage
    using storage_type = std::array<value_type, Rank>;
    // iterators
    using iterator = typename storage_type::iterator;
    using const_iterator = typename storage_type::const_iterator;

    // metamethods
public:
    // default constructor: all zeroes that can be programmatically set
    constexpr Shape() noexcept;
    // construct from a backing array
    explicit constexpr Shape(storage_type) noexcept;
    // construct from exactly {Rank} non-negative values
    template <std::unsigned_integral... Ts>
        requires(sizeof...(Ts) == Rank)
    explicit constexpr Shape(Ts...) noexcept;
    // construct from an initializer list
    explicit constexpr Shape(std::initializer_list<value_type> ilist) noexcept;

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

    // access to the underlying storage
    constexpr auto data() noexcept -> pointer;
    constexpr auto data() const noexcept -> const_pointer;

    // interface
public:
    // the total number of addressable values
    constexpr auto cells() const noexcept -> size_type;

    // iteration support
public:
    constexpr auto begin() noexcept -> iterator;
    constexpr auto end() noexcept -> iterator;
    constexpr auto begin() const noexcept -> const_iterator;
    constexpr auto end() const noexcept -> const_iterator;
    constexpr auto cbegin() const noexcept -> const_iterator;
    constexpr auto cend() const noexcept -> const_iterator;

    // implementation details - data
private:
    storage_type _extents {};
};


// get the inline implementations
#include "Shape.icc"


// end of file

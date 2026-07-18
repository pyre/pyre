// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// support
#include "forward.h"


// the packing order of the axes of a grid: a permutation of the axis labels {0 .. Rank-1} in
// which every label occurs exactly once; slot {axis} holds the packing level of that axis, and
// smaller levels mark the faster varying axes
template <std::size_t Rank>
class pyre::grid::Order {
    // types
public:
    // myself
    using self_type = Order<Rank>;
    // basic
    using size_type = size_t;
    // packing levels are non-negative, hence the unsigned cell type
    using value_type = size_t;
    using pointer = value_type *;
    using const_pointer = const value_type *;
    using reference = value_type &;
    using const_reference = const value_type &;
    using rvalue_reference = value_type &&;
    using const_rvalue_reference = const value_type &&;
    // the permutation lives in a fixed size array, one slot per axis
    using storage_type = std::array<value_type, Rank>;
    // iterators
    using iterator = typename storage_type::iterator;
    using const_iterator = typename storage_type::const_iterator;
    using reverse_iterator = typename storage_type::reverse_iterator;
    using const_reverse_iterator = typename storage_type::const_reverse_iterator;

    // metamethods
public:
    // absent other instructions, pack the c way: {R-1, ..., 1, 0}
    constexpr Order() noexcept;
    // adopt a permutation that has already been assembled
    explicit constexpr Order(storage_type) noexcept;
    // spell out the packing level of each axis, exactly {Rank} of them
    template <std::unsigned_integral... Ts>
        requires(sizeof...(Ts) == Rank)
    explicit constexpr Order(Ts...) noexcept;
    // spell out the packing levels in braces, e.g. {2, 0, 1}
    constexpr Order(std::initializer_list<value_type> ilist) noexcept;

    // default metamethods
public:
    // destructor
    ~Order() = default;
    // copy/move
    Order(const Order &) noexcept = default;
    Order(Order &&) noexcept = default;
    auto operator=(const Order &) noexcept -> Order & = default;
    auto operator=(Order &&) noexcept -> Order & = default;

    // accessors
public:
    // the number of axes i order, known at compile time
    static consteval auto rank() noexcept -> size_type;

    // the packing level of a given axis, unchecked
    constexpr auto operator[](size_type idx) noexcept -> reference;
    constexpr auto operator[](size_type idx) const noexcept -> const_reference;

    // the packing level of a given axis, with a guard against bad axis labels;
    // throws {std::out_of_range}
    constexpr auto at(size_type idx) -> reference;
    constexpr auto at(size_type idx) const -> const_reference;

    // hand out the raw permutation, e.g. for interoperating with legacy interfaces
    constexpr auto data() noexcept -> pointer;
    constexpr auto data() const noexcept -> const_pointer;

    // utilities
public:
    // the two conventional packing orders, each under both of its names
    static constexpr auto c() noexcept -> self_type;
    static constexpr auto fortran() noexcept -> self_type;
    static constexpr auto rowMajor() noexcept -> self_type;
    static constexpr auto columnMajor() noexcept -> self_type;

    // verify my class invariant: that i am a genuine permutation in S_{Rank}
    [[nodiscard]] constexpr auto isPermutation() const noexcept -> bool;

    // visit the axes in their natural sequence, from the first to the last
public:
    constexpr auto begin() noexcept -> iterator;
    constexpr auto end() noexcept -> iterator;
    constexpr auto begin() const noexcept -> const_iterator;
    constexpr auto end() const noexcept -> const_iterator;
    constexpr auto cbegin() const noexcept -> const_iterator;
    constexpr auto cend() const noexcept -> const_iterator;

    // visit the axes back to front, from the last to the first
public:
    constexpr auto rbegin() noexcept -> reverse_iterator;
    constexpr auto rend() noexcept -> reverse_iterator;
    constexpr auto rbegin() const noexcept -> const_reverse_iterator;
    constexpr auto rend() const noexcept -> const_reverse_iterator;
    constexpr auto crbegin() const noexcept -> const_reverse_iterator;
    constexpr auto crend() const noexcept -> const_reverse_iterator;

    // implementation details - data
private:
    // the packing level of each axis
    storage_type _permutation {};

    // implementation details - compile-time factories
private:
    // build {Rank-1, ..., 1, 0}, so the last axis is the fastest varying one
    template <std::size_t... Is>
    static consteval auto _make_row_major(std::index_sequence<Is...>) noexcept -> storage_type;
    // build {0, 1, ..., Rank-1}, so the first axis is the fastest varying one
    template <std::size_t... Is>
    static consteval auto _make_column_major(std::index_sequence<Is...>) noexcept -> storage_type;
};


// get the inline implementations
#include "Order.icc"


// end of file

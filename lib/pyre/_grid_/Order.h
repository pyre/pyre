// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved

// code guard
#pragma once


// support
#include "forward.h"


// storage for the index packing order
template <std::size_t Rank>
class pyre::grid::Order {
    // types
public:
    // myself
    using self_type = Order<Rank>;
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
    // default constructor: c-style: {R-1, ..., 1, 0}
    constexpr Order() noexcept;
    // construct from a backing array
    explicit constexpr Order(storage_type) noexcept;
    // construct from exactly {Rank} non-negative values
    template <std::unsigned_integral... Ts>
        requires(sizeof...(Ts) == Rank)
    explicit constexpr Order(Ts...) noexcept;
    // construct from an initializer list
    explicit constexpr Order(std::initializer_list<value_type> ilist) noexcept;

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
    // my rank as a compile time constant
    static consteval auto rank() noexcept -> size_type;

    // element access
    constexpr auto operator[](size_type idx) noexcept -> reference;
    constexpr auto operator[](size_type idx) const noexcept -> const_reference;

    // access to the underlying storage
    constexpr auto data() noexcept -> pointer;
    constexpr auto data() const noexcept -> const_pointer;

    // utilities
public:
    // convenience factories
    static constexpr auto c() noexcept -> self_type;
    static constexpr auto fortran() noexcept -> self_type;
    static constexpr auto rowMajor() noexcept -> self_type;
    static constexpr auto columnMajor() noexcept -> self_type;

    // check whether i am a permutation in S_{Rank}
    [[nodiscard]] constexpr auto isPermutation() const noexcept -> bool;

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
    storage_type _permutation {};

    // implementation details - compile-time factories
private:
    // row major
    template <std::size_t... Is>
    static consteval auto _make_row_major(std::index_sequence<Is...>) noexcept -> storage_type;
    // column major
    template <std::size_t... Is>
    static consteval auto _make_column_major(std::index_sequence<Is...>) noexcept -> storage_type;
};


// get the inline implementations
#include "Order.icc"


// end of file

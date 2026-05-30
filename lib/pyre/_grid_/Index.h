// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// support
#include "forward.h"


// storage for a multidimensional index
// resist the temptation to use unsigned types; they complicate index arithmetic unnecessarily
template <std::size_t Rank>
class pyre::grid::Index {
    // types
public:
    // myself
    using self_type = Index<Rank>;
    // basic
    using size_type = size_t;
    // cell type and access
    using value_type = std::ptrdiff_t;
    using pointer = value_type *;
    using const_pointer = const value_type *;
    using reference = value_type &;
    using const_reference = const value_type &;
    using rvalue_reference = value_type &&;
    using const_rvalue_reference = const value_type &&;
    // storage
    using storage_type = std::array<value_type, Rank>;
    // iterators
    using iterator = typename storage_type::iterator;
    using const_iterator = typename storage_type::const_iterator;
    using reverse_iterator = typename storage_type::reverse_iterator;
    using const_reverse_iterator = typename storage_type::const_reverse_iterator;

    // metamethods
public:
    // default constructor: all zeroes
    constexpr Index() noexcept;
    // construct from a backing array
    explicit constexpr Index(storage_type) noexcept;
    // construct from exactly {Rank} signed integer values
    template <std::signed_integral... Ts>
        requires(sizeof...(Ts) == Rank)
    explicit constexpr Index(Ts...) noexcept;
    // construct from an initializer list
    explicit constexpr Index(std::initializer_list<value_type>) noexcept;

    // default metamethods
public:
    // destructor
    ~Index() = default;
    // copy/move
    Index(const Index &) noexcept = default;
    Index(Index &&) noexcept = default;
    auto operator=(const Index &) noexcept -> Index & = default;
    auto operator=(Index &&) noexcept -> Index & = default;

    // accessors
public:
    // my rank as a compile time constant
    static consteval auto rank() noexcept -> size_type;

    // element access
    constexpr auto operator[](size_type) noexcept -> reference;
    constexpr auto operator[](size_type) const noexcept -> const_reference;

    // bounds-checked element access; throws {std::out_of_range}
    constexpr auto at(size_type) -> reference;
    constexpr auto at(size_type) const -> const_reference;

    // access to the underlying storage
    constexpr auto data() noexcept -> pointer;
    constexpr auto data() const noexcept -> const_pointer;

    // interface
public:
    // the smallest and largest coordinate
    [[nodiscard]] constexpr auto min() const noexcept -> value_type;
    [[nodiscard]] constexpr auto max() const noexcept -> value_type;

    // factories
public:
    // an index with all coordinates zeroed out
    static constexpr auto zero() noexcept -> self_type;
    // an index with all coordinates set to one
    static constexpr auto one() noexcept -> self_type;
    // an index with all coordinates set to a given value
    static constexpr auto fill(value_type) noexcept -> self_type;

    // iteration support
public:
    constexpr auto begin() noexcept -> iterator;
    constexpr auto end() noexcept -> iterator;
    constexpr auto begin() const noexcept -> const_iterator;
    constexpr auto end() const noexcept -> const_iterator;
    constexpr auto cbegin() const noexcept -> const_iterator;
    constexpr auto cend() const noexcept -> const_iterator;

    // reverse iteration support
public:
    constexpr auto rbegin() noexcept -> reverse_iterator;
    constexpr auto rend() noexcept -> reverse_iterator;
    constexpr auto rbegin() const noexcept -> const_reverse_iterator;
    constexpr auto rend() const noexcept -> const_reverse_iterator;
    constexpr auto crbegin() const noexcept -> const_reverse_iterator;
    constexpr auto crend() const noexcept -> const_reverse_iterator;

    // implementation details
private:
    storage_type _coords {};
};


// get the inline implementations
#include "Index.icc"


// end of file

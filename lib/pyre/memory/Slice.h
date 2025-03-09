// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved

// code guard
#pragma once


// externals
#include "externals.h"
// forward declarations
#include "forward.h"

template <class memT>
class pyre::memory::Slice {
    // types
public:
    using storage_type = memT;
    using self_type = Slice<storage_type>;
    using index_type = int;

    // iterator requirements
    using iterator_category = std::forward_iterator_tag;
    using value_type = typename storage_type::reference;
    using difference_type = void;
    using pointer = typename storage_type::pointer;
    using reference = typename storage_type::reference;

    // metamethods
public:
    // constructors
    constexpr Slice(const storage_type & storage, index_type start = 0);

    // accessors
public:
    constexpr auto storage() const -> const storage_type &;
    constexpr auto index() const -> index_type;

    // iterator protocol
public:
    // dereference
    constexpr auto operator*() const -> typename storage_type::reference;
    // arithmetic
    constexpr auto operator++() -> self_type &;
    constexpr auto operator++(int) -> self_type;

    // implementation details - data
private:
    // the buffer we are iterating over
    const storage_type & _storage;
    // the current value
    index_type _index;

    // default metamethods
public:
    // destructor
    ~Slice() = default;
    // constructors
    Slice(const Slice &) = default;
    Slice(Slice &&) = default;
    Slice & operator=(const Slice &) = default;
    Slice & operator=(Slice &&) = default;
};

// definitions
#include "Slice.icc"


// end of file

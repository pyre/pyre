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

// base class
#include "Buffer.h"
// non-trivial iterator
#include "Slice.h"


// a block of cells whose memory belongs to someone else
template <class T, bool isConst>
class pyre::memory::View : public Buffer<T, isConst> {
    // types
public:
    // me
    using self_type = View<T, isConst>;
    // my base class
    using super_type = Buffer<T, isConst>;
    // my iterator
    using slice_type = Slice<self_type>;

    // my cell
    using typename super_type::cell_type;
    // pull the type aliases
    using typename super_type::value_type;
    // derived types
    using typename super_type::pointer;
    using typename super_type::const_pointer;
    using typename super_type::reference;
    using typename super_type::const_reference;
    // distances
    using typename super_type::difference_type;
    // sizes of things
    using typename super_type::size_type;
    using typename super_type::cell_count_type;
    // strings
    using typename super_type::uri_type;
    using typename super_type::string_type;

    // metamethods
public:
    // map an existing data product
    inline View(pointer data, cell_count_type cells, cell_count_type stride = 1);

    // interface
public:
    // human readable form of my location
    inline auto uri() const -> uri_type;
    // the number of cells
    inline auto cells() const -> cell_count_type;
    // the memory footprint of the block
    inline auto bytes() const -> size_type;
    // access to the raw data pointer
    inline auto data() const -> pointer;
    // access to the raw data pointer in a form suitable for diagnostics
    inline auto where() const -> const void *;

    // expose my constness
    static constexpr auto readonly() -> bool;
    static constexpr auto writable() -> bool;

    // simulate my c++ declaration
    static inline auto declSelf() -> string_type;
    // simulate the c++ declaration of my template parameter
    static inline auto declValue() -> string_type;
    // human readable name for my type
    static inline auto className() -> string_type;

    // iterator support
public:
    inline auto begin() const -> slice_type;
    inline auto end() const -> slice_type;

    // data access
public:
    // with bounds checking
    inline auto at(size_type) const -> reference;
    // without bounds checking
    inline auto operator[](size_type) const -> reference;

    // interface
public:
    inline auto fill(const value_type value) const -> const self_type &;

    // implementation details: data
private:
    const pointer _data;
    const cell_count_type _cells;
    const cell_count_type _stride;

    // default metamethods
public:
    // destructor
    ~View() = default;
    // constructors
    View(const View &) = default;
    View(View &&) = default;
    View & operator=(const View &) = default;
    View & operator=(View &&) = default;
};


// inline definitions
#include "View.icc"


// end of file

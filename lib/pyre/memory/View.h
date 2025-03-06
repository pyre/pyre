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


// a block of cells whose memory belongs to someone else
template <class T, bool isConst>
class pyre::memory::View : public Buffer<T, isConst> {
    // types
public:
    // me
    using self_type = View<T, isConst>;
    // my base class
    using super_type = Buffer<T, isConst>;

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
    inline View(pointer, cell_count_type);

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
    // human readable rendering of my expansion
    static inline auto name() -> string_type;
    // human readable rendering of my storage strategy
    static inline auto strategyName() -> string_type;
    // human readable rendering of my {cell_type}
    static inline auto cellName() -> string_type;
    // my {cell_type} decl
    static inline auto cellDecl() -> string_type;

    // iterator support
public:
    inline auto begin() const -> pointer;
    inline auto end() const -> pointer;

    // data access
public:
    // with bounds checking
    inline auto at(size_type) const -> reference;
    // without bounds checking
    inline auto operator[](size_type) const -> reference;

    // implementation details: data
private:
    const pointer _data;
    const cell_count_type _cells;

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

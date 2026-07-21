// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// externals
#include "externals.h"
// forward declarations
#include "forward.h"

// base class
#include "Buffer.h"


// a file-backed block of cells
template <class T, bool isConst>
class pyre::memory::Map : public Buffer<T, isConst> {
    // types
public:
    // me
    using self_type = Map<T, isConst>;
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
    // my handle
    using handle_type = std::shared_ptr<FileMap>;
    // strings
    using typename super_type::uri_type;
    using typename super_type::string_type;

    // permissions
    using writable_type = FileMap::writable_type;
    // my handle

    // metamethods
public:
    // map an existing data product; the second argument is a read/write flag
    inline explicit Map(uri_type, writable_type = false);
    // create a new one, given a path and a number of cells
    // the count is taken as any integer type and constrained to be one, so that it never
    // collides with the {writable_type} flag of the mapping constructor above: an integer
    // argument always sizes a new file, and only a {bool} opens an existing one
    template <std::integral countT>
    inline Map(uri_type, countT);

    // interface
public:
    // access to the name of the supporting file
    inline auto uri() const -> uri_type;
    // the number of cells; the inherited {bytes} tells you the memory footprint of the block
    inline auto cells() const -> cell_count_type;
    // the memory footprint of the block
    inline auto bytes() const -> size_type;
    // access to the raw data pointer
    inline auto data() const -> pointer;
    // access to the raw data pointer in a form suitable for including in diagnostics
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
    inline auto begin() const -> pointer;
    inline auto end() const -> pointer;

    // data access
public:
    // with bounds checking
    inline auto at(difference_type) const -> reference;
    // without bounds checking
    inline auto operator[](difference_type) const -> reference;

    // interface
public:
    inline auto fill(const value_type value) const -> const self_type &;

    // implementation details: data
private:
    handle_type _map;

    // default metamethods
public:
    // destructor
    ~Map() = default;
    // constructors
    Map(const Map &) = default;
    Map(Map &&) = default;
    Map & operator=(const Map &) = default;
    Map & operator=(Map &&) = default;
};


// inline definitions
#include "Map.icc"


// end of file

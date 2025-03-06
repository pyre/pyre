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
    // map an existing data product
    inline explicit Map(uri_type, writable_type = false);
    // create a new one, given a path and a number of cells
    inline Map(uri_type, size_type);

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

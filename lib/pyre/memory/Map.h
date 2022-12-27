// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_memory_Map_h)
#define pyre_memory_Map_h


// a file-backed block of cells
template <class T, bool isConst>
class pyre::memory::Map {
    // types
public:
    // my cell
    using cell_type = cell_t<T, isConst>;
    // pull the type aliases
    using value_type = typename cell_type::value_type;
    // derived types
    using pointer = typename cell_type::pointer;
    using const_pointer = typename cell_type::const_pointer;
    using reference = typename cell_type::reference;
    using const_reference = typename cell_type::const_reference;
    // distances
    using difference_type = typename cell_type::difference_type;
    // sizes of things
    using size_type = typename cell_type::size_type;
    using cell_count_type = typename cell_type::cell_count_type;

    // file paths
    using uri_type = FileMap::uri_type;
    // permissions
    using writable_type = FileMap::writable_type;
    // my handle
    using handle_type = std::shared_ptr<FileMap>;

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


// get the inline definitions
#define pyre_memory_Map_icc
#include "Map.icc"
#undef pyre_memory_Map_icc


#endif

// end of file

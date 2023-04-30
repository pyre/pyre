// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_memory_FileMap_h)
#define pyre_memory_FileMap_h


// a file-backed memory map
class pyre::memory::FileMap {
    // types
public:
    // the address of the mapping
    using pointer = void *;
    // file paths
    using uri_type = uri_t;
    // file information
    using info_type = info_t;
    // sizes of things
    using size_type = size_t;
    // flags
    using writable_type = bool;

    // metamethods
public:
    // destructor
    inline ~FileMap();

    // constructors
    // map an existing data product given its filename
    inline explicit FileMap(uri_type, writable_type = false);
    // create a new product of a given size in bytes
    inline FileMap(uri_type, size_type);

    // interface
public:
    // accessors
    inline auto uri() const -> uri_type;
    inline auto writable() const -> bool;
    // memory footprint
    inline auto bytes() const -> size_type;
    // raw access to the memory block
    inline auto data() const -> pointer;

    // syntactic sugar
    inline operator pointer () const;

    // implementation details: methods
private:
    void stat();
    void create();
    void map();
    void unmap();

    // implementation details: data
private:
    // client supplied
    uri_type _uri;            // the path to my backing store
    writable_type _writable;  // access control
    // bookkeeping
    pointer _data;            // the address of the memory block
    size_type _bytes;         // the memory footprint of the block
    info_type _info;          // information about the backing store; retrieved by {::stat}

    // disallow
private:
    FileMap(const FileMap &) = delete;
    FileMap(FileMap &&) = delete;
    FileMap & operator= (const FileMap &) = delete;
    FileMap & operator= (FileMap &&) = delete;
};


// get the inline definitions
#define pyre_memory_FileMap_icc
#include "FileMap.icc"
#undef pyre_memory_FileMap_icc


#endif

// end of file

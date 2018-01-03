// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2018 all rights reserved
//

// code guard
#if !defined(pyre_memory_MemoryMap_h)
#define pyre_memory_MemoryMap_h


// declaration
// this class is a wrapper around the os calls
class pyre::memory::MemoryMap {
    // types
public:
    typedef pyre::memory::uri_t uri_type;
    typedef pyre::memory::info_t info_type;
    typedef pyre::memory::size_t size_type;
    typedef pyre::memory::offset_t offset_type;

    // constants
public:
    constexpr static int entireFile = 0;

    // meta-methods
public:
    MemoryMap(uri_type name="", size_type size=0, bool preserve=false);

    // interface
public:
    inline auto uri() const;
    inline const auto & info() const;

    // implementation details - data
private:
    uri_type _uri;
    info_type _info;


    // class methods
public:
    static void create(uri_type name, size_type size);
    static void * map(uri_type name, size_type & size, size_type offset, bool writable);
    static void unmap(const void * buffer, size_type size);
};

#endif

// end of file

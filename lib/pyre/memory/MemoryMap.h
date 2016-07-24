// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2016 all rights reserved
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
    typedef pyre::memory::size_t size_type;
    typedef pyre::memory::offset_t offset_type;

    // constants
public:
    static const size_t entireFile = 0;

    // class methods
public:
    static void create(uri_type name, size_type size);
    static void * map(uri_type name, size_type & size, offset_type offset, bool writable);
    static void unmap(const void * buffer, size_type size);
};

#endif

// end of file

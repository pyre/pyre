// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2016 all rights reserved
//

// code guard
#if !defined(pyre_grid_MemoryMap_h)
#define pyre_grid_MemoryMap_h


// declaration
// this class is a wrapper around the os calls
class pyre::grid::MemoryMap {
    // types
public:
    typedef pyre::grid::uri_t uri_type;
    typedef pyre::grid::size_t size_type;
    typedef pyre::grid::offset_t offset_type;

    // constants
public:
    static const size_t entireFile = 0;

    // class methods
public:
    static void create(uri_t name, size_t size);
    static void * map(uri_t name, size_t & size, offset_t offset, bool writable);
    static void unmap(const void * buffer, size_t size);
};

#endif

// end of file

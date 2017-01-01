// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2017 all rights reserved
//

// code guard
#if !defined(pyre_memory_Direct_h)
#define pyre_memory_Direct_h

//
// Direct is the life cycle manager of a memory mapping
//
// It is a low level concept and should be considered an implementation detail; as such, you
// should probably avoid using it directly
//

// declaration
class pyre::memory::Direct : public pyre::memory::MemoryMap {
    // meta-methods
public:
    // default constructor
    inline Direct();
    // constructor
    inline
    Direct(uri_type uri,         // the name of the file
           size_type size,       // how much of the file to map
           size_type offset = 0  // starting at this offset from the beginning
           );

    // move semantics
    inline Direct(Direct && other);
    inline Direct & operator=(Direct && other);

    // destructor
    inline ~Direct();

    // interface
public:
    // accessors
    inline auto size() const;
    inline auto buffer() const;

    // implementation details: data
private:
    void * _buffer;
    size_type _size;

    // disable the copy semantics
private:
    Direct(const Direct &) = delete;
    Direct & operator=(const Direct &) = delete;
};


#endif

// end of file

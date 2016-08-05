// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2016 all rights reserved
//

// code guard
#if !defined(pyre_memory_ConstDirect_h)
#define pyre_memory_ConstDirect_h

//
// ConstDirect is the life cycle manager of a memory mapping
//
// It is a low level concept and should be considered an implementation detail; as such, you
// should probably avoid using it directly
//

// declaration
class pyre::memory::ConstDirect : public pyre::memory::MemoryMap {
    // meta-methods
public:
    // default constructor
    inline ConstDirect();
    // constructor
    inline
    ConstDirect(uri_type uri,         // the name of the file
           size_type size,       // how much of the file to map
           size_type offset = 0  // starting at this offset from the beginning
           );

    // move semantics
    inline ConstDirect(ConstDirect && other);
    inline ConstDirect & operator=(ConstDirect && other);

    // destructor
    inline ~ConstDirect();

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
    ConstDirect(const ConstDirect &) = delete;
    ConstDirect & operator=(const ConstDirect &) = delete;
};


#endif

// end of file

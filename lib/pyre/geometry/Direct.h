// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2016 all rights reserved
//

// code guard
#if !defined(pyre_geometry_Direct_h)
#define pyre_geometry_Direct_h

//
// Direct is the life cycle manager of a memory mapping
//
// It is a low level concept and should be considered an implementation detail; as such, you
// should probably avoid using it directly
//

// declaration
class pyre::geometry::Direct : public pyre::geometry::MemoryMap {
    // meta-methods
public:
    // constructor
    explicit inline
    Direct(uri_type name,               // the name of the file
           size_type size = entireFile, // how much of the file to map
           offset_type offset = 0,      // starting at this offset from the beginning
           bool writable = false);      // type of access to grant

    // move semantics
    constexpr Direct(Direct &&) = default;
    Direct & operator=(Direct &&) = default;

    // destructor
    inline ~Direct();

    // interface
public:
    // accessors
    inline size_type size() const;
    inline void * buffer() const;

    // implementation details: data
private:
    void * const _buffer;  // the buffer payload may be writable; the pointer itself is not
    const size_type _size; // need this during destruction

    // disable copy semantics
private:
    Direct(const Direct &) = delete;
    Direct & operator=(const Direct &) = delete;
};


#endif

// end of file

// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2018 all rights reserved
//

// code guard
#if !defined(pyre_memory_ConstView_h)
#define pyre_memory_ConstView_h

//
// ConstView converts memory owned by some other object into a storage strategy
//
// It is a low level concept and should be considered an implementation detail; as such, you
// should probably avoid using it directly
//

// declaration
class pyre::memory::ConstView {
    // meta-methods
public:
    // constructor
    inline ConstView(const void * buffer);

    // copy semantics
    inline ConstView(const ConstView & other);
    inline ConstView & operator=(const ConstView & other);

    // move semantics
    inline ConstView(const ConstView &&);
    inline ConstView & operator=(const ConstView &&);

    // destructor
    inline ~ConstView();

    // interface
public:
    // accessor
    inline auto buffer() const;

    // implementation details: data
private:
    const void * _buffer;
};


#endif

// end of file

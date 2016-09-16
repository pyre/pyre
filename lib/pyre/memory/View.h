// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2016 all rights reserved
//

// code guard
#if !defined(pyre_memory_View_h)
#define pyre_memory_View_h

//
// View converts memory owned by some other object into a storage strategy
//
// It is a low level concept and should be considered an implementation detail; as such, you
// should probably avoid using it directly
//

// declaration
class pyre::memory::View {
    // meta-methods
public:
    // constructor
    inline View(void * buffer = 0);

    // copy semantics
    inline View(const View & other);
    inline View & operator=(const View & other);

    // move semantics
    inline View(const View &&);
    inline View & operator=(const View &&);

    // destructor
    inline ~View();

    // interface
public:
    // accessor
    inline auto buffer() const;

    // implementation details: data
private:
    void * _buffer;
};


#endif

// end of file

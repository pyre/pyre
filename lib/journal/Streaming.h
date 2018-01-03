// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2018 all rights reserved
//

// code guard
#if !defined(pyre_journal_Streaming_h)
#define pyre_journal_Streaming_h

// place Streaming in namespace pyre::journal
namespace pyre {
    namespace journal {
        class Streaming;
    }
}


// declaration
class pyre::journal::Streaming : public pyre::journal::Device {
    // types
public:
    typedef std::ostream stream_t;

    // meta methods
public:
    virtual ~Streaming();
    inline Streaming(stream_t &);
private:
    // disallow
    inline Streaming(const Streaming &);
    inline const Streaming & operator=(const Streaming &);

    // data members
private:
    stream_t & _stream;
};


// get the inline definitions
#define pyre_journal_Streaming_icc
#include "Streaming.icc"
#undef pyre_journal_Streaming_icc


# endif
// end of file

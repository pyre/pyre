// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2018 all rights reserved
//

// code guard
#if !defined(pyre_journal_Console_h)
#define pyre_journal_Console_h

// place Console in namespace pyre::journal
namespace pyre {
    namespace journal {
        class Console;
    }
}


// declaration
class pyre::journal::Console : public pyre::journal::Streaming {
    // types
public:
    typedef Renderer renderer_t;

    // interface
public:
    virtual void record(entry_t &, metadata_t &);

    // meta methods
public:
    virtual ~Console();
    Console();
private:
    // disallow
    Console(const Console &);
    const Console & operator=(const Console &);

    // data
private:
    renderer_t * _renderer;
};


# endif
// end of file

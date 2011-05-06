// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
// 

// code guard
#if !defined(pyre_journal_Renderer_h)
#define pyre_journal_Renderer_h

// place Renderer in namespace pyre::journal
namespace pyre {
    namespace journal {
        class Renderer;
    }
}

// declaration
class pyre::journal::Renderer {
    // types
public:
    typedef std::string string_t;
    typedef std::vector<string_t> entry_t;
    typedef std::map<string_t, string_t> metadata_t;

    // interface
public:
    virtual string_t render(const entry_t &, const metadata_t &) = 0;

    // meta methods
public:
    virtual ~Renderer();
    inline Renderer();
    // disallow
private:
    Renderer(const Renderer &);
    const Renderer & operator=(const Renderer &);

    // implementation details
protected:
    virtual string_t header(const entry_t &, const metadata_t &) = 0;
    virtual string_t body(const entry_t &, const metadata_t &) = 0;
    virtual string_t footer(const entry_t &, const metadata_t &) = 0;

    // meta methods
};


// get the inline definitions
#define pyre_journal_Renderer_icc
#include "Renderer.icc"
#undef pyre_journal_Renderer_icc


# endif
// end of file

// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2018 all rights reserved
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
    typedef std::stringstream stream_t;
    typedef std::vector<string_t> entry_t;
    typedef std::map<string_t, string_t> metadata_t;

    // interface
public:
    virtual string_t render(entry_t &, metadata_t &);

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
    virtual void header(stream_t &, entry_t &, metadata_t &);
    virtual void body(stream_t &, entry_t &, metadata_t &);
    virtual void footer(stream_t &, entry_t &, metadata_t &);
};


// get the inline definitions
#define pyre_journal_Renderer_icc
#include "Renderer.icc"
#undef pyre_journal_Renderer_icc


# endif
// end of file

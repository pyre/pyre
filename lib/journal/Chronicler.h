// -*- C++ -*-
// 
// michael a.g. aïvázis
// california institute of technology
// (c) 1998-2011 all rights reserved
// 

// code guard
#if !defined(pyre_journal_Chronicler_h)
#define pyre_journal_Chronicler_h

// place Chronicler in namespace pyre::journal
namespace pyre {
    namespace journal {
        class Chronicler;
    }
}

// This class is the main resting place for the various journal parts
//
// It maintains an index with the activation state of journal channels. This index is primed at
// construction time with settings from the environment variable {DEBUG_OPT}. Diagnostics
// access the index at construction time to discover whether they are enabled, and therefore
// allowed to generate output

// declaration
class pyre::journal::Chronicler {
    // types
protected:
    class journal_t {
        // types
    public:
        typedef Device device_t;
        typedef Renderer renderer_t;
        // interface
    public:
        inline device_t & device() const;
        inline journal_t & device(device_t *);

        inline renderer_t & renderer() const;
        inline journal_t & renderer(renderer_t *);
        // meta methods
    public:
        inline ~journal_t();
        inline journal_t(device_t *, renderer_t *);
        // disallow
    private:
        journal_t(const journal_t &);
        journal_t & operator=(const journal_t &);

        // data
    private:
        device_t * _device;
        renderer_t * _renderer;
    };

    // interface
protected:
    static journal_t & journal();

    // meta methods
protected:
    inline ~Chronicler();
    inline Chronicler();
    // disallow
private:
    inline Chronicler(const Chronicler &);
    inline const Chronicler & operator=(const Chronicler &);
};


// get the inline definitions
#define pyre_journal_Chronicler_icc
#include "Chronicler.icc"
#undef pyre_journal_Chronicler_icc


# endif
// end of file

// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// code guard
#if !defined(pyre_journal_ErrorConsole_h)
#define pyre_journal_ErrorConsole_h

// a device that prints to {cerr}
class pyre::journal::ErrorConsole : public Stream {
    // types
public:
    // pointers to me
    using pointer_type = std::shared_ptr<ErrorConsole>;

    // metamethods
public:
    // constructor
    ErrorConsole();
    // destructor
    virtual ~ErrorConsole();

    // interface
public:
    inline bool tty() const;

    // data
private:
    bool _tty;

    // disallow
private:
    ErrorConsole(const ErrorConsole &) = delete;
    ErrorConsole(const ErrorConsole &&) = delete;
    const ErrorConsole & operator= (const ErrorConsole &) = delete;
    const ErrorConsole & operator= (const ErrorConsole &&) = delete;
};


// get the inline definitions
#define pyre_journal_ErrorConsole_icc
#include "ErrorConsole.icc"
#undef pyre_journal_ErrorConsole_icc


#endif

// end of file

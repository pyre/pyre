// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#if !defined(pyre_journal_ANSI_h)
#define pyre_journal_ANSI_h


// a map of color names to the ANSI escape sequences that render them; the sequences are
// produced by {pyre::chroma}
class pyre::journal::ANSI {
    // types
public:
    // for the color tables
    using name_type = colorname_t;
    using csi_type = colorrep_t;

    // interface
public:
    // compatibility check based on the value of the {TERM} environment variable
    static bool compatible();

    // access to the color tables
    static auto null(const name_type &) -> csi_type;
    static auto ansi(const name_type &) -> csi_type;
    static auto gray(const name_type &) -> csi_type;
    static auto x11(const name_type &) -> csi_type;
    static auto misc(const name_type &) -> csi_type;

    // implementation details
private:
    // the emulation checker
    static auto emulates() -> bool;
};


#endif

// end of file

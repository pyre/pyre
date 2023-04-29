// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_journal_ANSI_h)
#define pyre_journal_ANSI_h


// a map of color names from known color spaces to the ANSI escape sequences required to render
// them in compatible terminal emulators
class pyre::journal::ANSI {
    // types
public:
    // for the color tables
    using name_type = colorname_t;
    using csi_type = colorrep_t;
    using table_type = colortable_t;

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
    // the instance builder
    static auto initialize() -> const ANSI &;

    // the color table builders
    static auto make_x11() -> table_type;
    static auto make_ansi() -> table_type;
    static auto make_gray() -> table_type;
    static auto make_misc() -> table_type;

    // the emulation checker
    static auto emulates() -> bool;

    // instance management
private:
    ANSI();

    // disable
    ANSI(const ANSI &) = delete;
    ANSI(const ANSI &&) = delete;
    const ANSI & operator= (const ANSI &) = delete;
    const ANSI & operator= (const ANSI &&) = delete;

    // data
private:
    // compatibility flag
    bool _compatible;
    // the color tables
    table_type _ansi;
    table_type _gray;
    table_type _x11;
    table_type _misc;
};


#endif

// end of file

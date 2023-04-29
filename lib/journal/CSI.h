// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_journal_CSI_h)
#define pyre_journal_CSI_h


// the generator of ANSI color control sequences given color info
class pyre::journal::CSI {
    // types
public:
    using rep_type = string_t;

    // static interface
public:
    // the reset sequence; it returns the terminal to defaults
    inline static auto reset() -> rep_type;

    // the old 3 bit colors: {code} in [30,37] or [40,47]
    inline static auto csi3(int code, bool bright=false) -> rep_type;

    // 8 bit color: values in [0,7]
    inline static auto csi8(int red, int green, int blue, bool foreground=true) -> rep_type;
    inline static auto csi8_gray(int gray, bool foreground=true) -> rep_type;

    // 24 bit color: values in [0,23]
    inline static auto csi24(int red, int green, int blue, bool foreground=true) -> rep_type;

    // turn blink on and off; there isn't wide support for this, so avoid it
    inline static auto blink(bool state=true) -> rep_type;
};


// get the inline definitions
#define pyre_journal_CSI_icc
#include "CSI.icc"
#undef pyre_journal_CSI_icc


#endif

// end of file

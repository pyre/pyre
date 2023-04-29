// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_journal_ASCII_h)
#define pyre_journal_ASCII_h


// symbolic names for the ASCII control sequences
class pyre::journal::ASCII {
    // static data members
public:
    static const char NUL = '\x00';
    static const char SOH = '\x01';
    static const char STX = '\x02';
    static const char ETX = '\x03';
    static const char EOT = '\x04';
    static const char ENQ = '\x05';
    static const char ACK = '\x06';
    static const char BEL = '\x07';
    static const char BS  = '\x08';
    static const char TAB = '\x09';
    static const char LF  = '\x0a';
    static const char VT  = '\x0b';
    static const char FF  = '\x0c';
    static const char CR  = '\x0d';
    static const char SO  = '\x0e';
    static const char SI  = '\x0f';
    static const char ESC = '\x1b';
    static const char DEL = '\x7f';
};


#endif

// end of file

// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the journal
#include <pyre/journal.h>
// support
#include <cassert>


// type aliases
using csi_t = pyre::journal::csi_t;
using ansi_t = pyre::journal::ansi_t;


// verify that the colors in the ANSI palette are the correct escape sequences
int main() {

    // verify the contents of the {ansi} color table
    // the reset sequence
    assert ((ansi_t::ansi("normal") == csi_t::reset()));
    // regular colors
    assert ((ansi_t::ansi("black") == csi_t::csi3(30)));
    assert ((ansi_t::ansi("red") == csi_t::csi3(31)));
    assert ((ansi_t::ansi("green") == csi_t::csi3(32)));
    assert ((ansi_t::ansi("brown") == csi_t::csi3(33)));
    assert ((ansi_t::ansi("blue") == csi_t::csi3(34)));
    assert ((ansi_t::ansi("purple") == csi_t::csi3(35)));
    assert ((ansi_t::ansi("cyan") == csi_t::csi3(36)));
    assert ((ansi_t::ansi("light-gray") == csi_t::csi3(37)));
    // bright colors
    assert ((ansi_t::ansi("dark-gray") == csi_t::csi3(30, true)));
    assert ((ansi_t::ansi("light-red") == csi_t::csi3(31, true)));
    assert ((ansi_t::ansi("light-green") == csi_t::csi3(32, true)));
    assert ((ansi_t::ansi("yellow") == csi_t::csi3(33, true)));
    assert ((ansi_t::ansi("light-blue") == csi_t::csi3(34, true)));
    assert ((ansi_t::ansi("light-purple") == csi_t::csi3(35, true)));
    assert ((ansi_t::ansi("light-cyan") == csi_t::csi3(36, true)));
    assert ((ansi_t::ansi("white") == csi_t::csi3(37, true)));

    // all done
    return 0;
}


// end of file

// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "forward.h"


// publicly visible types
namespace pyre::viz {
    // correctly typed file streams for reading and writing to avoid having to cast
    // {byte_t *} to {char *}
    // using fstream_t = std::basic_fstream<byte_t>;
    // using ifstream_t = std::basic_ifstream<byte_t>;
    // using ofstream_t = std::basic_ofstream<byte_t>;
    // N.B. these used to be aliases to {std::?stream<byte_t>} but the llvm libc++ seems to have
    //      trouble building streams over {unsigned char}
    // LAST CHECKED: 20220502 with llvm-13:
    //      implicit instantiation of undefined template std::codecvt<unsigned char, ...>
    // LAST CHECKED: 20231201 with macports llvm-17
    //      seems to work; must verify i'm linking against libc++
    using fstream_t = std::fstream;
    using ifstream_t = std::ifstream;
    using ofstream_t = std::ofstream;
} // namespace pyre::viz

// the api of each sub-namespace
#include "products/api.h"
#include "factories/api.h"
#include "iterators/api.h"


// end of file

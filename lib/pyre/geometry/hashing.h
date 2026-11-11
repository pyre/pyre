// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "externals.h"
#include "forward.h"


// building the hash of a value out of the hashes of its parts
namespace pyre::geometry {
    // fold the hash of one more {part} into the hash of the parts before it, so that the order
    // of the parts matters
    inline auto hashCombine(hash_t seed, hash_t part) -> hash_t;
} // namespace pyre::geometry


// get the inline definitions
#include "hashing.icc"


// end of file

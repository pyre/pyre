// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// external packages and the type aliases that shape the {pyre::h5} namespace
#include "../external.h"


// the pyre-owned hdf5 datatypes
namespace pyre::h5::types {
    // the generic base
    class Datatype;
    // the base of the atomic types
    class Atom;
    // predefined library constants, e.g. the {H5T_NATIVE_*} types
    class Predefined;
    // atomic types
    class Int;
    class Float;
    class String;
    // composite types
    class Compound;
    class Enum;
    class Array;
    class VarLen;
} // namespace pyre::h5::types


// end of file

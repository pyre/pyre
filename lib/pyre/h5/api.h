// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

// externals
#include "external.h"
// forward declarations
#include "forward.h"


// the canonical names for the pyre-owned hdf5 property lists
namespace pyre::h5::properties {
    // the generic base
    using list_t = List;
    // dataset access, creation, and transfer
    using dataset_access_t = DAPL;
    using dataset_creation_t = DCPL;
    using dataset_transfer_t = DXPL;
    // file access and creation
    using file_access_t = FAPL;
    using file_creation_t = FCPL;
    // link access and creation
    using link_access_t = LAPL;
    using link_creation_t = LCPL;
} // namespace pyre::h5::properties


// the canonical names for the pyre-owned hdf5 datatypes
namespace pyre::h5::types {
    // the generic base
    using datatype_t = Datatype;
    // the base of the atomic types
    using atom_t = Atom;
    // predefined library constants, e.g. the {H5T_NATIVE_*} types
    using predefined_t = Predefined;
    // atomic types
    using int_t = Int;
    using float_t = Float;
    using str_t = String;
    // composite types
    using composite_t = Compound;
    using enum_t = Enum;
    using array_t = Array;
    using varlen_t = VarLen;
} // namespace pyre::h5::types


// end of file

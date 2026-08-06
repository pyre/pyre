// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// external packages and the type aliases that shape the {pyre::h5} namespace
#include "../external.h"


// the pyre-owned hdf5 property lists
namespace pyre::h5::properties {
    // whether the order in which things were created is remembered; hdf5 spells these as
    // bare macros that are meant to be combined, but it also rules that indexing the order
    // requires tracking it, so we name the three states that are actually legal and leave
    // the invalid combination unrepresentable
    enum class CreationOrder : unsigned int {
        // the order is not remembered at all
        none = 0,
        // the order is recorded, so it can be recovered
        tracked = H5P_CRT_ORDER_TRACKED,
        // the order is recorded and indexed, so it can also be traversed efficiently
        indexed = H5P_CRT_ORDER_TRACKED | H5P_CRT_ORDER_INDEXED,
    };

    // the values a property list hands back and takes in, when a setting has more
    // structure than a single number
    class ChunkCache;
    class Alignment;
    class Cache;
    class PageBuffer;
    class VersionBounds;
    class FilespaceStrategy;
    class Sizes;
    class PhaseChange;
    class LinkEstimate;
    class Filter;

    // the generic base
    class List;
    // the properties shared by everything one creates
    class OCPL;
    // the properties shared by everything that lays down a name
    class STRCPL;
    // dataset access, creation, and transfer
    class DAPL;
    class DCPL;
    class DXPL;
    // group creation
    class GCPL;
    // file access and creation
    class FAPL;
    class FCPL;
    // link access and creation
    class LAPL;
    class LCPL;
    // attribute creation
    class ACPL;
} // namespace pyre::h5::properties


// end of file

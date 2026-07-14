// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// set up the namespace
namespace pyre::cuda::memory {
    // managed memory block on the device with universal access
    template <typename T, bool isConst>
    class Managed;
    // pinned memory block on the host with host-only access
    template <typename T, bool isConst>
    class Pinned;
    // mapped memory block on the host with host-only access
    template <typename T, bool isConst>
    class Mapped;
}; // namespace pyre::cuda::memory


// end of file

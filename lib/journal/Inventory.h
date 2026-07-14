// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "forward.h"
// my parts
#include "Device.h"


// the state shared by all channels of a given name+severity
class pyre::journal::Inventory {
    // types
public:
    // me
    using self_type = Inventory;

    // inventory
    using inventory_type = self_type;
    using inventory_reference = inventory_type &;
    // my parts
    using active_type = bool;
    using fatal_type = bool;
    using device_type = std::shared_ptr<Device>;

    // metamethods
public:
    inline explicit Inventory(active_type = true, fatal_type = false);

    // accessors
public:
    inline auto active() const -> active_type;
    inline auto fatal() const -> fatal_type;
    inline auto device() const -> device_type;

    // mutators
public:
    inline auto active(active_type) -> inventory_reference;
    inline auto fatal(fatal_type) -> inventory_reference;
    inline auto device(device_type) -> inventory_reference;

    template <class deviceT, class... Args>
    inline auto device(Args &&... args) -> inventory_reference;

    // syntactic sugar
public:
    inline operator active_type() const;

    // data members
private:
    active_type _active;
    fatal_type _fatal;
    device_type _device;
};


// get the inline definitions
#include "Inventory.icc"


// end of file

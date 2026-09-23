// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

#pragma once

// stdlib
#include <vector>
// set up the namespace
#include "forward.h"
// my superclass
#include "Device.h"


// a device that forwards every entry it receives to each of the devices attached to it
class pyre::journal::Splitter : public Device {
    // types
public:
    // me
    using self_type = Splitter;
    // pointers to me
    using pointer_type = std::shared_ptr<Splitter>;
    // my superclass
    using super_type = Device;
    // the devices i forward to
    using output_type = Device::pointer_type;
    using outputs_type = std::vector<output_type>;

    // metamethods
public:
    // an empty splitter, ready for devices to be attached
    inline explicit Splitter(const name_type & name = "splitter");
    // a splitter over a given set of devices
    inline Splitter(outputs_type outputs, const name_type & name = "splitter");
    // destructor
    virtual ~Splitter();

    // interface
public:
    // the devices i forward to
    inline auto outputs() const -> const outputs_type &;
    // add a device to the set
    inline auto attach(output_type output) -> Splitter &;

    // user facing messages
    virtual auto alert(const entry_type &) -> Splitter & override;
    // help messages
    virtual auto help(const entry_type &) -> Splitter & override;
    // developer messages
    virtual auto memo(const entry_type &) -> Splitter & override;

    // data
private:
    // the devices i forward to
    outputs_type _outputs;

    // disallow
private:
    Splitter(const Splitter &) = delete;
    Splitter(const Splitter &&) = delete;
    const Splitter & operator=(const Splitter &) = delete;
    const Splitter & operator=(const Splitter &&) = delete;
};


// get the inline definitions
#include "Splitter.icc"


// end of file

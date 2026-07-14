// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "forward.h"
// my superclass
#include "Device.h"
// my parts
#include "Renderer.h"
#include "Alert.h"
#include "Bland.h"
#include "Memo.h"


// a device that ignores all requests for output
class pyre::journal::Trash : public Device {
    // types
public:
    // me
    using self_type = Trash;
    // pointers to me
    using pointer_type = std::shared_ptr<Trash>;
    // my superclass
    using super_type = Device;

    using palette_type = palette_t;
    using renderer_type = Renderer;
    using renderer_pointer = renderer_type::pointer_type;

    // metamethods
public:
    // constructor
    inline Trash();
    // destructor
    virtual ~Trash();

    // interface
public:
    // user facing messages
    virtual auto alert(const entry_type &) -> Trash & override;
    // help messages
    virtual auto help(const entry_type &) -> Trash & override;
    // developer messages
    virtual auto memo(const entry_type &) -> Trash & override;

    // data
private:
    // the renderer for alerts
    renderer_pointer _alert;
    // help messages
    renderer_pointer _help;
    // and memos
    renderer_pointer _memo;

    // disallow
private:
    Trash(const Trash &) = delete;
    Trash(const Trash &&) = delete;
    const Trash & operator=(const Trash &) = delete;
    const Trash & operator=(const Trash &&) = delete;
};


// get the inline definitions
#include "Trash.icc"


// end of file

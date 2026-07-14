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
#include "Renderer.h"


// a formatter for messages that are meant for the end users; currently, this means {info_t},
// {warning_t}, and {error_t}
class pyre::journal::Alert : public Renderer {
    // type aliases
public:
    // me
    using self_type = Alert;
    // my superclass
    using super_type = Renderer;

    // metamethods
public:
    virtual ~Alert();
    Alert() = default;

    // implementation details
protected:
    virtual void header(palette_type &, linebuf_type &, const entry_type &) const override;
    virtual void body(palette_type &, linebuf_type &, const entry_type &) const override;
    virtual void footer(palette_type &, linebuf_type &, const entry_type &) const override;

    // configuration
private:
    const line_type _headerMarker { " >> " };
    const line_type _bodyMarker { " -- " };
    const line_type _footerMarker { " .. " };

    // disallow
private:
    Alert(const Alert &) = delete;
    Alert(const Alert &&) = delete;
    const Alert & operator=(const Alert &) = delete;
    const Alert & operator=(const Alert &&) = delete;
};


// end of file

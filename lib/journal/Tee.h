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
#include "Splitter.h"
// the devices i assemble
#include "File.h"


// a splitter that writes every entry to the console and to a set of files
class pyre::journal::Tee : public Splitter {
    // types
public:
    // me
    using self_type = Tee;
    // pointers to me
    using pointer_type = std::shared_ptr<Tee>;
    // my superclass
    using super_type = Splitter;
    // the files
    using path_type = File::path_type;
    using paths_type = std::vector<path_type>;

    // metamethods
public:
    // a tee to the console and to a file at each of the given {paths}
    Tee(const paths_type & paths = {}, const name_type & name = "tee");
    // destructor
    virtual ~Tee();

    // disallow
private:
    Tee(const Tee &) = delete;
    Tee(const Tee &&) = delete;
    const Tee & operator=(const Tee &) = delete;
    const Tee & operator=(const Tee &&) = delete;
};


// get the inline definitions
#include "Tee.icc"


// end of file

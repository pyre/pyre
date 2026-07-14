// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

#include <map>
#include <string>

namespace pyre { namespace patterns {
    template <typename Object, typename Name>
    class Registrar;
}} // namespace pyre::patterns

template <typename Object, typename Name = std::string>
class pyre::patterns::Registrar : public std::map<Name, Object *> {
    // typedefs
public:
    typedef Name name_t;
    typedef Object object_t;
    typedef std::map<name_t, object_t *> map_t;
    typedef typename map_t::iterator iterator_t;

    // interface
    inline ~Registrar();
};


// get the inline definitions
#include "Registrar.icc"


// end of file

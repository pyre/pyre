// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once

#include <map>
#include <string>

namespace pyre::patterns {
    template <typename objectT, typename nameT>
    class Registrar;
} // namespace pyre::patterns

template <typename objectT, typename nameT = std::string>
class pyre::patterns::Registrar : public std::map<nameT, objectT *> {
    // type aliases
public:
    // me
    using self_type = Registrar<objectT, nameT>;
    // my superclass
    using super_type = std::map<nameT, objectT *>;
    // my parts
    using name_type = nameT;
    using object_type = objectT;
    using map_type = super_type;
    using iterator_type = map_type::iterator;

    // interface
    inline ~Registrar();
};


// get the inline definitions
#include "Registrar.icc"


// end of file

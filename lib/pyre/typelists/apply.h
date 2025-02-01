// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved

// code guard
#pragma once

// add a type to the end of an existing list

// forward declaration
#include "forward.h"

// support
#include "types.h"
#include "templates.h"
#include "concat.h"


// apply a template to no arguments
template <template <typename...> class templateT>
struct pyre::typelists::apply_t<
    pyre::typelists::templates_t<templateT>, pyre::typelists::types_t<>> {
    using type = types_t<>;
};

// apply a template to a single set of arguments
template <template <typename...> class templateT, typename... T>
struct pyre::typelists::apply_t<
    pyre::typelists::templates_t<templateT>, pyre::typelists::types_t<T...>> {
    using type = types_t<templateT<T...>>;
};

// apply a template to a bunch of types
template <template <typename...> class templateT, typename... carT, typename... cdrT>
struct pyre::typelists::apply_t<
    pyre::typelists::templates_t<templateT>,
    pyre::typelists::types_t<pyre::typelists::types_t<carT...>, cdrT...>> {
    using type = typename pyre::typelists::concat_t<
        // the template against the first set of arguments
        typename apply_t<templates_t<templateT>, types_t<carT...>>::type,
        // followed by the template against the rest of the arguments
        typename apply_t<templates_t<templateT>, types_t<cdrT...>>::type
        // done
        >::type;
};

// apply a bunch of templates to a bunch of types
template <
    template <typename...> class carT, template <typename...> class... cdrT, typename... argsT>
struct pyre::typelists::apply_t<pyre::typelists::templates_t<carT, cdrT...>, argsT...> {
    using type = typename pyre::typelists::concat_t<
        // the car against the args
        typename apply_t<pyre::typelists::templates_t<carT>, argsT...>::type,
        // the cdr against the args
        typename apply_t<pyre::typelists::templates_t<cdrT...>, argsT...>::type
        // done
        >::type;
};


// end of file

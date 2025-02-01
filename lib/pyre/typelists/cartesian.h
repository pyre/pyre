// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved

// code guard
#pragma once

// compute the cartesian product of type lists

// forward declarations
#include "forward.h"

// support
#include "types.h"
#include "merge.h"
#include "concat.h"


// the forward declaration
// base case: nil x nil
template <>
struct pyre::typelists::cartesian_t<pyre::typelists::types_t<>, pyre::typelists::types_t<>> {
    using type = types_t<>;
};

// base case: list x nil
template <typename carT, typename... cdrT>
struct pyre::typelists::cartesian_t<
    pyre::typelists::types_t<carT, cdrT...>, pyre::typelists::types_t<>> {
    using type = types_t<>;
};

// base case: nil x list
template <typename carT, typename... cdrT>
struct pyre::typelists::cartesian_t<
    pyre::typelists::types_t<>, pyre::typelists::types_t<carT, cdrT...>> {
    using type = types_t<>;
};

// list x list
template <typename car1T, typename... cdr1T, typename car2T, typename... cdr2T>
struct pyre::typelists::cartesian_t<
    pyre::typelists::types_t<car1T, cdr1T...>, pyre::typelists::types_t<car2T, cdr2T...>> {
    using type = typename concat_t<
        // car1T x car2T
        types_t<typename merge_t<car1T, car2T>::type>,
        // car1T x cdr2T
        typename cartesian_t<types_t<car1T>, types_t<cdr2T...>>::type,
        // cdr1T x list
        typename cartesian_t<types_t<cdr1T...>, types_t<car2T, cdr2T...>>::type
        // all done
        >::type;
};

// list x list x list x list...
template <typename... T, typename... U, typename... V>
struct pyre::typelists::cartesian_t<
    pyre::typelists::types_t<T...>, pyre::typelists::types_t<U...>, V...> {
    using type =
        typename cartesian_t<types_t<T...>, typename cartesian_t<types_t<U...>, V...>::type>::type;
};


// end of file

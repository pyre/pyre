// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved


// STL
#include <utility>
#include <tuple>

// declarations
#include <pyre/typelists/list.h>

// a tuple maker
template <typename...>
struct tuple_t;
// from {types_t}
template <typename... T>
struct tuple_t<pyre::typelists::types_t<T...>> {
    using type = std::tuple<T...>;
};


// driver
int
main()
{
    // make a type list
    using ints_t = typename pyre::typelists::list_t<int, 3>::type;

    // check
    static_assert(
        std::is_same_v<
            // check
            ints_t, pyre::typelists::types_t<int, int, int>>,
        "mismatch in ints_t");

    // place the {ints_t} in a tuple
    using my_t = typename tuple_t<ints_t>::type;
    // instantiate
    constexpr auto t = my_t { 0, 1, 2 };
    // check
    static_assert(std::get<0>(t) == 0);
    static_assert(std::get<1>(t) == 1);
    static_assert(std::get<2>(t) == 2);

    // all done
    return 0;
}


// end of file

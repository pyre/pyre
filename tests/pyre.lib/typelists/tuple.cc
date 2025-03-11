// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2025 all rights reserved


// declarations
#include <pyre/typelists/tuple.h>


// driver
int
main()
{
    // make a type list
    using ints_t = pyre::typelists::types_t<int, int, int>;
    // use the {ints_t} to declare a tuple
    using my_t = typename pyre::typelists::tuple_t<ints_t>::type;
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

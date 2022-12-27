// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// support
#include <cassert>
#include <tuple>
// get the grid
#include <pyre/grid.h>


// type alias
using idx_t = pyre::grid::index_t<4>;

// converter
auto convert = [](auto&& tuple) {
    // the converter
    constexpr auto array = [](auto&&... x) {
        return idx_t { std::forward<decltype(x)>(x) ... };
    };
    // invoked
    return std::apply(array, tuple);
 };


// exercise the filling constructor
int main(int argc, char * argv[]) {
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("index_from_tuple");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.index");

    // make a tuple
    auto src = std::make_tuple(0,1,2,3);

    // convert to an index
    auto idx = convert(src);

    // show me
    channel
        << "idx: " << idx
        << pyre::journal::endl(__HERE__);

    // all done
    return 0;
}


// end of file

// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved


// get the grid
#include <pyre/grid.h>

// the idea here is check whether we can raise the abstraction level closer to the user;
// {enum}s don't cut it, for a variety of reasons; so here is the foundation for a better
// solution...


// type alias
using idx_t = pyre::grid::index_t<2>;

// polarizations
class pol {
    // the values
public:
    static const int hh = 0;
    static const int hv = 1;
    static const int vh = 2;
    static const int vv = 3;
};

// colors
class color {
    // the values
public:
    static const int red = 0;
    static const int green = 1;
    static const int blue = 2;
};


// check the enums can be used as indices
int main(int argc, char *argv[]) {
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("index_enum");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.index");

    // make an index
    constexpr idx_t idx { pol::hv, color::blue };
    // show me
    channel
        << "index: " << idx
        << pyre::journal::endl(__HERE__);
    // verify it gets represented correctly
    static_assert( idx[0] == pol::hv );
    static_assert( idx[1] == color::blue );

    // all done
    return 0;
}


// end of file

// -*- coding: utf-8 -*-
//
// bianca giovanardi
// (c) 2021 all rights reserved
//

// support
#include <cassert>
// get the grid
#include <pyre/grid.h>


// simple check that the map from index space to offsets is correct
int main(int argc, char * argv[]) {
    // initialize the journal
    pyre::journal::init(argc, argv);
    pyre::journal::application("symmetric_visit");
    // make a channel
    pyre::journal::debug_t channel("pyre.grid.symmetric");

    // pick a dimension
    constexpr int D = 3;

    // sign on
    channel << "tensor dimension " << D << pyre::journal::newline;
    channel << "computing offset of largest index:" << pyre::journal::newline;

    {
        // type alias
        using symmetric_rank1_t = pyre::grid::symmetric_t<1>;
        // pick a shape
        constexpr symmetric_rank1_t::shape_type shape { D };
        // make a canonical packing strategy
        constexpr symmetric_rank1_t packing { shape };
        // compute largest offset
        constexpr auto offset = packing[symmetric_rank1_t::index_type{ D - 1 }];
        // report
        channel << "rank 1: " << offset << pyre::journal::newline;
        // assert the offset of the largest index is the last element
        static_assert( offset == packing.cells() - 1 );
    }

    {
        // type alias        
        using symmetric_rank2_t = pyre::grid::symmetric_t<2>;
        // pick a shape
        constexpr symmetric_rank2_t::shape_type shape { D, D };
        // make a canonical packing strategy
        constexpr symmetric_rank2_t packing { shape };
        // compute largest offset
        constexpr auto offset = packing[symmetric_rank2_t::index_type{ D - 1, D - 1 }];
        // report
        channel << "rank 2: " << offset << pyre::journal::newline;
        // assert the offset of the largest index is the last element
        static_assert( offset == packing.cells() - 1 );
    }

    {
        // type alias        
        using symmetric_rank3_t = pyre::grid::symmetric_t<3>;
        // pick a shape
        constexpr symmetric_rank3_t::shape_type shape { D, D, D };
        // make a canonical packing strategy
        constexpr symmetric_rank3_t packing { shape };
        // compute largest offset
        constexpr auto offset = packing[symmetric_rank3_t::index_type{ D - 1, D - 1, D - 1 }];
        // report
        channel << "rank 3: " << offset << pyre::journal::newline;
        // assert the offset of the largest index is the last element
        static_assert( offset == packing.cells() - 1 );
    }

    {
        // type alias        
        using symmetric_rank4_t = pyre::grid::symmetric_t<4>;
        // pick a shape
        constexpr symmetric_rank4_t::shape_type shape { D, D, D, D };
        // make a canonical packing strategy
        constexpr symmetric_rank4_t packing { shape };
        // compute largest offset
        constexpr auto offset = 
            packing[symmetric_rank4_t::index_type{ D - 1, D - 1, D - 1, D - 1 }];
        // report
        channel << "rank 4: " << offset << pyre::journal::newline;
        // assert the offset of the largest index is the last element
        static_assert( offset == packing.cells() - 1 );
    }

    {
        // type alias        
        using symmetric_rank5_t = pyre::grid::symmetric_t<5>;
        // pick a shape
        constexpr symmetric_rank5_t::shape_type shape { D, D, D, D, D };
        // make a canonical packing strategy
        constexpr symmetric_rank5_t packing { shape };
        // compute largest offset
        constexpr auto offset = 
            packing[symmetric_rank5_t::index_type{ D - 1, D - 1, D - 1, D - 1, D - 1 }];
        // report
        channel << "rank 5: " << offset << pyre::journal::newline;
        // assert the offset of the largest index is the last element
        static_assert( offset == packing.cells() - 1 );
    }

    // flush
    channel << pyre::journal::endl(__HERE__);


    // all done
    return 0;
}


// end of file

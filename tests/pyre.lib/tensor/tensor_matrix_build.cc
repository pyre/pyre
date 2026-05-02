// -*- coding: utf-8 -*-
//
// bianca giovanardi
// (c) 1998-2026 all rights reserved
//


// support
#include <cassert>
// get the tensor algebra
#include <pyre/tensor.h>


// use namespace for readability
using namespace pyre::tensor;


// main program
int
main(int argc, char * argv[])
{
    // two vectors in 3D
    constexpr auto v1 = vector_t<3, int> { -2, 2, 10 };
    constexpr auto v2 = vector_t<3> { 1.0, 2.0, 3.0 / 2.0 };

    // use {v1} and {v2} to build {A_row} row-wise
    constexpr auto A_row = rows(v1, v2);

    // extract the rows of {A}
    constexpr auto A_rows = rows(A_row);
    constexpr auto row1 = std::get<0>(A_rows);
    constexpr auto row2 = std::get<1>(A_rows);

    // rebuild the matrix with the extracted rows
    constexpr auto A_row2 = rows(row1, row2);

    // verify result
    static_assert(A_row2 == A_row);

    // use {v1} and {v2} to build {A_col} column-wise
    constexpr auto A_col = columns(v1, v2);

    // extract the columns of {A}
    constexpr auto A_cols = columns(A_col);
    constexpr auto col1 = std::get<0>(A_cols);
    constexpr auto col2 = std::get<1>(A_cols);

    // rebuild the matrix with the extracted rows
    constexpr auto A_col2 = columns(col1, col2);

    // verify result
    static_assert(A_col2 == A_col);

    // all done
    return 0;
}


// end of file

// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// dependencies
#include <pyre/tensor.h>
// support
#include <cassert>
#include <sstream>
#include <string>
#include <vector>


// use namespace for readability
using namespace pyre::tensor;


// render {item} the way a stream sees it
template <class itemT>
auto
render(const itemT & item) -> std::string
{
    // make a stream
    std::ostringstream stream;
    // inject the item
    stream << item;
    // and hand off the text
    return stream.str();
}


// gather the stored values of {tensor}, in storage order
template <class tensorT>
auto
storage(const tensorT & tensor) -> std::vector<double>
{
    // make a pile
    std::vector<double> values;
    // go through the stored values
    for (const auto value : tensor) {
        // and add each one to the pile
        values.push_back(value);
    }
    // hand off the pile
    return values;
}


// verify the rendering of tensors
int
main()
{
    // matrices of every shape up to 3x3 render row by row
    assert(render(matrix_t<1, 1> { 1 }) == "[ [ 1 ] ]");
    assert(render(matrix_t<1, 2> { 0, 1 }) == "[ [ 0, 1 ] ]");
    assert(render(matrix_t<2, 1> { 0, 1 }) == "[ [ 0 ],[ 1 ] ]");
    assert(render(matrix_t<2, 2> { 0, 1, 2, 3 }) == "[ [ 0, 1 ],[ 2, 3 ] ]");
    assert(
        render(matrix_t<3, 3> { 0, 1, 2, 3, 4, 5, 6, 7, 8 })
        == "[ [ 0, 1, 2 ],[ 3, 4, 5 ],[ 6, 7, 8 ] ]");

    // vectors render as a single row
    assert(render(vector_t<1> { 1 }) == "[ 1 ]");
    assert(render(vector_t<2> { 1, 1 }) == "[ 1, 1 ]");
    assert(render(vector_t<3> { 1, 1, 1 }) == "[ 1, 1, 1 ]");

    // a symmetric matrix stores only its upper triangle
    symmetric_matrix_t<2> S { 0, 1, /*1, */ 2 };
    // but renders in full
    assert(render(S) == "[ [ 0, 1 ],[ 1, 2 ] ]");
    // knows it is symmetric
    assert(S.is_symmetric());
    // renders its shape
    assert(render(S.shape()) == "[ 2, 2 ]");
    // and holds exactly the values it was given
    assert((storage(S) == std::vector<double> { 0, 1, 2 }));

    // a diagonal matrix stores only its diagonal
    diagonal_matrix_t<2> R { 0, 1 };
    // but renders in full
    assert(render(R) == "[ [ 0, 0 ],[ 0, 1 ] ]");
    // knows it is diagonal
    assert(R.is_diagonal());
    // and therefore symmetric
    assert(R.is_symmetric());
    // renders its shape
    assert(render(R.shape()) == "[ 2, 2 ]");
    // and holds exactly the values it was given
    assert((storage(R) == std::vector<double> { 0, 1 }));

    // all done
    return 0;
}


// end of file

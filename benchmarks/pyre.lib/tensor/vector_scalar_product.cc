// -*- coding: utf-8 -*-
//
// bianca giovanardi
// (c) 1998-2023 all rights reserved
//


// get array
#include <array>
#include <iostream>

// get support
#include <pyre/timers.h>
#include <pyre/journal.h>
#include <pyre/tensor.h>


// type aliases
using process_timer_t = pyre::timers::process_timer_t;


void
vector_scalar_product(int N)
{
    // make a channel
    pyre::journal::info_t channel("tests.timer.vector_scalar_product");

    // make a timer
    process_timer_t t("tests.timer");

    channel << "Computing " << N << " scalar products" << pyre::journal::endl;


    // ARRAY FOR LOOP
    // array vector
    std::array<double, 3> vector_array_1 { 1.0, -1.0, 2.0 };
    std::array<double, 3> vector_array_2 { 1.0, 1.0, 2.0 };
    double result_array_for = 0.0;

    // reset timer
    t.reset();
    // start timer
    t.start();

    // vector * vector (array, for loop)
    for (int n = 0; n < N; ++n) {
        for (size_t i = 0; i < vector_array_1.size(); ++i) {
            result_array_for += vector_array_1[i] * vector_array_2[i];
        }
    }

    // stop the timer
    t.stop();

    // report
    channel << "array (for loop)" << pyre::journal::newline << pyre::journal::indent(1)
            << "result = " << result_array_for << pyre::journal::newline
            << "process time = " << t.ms() << " ms " << pyre::journal::newline
            << pyre::journal::outdent(1) << pyre::journal::endl;


    // ARRAY EXPANDED BY HAND
    double result_array = 0.0;

    // reset timer
    t.reset();
    // start timer
    t.start();

    // vector * vector (array, expanded)
    for (int n = 0; n < N; ++n) {
        result_array += vector_array_1[0] * vector_array_2[0]
                      + vector_array_1[1] * vector_array_2[1]
                      + vector_array_1[2] * vector_array_2[2];
    }

    // stop the timer
    t.stop();

    // report
    channel << "array (expanded)" << pyre::journal::newline << pyre::journal::indent(1)
            << "result = " << result_array << pyre::journal::newline << "process time = " << t.ms()
            << " ms " << pyre::journal::newline << pyre::journal::outdent(1) << pyre::journal::endl;


    // PYRE TENSOR
    // tensor vector
    pyre::tensor::vector_t<3> vector_1 { 1.0, -1.0, 2.0 };
    pyre::tensor::vector_t<3> vector_2 { 1.0, 1.0, 2.0 };
    pyre::tensor::scalar_t result_tensor = 0.0;

    // reset timer
    t.reset();
    // start timer
    t.start();

    for (int n = 0; n < N; ++n) {
        // vector * vector (tensor)
        result_tensor += vector_1 * vector_2;
    }

    // stop the timer
    t.stop();

    // report
    channel << "pyre tensor" << pyre::journal::newline << pyre::journal::indent(1)
            << "result = " << result_tensor << pyre::journal::newline << "process time = " << t.ms()
            << " ms " << pyre::journal::newline << pyre::journal::outdent(1) << pyre::journal::endl;


    // all done
    return;
}


int
main()
{
    // number of times to do operation
    int N = 1 << 25;

    // vector * vector
    vector_scalar_product(N);

    // all done
    return 0;
}


// end of file

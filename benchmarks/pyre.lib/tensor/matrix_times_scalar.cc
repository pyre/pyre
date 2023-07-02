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
matrix_times_scalar(int N)
{
    // make a channel
    pyre::journal::info_t channel("tests.timer.matrix_times_scalar");

    // make a timer
    process_timer_t t("tests.timer");

    channel << "Computing " << N << " scalar-matrix multiplications" << pyre::journal::endl;


    // ARRAY
    // a scalar
    pyre::tensor::real scalar = sqrt(2);

    // array tensor
    std::array<double, 9> tensor_c { 1.0, -1.0, 2.0, 1.0, 0.0, 1.0, 2.0, -1.0, 0.0 };
    std::array<double, 9> result_c { 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 };

    // reset timer
    t.reset();
    // start timer
    t.start();

    for (int n = 0; n < N; ++n) {
        // scalar * vector (array)
        for (size_t i = 0; i < tensor_c.size(); ++i) {
            result_c[i] += scalar * tensor_c[i];
        }
    }

    // stop the timer
    t.stop();

    // report
    channel << "array (for loop)" << pyre::journal::newline << pyre::journal::indent(1)
            << "result = " << result_c[0] << ", " << result_c[1] << ", " << result_c[2] << ", "
            << result_c[3] << ", " << result_c[4] << ", " << result_c[5] << ", " << result_c[6]
            << ", " << result_c[7] << ", " << result_c[8] << pyre::journal::newline
            << "process time = " << t.ms() << " ms " << pyre::journal::newline
            << pyre::journal::outdent(1) << pyre::journal::endl;


    // PYRE TENSOR (operator*)
    // tensor vector
    pyre::tensor::matrix_t<3> tensor { 1.0, -1.0, 2.0, 1.0, 0.0, 1.0, 2.0, -1.0, 0.0 };
    pyre::tensor::matrix_t<3> result_tensor { 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 };

    // reset timer
    t.reset();
    // start timer
    t.start();

    for (int n = 0; n < N; ++n) {
        // scalar * vector (tensor)
        result_tensor += scalar * tensor;
    }

    // stop the timer
    t.stop();

    // report
    channel << "pyre tensor (result_tensor += scalar * tensor)" << pyre::journal::newline
            << pyre::journal::indent(1) << "result = " << result_tensor << pyre::journal::newline
            << "process time = " << t.ms() << " ms " << pyre::journal::newline
            << pyre::journal::outdent(1) << pyre::journal::endl;

    // all done
    return;
}


int
main()
{
    // number of times to do operation
    int N = 1 << 25;

    // scalar * matrix
    matrix_times_scalar(N);

    // all done
    return 0;
}


// end of file

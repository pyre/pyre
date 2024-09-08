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
norm_3D(int N)
{
    // make a channel
    pyre::journal::info_t channel("tests.timer.norm");

    // make a timer
    process_timer_t t("tests.timer");

    channel << "Computing " << N << " norms (3x3)" << pyre::journal::endl;


    // ARRAY

    // array tensor
    std::array<double, 9> tensor_c { 1.0, -1.0, 2.0, 1.0, 0.0, 1.0, -1.0, 2.0, -2.0 };
    double result_c = 0;

    // reset timer
    t.reset();
    // start timer
    t.start();

    for (int n = 0; n < N; ++n) {
        // norm (array)
        result_c += std::sqrt(
            tensor_c[0] * tensor_c[0] + tensor_c[1] * tensor_c[1] + tensor_c[2] * tensor_c[2]
            + tensor_c[3] * tensor_c[3] + tensor_c[4] * tensor_c[4] + tensor_c[5] * tensor_c[5]
            + tensor_c[6] * tensor_c[6] + tensor_c[7] * tensor_c[7] + tensor_c[8] * tensor_c[8]);
    }

    // stop the timer
    t.stop();

    // report
    channel << "array " << pyre::journal::newline << pyre::journal::indent(1)
            << "result = " << result_c << pyre::journal::newline << "process time = " << t.ms()
            << " ms " << pyre::journal::newline << pyre::journal::outdent(1) << pyre::journal::endl;


    // PYRE TENSOR
    // tensor matrix
    pyre::tensor::matrix_t<3> tensor { 1.0, -1.0, 2.0, 1.0, 0.0, 1.0, -1.0, 2.0, -2.0 };
    pyre::tensor::real result_tensor = 0.;

    // reset timer
    t.reset();
    // start timer
    t.start();

    for (int n = 0; n < N; ++n) {
        // norm (tensor)
        result_tensor += pyre::tensor::norm(tensor);
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

    // run benchmark for 3D matrix
    norm_3D(N);

    // all done
    return 0;
}


// end of file

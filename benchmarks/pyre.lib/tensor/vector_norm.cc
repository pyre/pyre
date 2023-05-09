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
norm_vector(int N)
{
    // make a channel
    pyre::journal::info_t channel("tests.timer.norm_vector");

    // make a timer
    process_timer_t t("tests.timer");

    channel << "Computing " << N << " norms of vectors" << pyre::journal::endl;


    // ARRAY

    // array vector
    std::array<double, 3> vector_c { 1.0, -1.0, 2.0 };
    double result_c = 0.0;

    // reset timer
    t.reset();
    // start timer
    t.start();

    for (int n = 0; n < N; ++n) {
        double squared_sum = 0.;
        // norm of a vector (array)
        for (size_t i = 0; i < vector_c.size(); ++i) {
            squared_sum += vector_c[i] * vector_c[i];
        }

        result_c += std::sqrt(squared_sum);
    }

    // stop the timer
    t.stop();

    // report
    channel << "array (for loop) " << pyre::journal::newline << pyre::journal::indent(1)
            << "result = " << result_c << pyre::journal::newline << "process time = " << t.ms()
            << " ms " << pyre::journal::newline << pyre::journal::outdent(1) << pyre::journal::endl;


    // PYRE TENSOR
    // tensor vector
    pyre::tensor::vector_t<3> vector { 1.0, -1.0, 2.0 };
    pyre::tensor::real result_tensor = 0.;

    // reset timer
    t.reset();
    // start timer
    t.start();

    for (int n = 0; n < N; ++n) {
        // norm of a vector (tensor)
        result_tensor += pyre::tensor::norm(vector);
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

    // norm of a vector
    norm_vector(N);

    // all done
    return 0;
}


// end of file

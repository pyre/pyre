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
vector_plus_vector(int N)
{
    // make a channel
    pyre::journal::info_t channel("tests.timer.vector_plus_vector");

    // make a timer
    process_timer_t t("tests.timer");

    channel << "Computing " << N << " vector-vector sums" << pyre::journal::endl;


    // ARRAY

    // array vector
    std::array<double, 3> vector1_c { 1.0, -1.0, 2.0 };
    std::array<double, 3> vector2_c { 1.0, -1.0, 2.0 };
    std::array<double, 3> result_c { 0.0, 0.0, 0.0 };

    // reset timer
    t.reset();
    // start timer
    t.start();

    for (int n = 0; n < N; ++n) {
        // vector + vector (array)
        for (size_t i = 0; i < vector1_c.size(); ++i) {
            result_c[i] += vector2_c[i] + vector1_c[i];
        }
    }

    // stop the timer
    t.stop();

    // report
    channel << "array (for loop) " << pyre::journal::newline << pyre::journal::indent(1)
            << "result = [ " << result_c[0] << ", " << result_c[1] << ", " << result_c[2] << " ]"
            << pyre::journal::newline << "process time = " << t.ms() << " ms "
            << pyre::journal::newline << pyre::journal::outdent(1) << pyre::journal::endl;


    // PYRE TENSOR
    // tensor vector
    pyre::tensor::vector_t<3> vector1 { 1.0, -1.0, 2.0 };
    pyre::tensor::vector_t<3> vector2 { 1.0, -1.0, 2.0 };
    pyre::tensor::vector_t<3> result_tensor { 0.0, 0.0, 0.0 };

    // reset timer
    t.reset();
    // start timer
    t.start();

    for (int n = 0; n < N; ++n) {
        // vector + vector (tensor)
        result_tensor += vector2 + vector1;
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

    // vector plus vector
    vector_plus_vector(N);

    // all done
    return 0;
}


// end of file

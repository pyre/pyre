// -*- coding: utf-8 -*-
//
// bianca giovanardi
// (c) 2021 all rights reserved
//


// get array
#include <array>
#include <iostream>

// get support
#include <pyre/timers.h>
#include <pyre/journal.h>
#include <pyre/tensor.h>


// type aliases
using timer_t = pyre::timers::process_timer_t;


void determinant() 
{
    // make a channel
    pyre::journal::info_t channel("tests.timer.determinant");

    // make a timer
    timer_t t("tests.timer");
    
    // number of times to do operation
    int N = 1<<25;

    channel << "Computing " << N << " determinants" << pyre::journal::endl;


    // ARRAY

    // array tensor
    std::array<double, 9> tensor_c {1.0, -1.0, 2.0, 1.0};
    double result_c = 0;

    // reset timer
    t.reset();
    // start timer
    t.start();

    for (int n = 0; n < N; ++n) { 
        // determinant (array)
        result_c += tensor_c[0] * tensor_c[3] - tensor_c[1] * tensor_c[2];
    }

    // stop the timer
    t.stop();

    // report
    channel 
        << "array (for loop)" << pyre::journal::newline
        << pyre::journal::indent(1) 
        << "result = " << result_c << pyre::journal::newline
        << "process time = " << t.ms() << " ms " << pyre::journal::newline
        << pyre::journal::outdent(1) << pyre::journal::endl;


    // PYRE TENSOR
    // tensor vector
    pyre::tensor::matrix_t<2> tensor {1.0, -1.0, 2.0, 1.0};
    pyre::tensor::real result_tensor = 0.;

    // reset timer
    t.reset();
    // start timer
    t.start();

    for (int n = 0; n < N; ++n) { 
        // determinant (tensor)
        result_tensor += pyre::tensor::determinant(tensor);
    }

    // stop the timer
    t.stop();

    // report
    channel
        << "pyre tensor" << pyre::journal::newline
        << pyre::journal::indent(1) 
        << "result = " << result_tensor << pyre::journal::newline
        << "process time = " << t.ms() << " ms " << pyre::journal::newline
        << pyre::journal::outdent(1) << pyre::journal::endl;

    // all done
    return;
}


int main() {

    determinant();

    // all done
    return 0;
}


// end of file

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
determinant_2D(int N)
{
    // make a channel
    pyre::journal::info_t channel("tests.timer.determinant");

    // make a timer
    process_timer_t t("tests.timer");

    channel << "Computing " << N << " determinants (2x2)" << pyre::journal::endl;


    // ARRAY

    // array tensor
    std::array<double, 4> tensor_c { 1.0, -1.0, 2.0, 1.0 };
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
    channel << "array " << pyre::journal::newline << pyre::journal::indent(1)
            << "result = " << result_c << pyre::journal::newline << "process time = " << t.ms()
            << " ms " << pyre::journal::newline << pyre::journal::outdent(1) << pyre::journal::endl;


    // PYRE TENSOR
    // tensor matrix
    pyre::tensor::matrix_t<2> tensor { 1.0, -1.0, 2.0, 1.0 };
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
    channel << "pyre tensor" << pyre::journal::newline << pyre::journal::indent(1)
            << "result = " << result_tensor << pyre::journal::newline << "process time = " << t.ms()
            << " ms " << pyre::journal::newline << pyre::journal::outdent(1) << pyre::journal::endl;

    // all done
    return;
}


void
determinant_3D(int N)
{
    // make a channel
    pyre::journal::info_t channel("tests.timer.determinant");

    // make a timer
    process_timer_t t("tests.timer");

    channel << "Computing " << N << " determinants (3x3)" << pyre::journal::endl;


    // ARRAY

    // array tensor
    std::array<double, 9> tensor_c { 1.0, -1.0, 2.0, 1.0, 0.0, 1.0, -1.0, 2.0, -2.0 };
    double result_c = 0;

    // reset timer
    t.reset();
    // start timer
    t.start();

    for (int n = 0; n < N; ++n) {
        // determinant (array)
        result_c += tensor_c[0] * (tensor_c[4] * tensor_c[8] - tensor_c[5] * tensor_c[7])
                  - tensor_c[1] * (tensor_c[3] * tensor_c[8] - tensor_c[5] * tensor_c[6])
                  + tensor_c[2] * (tensor_c[3] * tensor_c[7] - tensor_c[4] * tensor_c[6]);
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
        // determinant (tensor)
        result_tensor += pyre::tensor::determinant(tensor);
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


void
determinant_3D_symmetric(int N)
{
    // make a channel
    pyre::journal::info_t channel("tests.timer.determinant");

    // make a timer
    process_timer_t t("tests.timer");

    channel << "Computing " << N << " determinants (3x3, symmetric)" << pyre::journal::endl;


    // ARRAY

    // array tensor
    std::array<double, 9> tensor_c { 1.0, -1.0, 2.0, -1.0, 1.0, 0.0, 2.0, 0.0, 1.0 };
    double result_c = 0;

    // reset timer
    t.reset();
    // start timer
    t.start();

    for (int n = 0; n < N; ++n) {
        // determinant (array)
        result_c += tensor_c[0] * (tensor_c[4] * tensor_c[8] - tensor_c[5] * tensor_c[7])
                  - tensor_c[1] * (tensor_c[3] * tensor_c[8] - tensor_c[5] * tensor_c[6])
                  + tensor_c[2] * (tensor_c[3] * tensor_c[7] - tensor_c[4] * tensor_c[6]);
    }

    // stop the timer
    t.stop();

    // report
    channel << "array " << pyre::journal::newline << pyre::journal::indent(1)
            << "result = " << result_c << pyre::journal::newline << "process time = " << t.ms()
            << " ms " << pyre::journal::newline << pyre::journal::outdent(1) << pyre::journal::endl;


    // PYRE TENSOR
    // tensor matrix
    pyre::tensor::symmetric_matrix_t<3> tensor { 1.0,
                                                 -1.0,
                                                 2.0,
                                                 /*-1.0,*/ 1.0,
                                                 0.0,
                                                 /*2.0, 0.0,*/ 1.0 };
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
    channel << "pyre tensor" << pyre::journal::newline << pyre::journal::indent(1)
            << "result = " << result_tensor << pyre::journal::newline << "process time = " << t.ms()
            << " ms " << pyre::journal::newline << pyre::journal::outdent(1) << pyre::journal::endl;

    // all done
    return;
}


void
determinant_3D_diagonal(int N)
{
    // make a channel
    pyre::journal::info_t channel("tests.timer.determinant");

    // make a timer
    process_timer_t t("tests.timer");

    channel << "Computing " << N << " determinants (3x3, diagonal)" << pyre::journal::endl;


    // ARRAY

    // array tensor
    std::array<double, 3> tensor_c { 1.0, -1.0, 2.0 };
    double result_c = 0;

    // reset timer
    t.reset();
    // start timer
    t.start();

    for (int n = 0; n < N; ++n) {
        // determinant (array)
        result_c += tensor_c[0] * tensor_c[1] * tensor_c[2];
    }

    // stop the timer
    t.stop();

    // report
    channel << "array " << pyre::journal::newline << pyre::journal::indent(1)
            << "result = " << result_c << pyre::journal::newline << "process time = " << t.ms()
            << " ms " << pyre::journal::newline << pyre::journal::outdent(1) << pyre::journal::endl;


    // PYRE TENSOR
    // tensor matrix
    pyre::tensor::diagonal_matrix_t<3> tensor { 1.0, -1.0, 2.0 };
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

    // run benchmark for 2D matrix
    determinant_2D(N);

    // run benchmark for 3D matrix
    determinant_3D(N);

    // run benchmark for 3D symmetric matrix
    determinant_3D_symmetric(N);

    // run benchmark for 3D diagonal matrix
    determinant_3D_diagonal(N);

    // all done
    return 0;
}


// end of file

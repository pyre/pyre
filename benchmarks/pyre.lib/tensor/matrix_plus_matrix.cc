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
matrix_plus_matrix(int N)
{
    // make a channel
    pyre::journal::info_t channel("tests.timer.matrix_plus_matrix");

    // make a timer
    process_timer_t t("tests.timer");

    channel << "Computing " << N << " matrix-matrix sums" << pyre::journal::endl;


    // ARRAY

    // array matrix
    std::array<double, 9> tensor1_c { 1.0, -1.0, 2.0, 1.0, 0.0, 1.0, 2.0, -1.0, 0.0 };
    std::array<double, 9> tensor2_c { 1.0, -1.0, 2.0, 1.0, 0.0, 1.0, 2.0, -1.0, 0.0 };
    std::array<double, 9> result_c { 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 };

    // reset timer
    t.reset();
    // start timer
    t.start();

    for (int n = 0; n < N; ++n) {
        // matrix + matrix (array)
        for (size_t i = 0; i < tensor1_c.size(); ++i) {
            result_c[i] += tensor2_c[i] + tensor1_c[i];
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


    // PYRE TENSOR
    // tensor matrix
    pyre::tensor::matrix_t<3> tensor1 { 1.0, -1.0, 2.0, 1.0, 0.0, 1.0, 2.0, -1.0, 0.0 };
    pyre::tensor::matrix_t<3> tensor2 { 1.0, -1.0, 2.0, 1.0, 0.0, 1.0, 2.0, -1.0, 0.0 };
    pyre::tensor::matrix_t<3> result_tensor { 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 };

    // reset timer
    t.reset();
    // start timer
    t.start();

    for (int n = 0; n < N; ++n) {
        // matrix + matrix (tensor)
        result_tensor += tensor2 + tensor1;
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
matrix_plus_symmetric_matrix(int N)
{
    // make a channel
    pyre::journal::info_t channel("tests.timer.matrix_plus_symmetric_matrix");

    // make a timer
    process_timer_t t("tests.timer");

    channel << "Computing " << N << " matrix-matrix sums (matrix + symmetric matrix)"
            << pyre::journal::endl;


    // ARRAY

    // array matrix
    std::array<double, 9> tensor1_c { 1.0, -1.0, 2.0, 1.0, 0.0, 1.0, 2.0, -1.0, 0.0 };
    std::array<double, 9> tensor2_c { 1.0, -1.0, 2.0, -1.0, 1.0, 0.0, 2.0, 0.0, 1.0 };
    std::array<double, 9> result_c { 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 };

    // reset timer
    t.reset();
    // start timer
    t.start();

    for (int n = 0; n < N; ++n) {
        // matrix + matrix (array)
        for (size_t i = 0; i < tensor1_c.size(); ++i) {
            result_c[i] += tensor2_c[i] + tensor1_c[i];
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


    // PYRE TENSOR
    // tensor matrix
    pyre::tensor::matrix_t<3> tensor1 { 1.0, -1.0, 2.0, 1.0, 0.0, 1.0, 2.0, -1.0, 0.0 };
    pyre::tensor::symmetric_matrix_t<3> tensor2 { 1.0,
                                                  -1.0,
                                                  2.0,
                                                  /*-1.0,*/ 1.0,
                                                  0.0,
                                                  /*2.0, 0.0,*/ 1.0 };
    pyre::tensor::matrix_t<3> result_tensor { 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 };

    // reset timer
    t.reset();
    // start timer
    t.start();

    for (int n = 0; n < N; ++n) {
        // matrix + matrix (tensor)
        result_tensor += tensor2 + tensor1;
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
matrix_plus_diagonal_matrix(int N)
{
    // make a channel
    pyre::journal::info_t channel("tests.timer.matrix_plus_diagonal_matrix");

    // make a timer
    process_timer_t t("tests.timer");

    channel << "Computing " << N << " matrix-matrix sums (matrix + diagonal matrix)"
            << pyre::journal::endl;


    // ARRAY

    // array matrix
    std::array<double, 9> tensor1_c { 1.0, -1.0, 2.0, 1.0, 0.0, 1.0, 2.0, -1.0, 0.0 };
    std::array<double, 9> tensor2_c { 1.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, 2.0 };
    std::array<double, 9> result_c { 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 };

    // reset timer
    t.reset();
    // start timer
    t.start();

    for (int n = 0; n < N; ++n) {
        // matrix + matrix (array)
        for (size_t i = 0; i < tensor1_c.size(); ++i) {
            result_c[i] += tensor2_c[i] + tensor1_c[i];
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


    // PYRE TENSOR
    // tensor matrix
    pyre::tensor::matrix_t<3> tensor1 { 1.0, -1.0, 2.0, 1.0, 0.0, 1.0, 2.0, -1.0, 0.0 };
    pyre::tensor::diagonal_matrix_t<3> tensor2 { 1.0, -1.0, 2.0 };
    pyre::tensor::matrix_t<3> result_tensor { 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 };

    // reset timer
    t.reset();
    // start timer
    t.start();

    for (int n = 0; n < N; ++n) {
        // matrix + matrix (tensor)
        result_tensor += tensor2 + tensor1;
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
symmetric_matrix_plus_diagonal_matrix(int N)
{
    // make a channel
    pyre::journal::info_t channel("tests.timer.symmetric_matrix_plus_diagonal_matrix");

    // make a timer
    process_timer_t t("tests.timer");

    channel << "Computing " << N << " matrix-matrix sums (symmetric matrix + diagonal matrix)"
            << pyre::journal::endl;


    // ARRAY

    // array matrix
    std::array<double, 9> tensor1_c { 1.0, -1.0, 2.0, -1.0, 1.0, 0.0, 2.0, 0.0, 1.0 };
    std::array<double, 9> tensor2_c { 1.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, 2.0 };
    std::array<double, 9> result_c { 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 };

    // reset timer
    t.reset();
    // start timer
    t.start();

    for (int n = 0; n < N; ++n) {
        // matrix + matrix (array)
        for (size_t i = 0; i < tensor1_c.size(); ++i) {
            result_c[i] += tensor2_c[i] + tensor1_c[i];
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


    // PYRE TENSOR
    // tensor matrix
    pyre::tensor::symmetric_matrix_t<3> tensor1 { 1.0,
                                                  -1.0,
                                                  2.0,
                                                  /*-1.0,*/ 1.0,
                                                  0.0,
                                                  /*2.0, 0.0,*/ 1.0 };
    pyre::tensor::diagonal_matrix_t<3> tensor2 { 1.0, -1.0, 2.0 };
    pyre::tensor::symmetric_matrix_t<3> result_tensor { 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 };

    // reset timer
    t.reset();
    // start timer
    t.start();

    for (int n = 0; n < N; ++n) {
        // matrix + matrix (tensor)
        result_tensor += tensor2 + tensor1;
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

    // matrix plus matrix
    matrix_plus_matrix(N);

    // matrix plus symmetric matrix
    matrix_plus_symmetric_matrix(N);

    // matrix plus diagonal matrix
    matrix_plus_diagonal_matrix(N);

    // symmetric matrix plus diagonal matrix
    symmetric_matrix_plus_diagonal_matrix(N);

    // all done
    return 0;
}


// end of file

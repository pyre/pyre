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
matrix_times_matrix(int N)
{
    // make a channel
    pyre::journal::info_t channel("tests.timer.matrix_times_matrix");

    // make a timer
    process_timer_t t("tests.timer");

    channel << "Computing " << N << " matrix-matrix multiplications" << pyre::journal::endl;


    // ARRAY

    // array matrix
    std::array<double, 9> tensor1_c { 1.0, -1.0, 2.0, 1.0, 0.0, 1.0, 2.0, -1.0, 0.0 };
    std::array<double, 9> tensor2_c { 1.0, -1.0, 2.0, 1.0, 0.0, 1.0, 2.0, -1.0, 0.0 };
    std::array<double, 9> result_c { 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 };

    const auto size_rows = tensor1_c.size() / 3;
    // reset timer
    t.reset();
    // start timer
    t.start();

    for (int n = 0; n < N; ++n) {
        // matrix * matrix (array)
        for (size_t i = 0; i < size_rows; ++i) {
            for (size_t j = 0; j < size_rows; ++j) {
                for (size_t k = 0; k < size_rows; ++k) {
                    result_c[j + i * size_rows] +=
                        tensor2_c[k + i * size_rows] * tensor1_c[j + k * size_rows];
                }
            }
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
        // matrix * matrix (tensor)
        result_tensor += tensor2 * tensor1;
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
matrix_times_symmetric_matrix(int N)
{
    // make a channel
    pyre::journal::info_t channel("tests.timer.matrix_times_matrix");

    // make a timer
    process_timer_t t("tests.timer");

    channel << "Computing " << N << " matrix-matrix multiplications" << pyre::journal::endl;


    // ARRAY

    // array matrix
    std::array<double, 9> tensor1_c { 1.0, -1.0, 2.0, 1.0, 0.0, 1.0, 2.0, -1.0, 0.0 };
    std::array<double, 9> tensor2_c { 1.0, -1.0, 2.0, -1.0, 1.0, 0.0, 2.0, 0.0, 1.0 };
    std::array<double, 9> result_c { 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 };

    const auto size_rows = tensor1_c.size() / 3;
    // reset timer
    t.reset();
    // start timer
    t.start();

    for (int n = 0; n < N; ++n) {
        // matrix * matrix (array)
        for (size_t i = 0; i < size_rows; ++i) {
            for (size_t j = 0; j < size_rows; ++j) {
                for (size_t k = 0; k < size_rows; ++k) {
                    result_c[j + i * size_rows] +=
                        tensor2_c[k + i * size_rows] * tensor1_c[j + k * size_rows];
                }
            }
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
        // matrix * matrix (tensor)
        result_tensor += tensor2 * tensor1;
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

    // matrix times matrix
    matrix_times_matrix(N);

    // matrix times symmetric matrix
    matrix_times_symmetric_matrix(N);

    // all done
    return 0;
}


// end of file

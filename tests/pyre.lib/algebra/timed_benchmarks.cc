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
#include <pyre/algebra.h>


// type aliases
using timer_t = pyre::timers::process_timer_t;

void scalar_vector_benchmark() 
{
    // make a channel
    pyre::journal::info_t channel("tests.timer");

    // make a timer
    timer_t t("tests.timer");
    
    // number of times to do operation
    int N = 1<<25;

    channel << "Computing " << N << " scalar-vector multiplications" << pyre::journal::endl;

    // ARRAY
    // a scalar
    pyre::algebra::real scalar = sqrt(2);

    // array vector
    std::array<double, 3> vector_c {1.0, -1.0, 2.0};
    std::array<double, 3> result_c {0.0, 0.0, 0.0};

    // start timer
    t.start();

    for (int n = 0; n < N; ++n) { 
        // scalar * vector (array)
        for (size_t i = 0; i < vector_c.size(); ++i)
        {
            result_c[i] += scalar * vector_c[i];
        }
    }

    // stop the timer
    t.stop();

    // report
    channel << "\t array (for loop) " << pyre::journal::newline
        << "\t\t result = " << result_c[0] << "\t" << result_c[1] << "\t" << result_c[2] 
            << pyre::journal::newline
        << "\t\t process time = " << t.ms() << " ms " << pyre::journal::endl;

    // reset timer
    t.reset();


    // PYRE TENSOR
    // tensor vector
    pyre::algebra::vector_t<3> vector {1.0, -1.0, 2.0};
    pyre::algebra::vector_t<3> result_tensor {0.0, 0.0, 0.0};

    // start timer
    t.start();

    for (int n = 0; n < N; ++n) { 
        // scalar * vector (tensor)
        result_tensor += scalar * vector;
    }

    // stop the timer
    t.stop();

    // report
    channel << "\t pyre tensor " << pyre::journal::newline
        << "\t\t result = " << result_tensor << pyre::journal::newline
        << "\t\t process time = " << t.ms() << " ms " << pyre::journal::endl;

    // all done
    return;
}

void scalar_product_vectors_benchmark() 
{
    // make a channel
    pyre::journal::info_t channel("tests.timer");

    // make a timer
    timer_t t("tests.timer");
    
    // number of times to do operation
    int N = 1<<25;

    channel << "Computing " << N << " scalar products" << pyre::journal::endl;


    // ARRAY FOR LOOP
    // array vector
    std::array<double, 3> vector_array_1 {1.0, -1.0, 2.0};
    std::array<double, 3> vector_array_2 {1.0, 1.0, 2.0};
    double result_array_for = 0.0;

    // start timer
    t.start();

    // vector * vector (array, for loop)
    for (int n = 0; n < N; ++n) { 
        for (size_t i = 0; i < vector_array_1.size(); ++i)
        {
            result_array_for += vector_array_1[i] * vector_array_2[i];
        }
    }

    // stop the timer
    t.stop();

    // report
    channel << "\t array (for loop) " << pyre::journal::newline
        << "\t\t result = " << result_array_for << pyre::journal::newline
        << "\t\t process time = " << t.ms() << " ms " << pyre::journal::endl;

    // reset timer
    t.reset();


    // ARRAY EXPANDED BY HAND
    double result_array = 0.0;

    // start timer
    t.start();

    // vector * vector (array, expanded)
    for (int n = 0; n < N; ++n) { 
        result_array += vector_array_1[0] * vector_array_2[0] 
            + vector_array_1[1] * vector_array_2[1] + vector_array_1[2] * vector_array_2[2];
    }

    // stop the timer
    t.stop();

    // report
    channel << "\t array (expanded) " << pyre::journal::newline
        << "\t\t result = " << result_array << pyre::journal::newline
        << "\t\t process time = " << t.ms() << " ms " << pyre::journal::endl;

    // reset timer
    t.reset();


    // PYRE TENSOR
    // tensor vector
    pyre::algebra::vector_t<3> vector_1 {1.0, -1.0, 2.0};
    pyre::algebra::vector_t<3> vector_2 {1.0, 1.0, 2.0};
    pyre::algebra::scalar_t result_tensor = 0.0;

    // start timer
    t.start();

    for (int n = 0; n < N; ++n) { 
        // vector * vector (tensor)
        result_tensor += vector_1 * vector_2;
    }

    // stop the timer
    t.stop();

    // report
    channel << "\t pyre tensor " << pyre::journal::newline
        << "\t\t result = " << result_tensor << pyre::journal::newline
        << "\t\t process time = " << t.ms() << " ms " << pyre::journal::endl;


    // all done
    return;
}


void scalar_tensor_benchmark() 
{
    // make a channel
    pyre::journal::info_t channel("tests.timer");

    // make a timer
    timer_t t("tests.timer");
    
    // number of times to do operation
    int N = 1<<25;

    channel << "Computing " << N << " scalar-vector multiplications" << pyre::journal::endl;

    // ARRAY
    // a scalar
    pyre::algebra::real scalar = sqrt(2);

    // array tensor
    std::array<double, 9> tensor_c {1.0, -1.0, 2.0, 1.0, 0.0, 1.0, 2.0, -1.0, 0.0};
    std::array<double, 9> result_c {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0};

    // start timer
    t.start();

    for (int n = 0; n < N; ++n) { 
        // scalar * vector (array)
        for (size_t i = 0; i < tensor_c.size(); ++i)
        {
            result_c[i] += scalar * tensor_c[i];
        }
    }

    // stop the timer
    t.stop();

    // report
    channel << "\t array (for loop) " << pyre::journal::newline
        << "\t\t result = " << result_c[0] << "\t" << result_c[1] << "\t" << result_c[2] 
            << pyre::journal::newline
        << "\t\t process time = " << t.ms() << " ms " << pyre::journal::endl;

    // reset timer
    t.reset();


    // PYRE TENSOR
    // tensor vector
    pyre::algebra::matrix_t<3> tensor {1.0, -1.0, 2.0, 1.0, 0.0, 1.0, 2.0, -1.0, 0.0};
    pyre::algebra::matrix_t<3> result_tensor {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0};

    // start timer
    t.start();

    for (int n = 0; n < N; ++n) { 
        // scalar * vector (tensor)
        result_tensor += scalar * tensor;
    }

    // stop the timer
    t.stop();

    // report
    channel << "\t pyre tensor " << pyre::journal::newline
        << "\t\t result = " << result_tensor << pyre::journal::newline
        << "\t\t process time = " << t.ms() << " ms " << pyre::journal::endl;

    // all done
    return;
}


int main() {

    scalar_vector_benchmark();
    scalar_product_vectors_benchmark();
    scalar_tensor_benchmark();

    return 0;
}


// end of file

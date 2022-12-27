// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_timers_Proxy_h)
#define pyre_timers_Proxy_h


// proxy for accessing a timer movement on behalf of a client
template <class timerT, class clockT>
class pyre::timers::Proxy {
    // types
public:
    // my client
    using timer_type = timerT;
    using timer_reference = timer_type &;
    // my clock type
    using clock_type = clockT;
    // my state
    using movement_type = Movement<clock_type>;
    using movement_reference = movement_type &;
    // its parts
    using active_type = typename movement_type::active_type;
    using duration_type = typename movement_type::duration_type;
    using time_point_type = typename movement_type::time_point_type;

    // metamethods
public:
    // constructor
    inline explicit Proxy(movement_reference);
    // let the compiler write the destructor
    ~Proxy() = default;

    // accessors
public:
    // ask whether the movement is active
    inline auto active() const;
    // get the timestamp of last activation
    inline auto mark() const;

    // interface
public:
    // buttons
    inline auto start();
    inline auto stop();
    inline auto reset() -> timer_reference;

    // readouts
    // get the accumulated time; make sure to stop the timer first, otherwise the behavior is
    // undefined
    inline auto read() const ;
    // compute the accumulated time without disturbing the timer;
    inline auto lap() const;

    // display convenience
    // return the accumulated time in seconds
    inline auto sec() const;
    // return the accumulated time in milliseconds
    inline auto ms() const;
    // return the accumulated time in microseconds
    inline auto us() const;

    // syntactic sugar
public:
    inline operator active_type() const;

    // disable constructors and assignments
private:
    Proxy(const Proxy &) = delete;
    Proxy(Proxy &&) = delete;
    Proxy & operator=(const Proxy &) = delete;
    Proxy & operator=(Proxy &&) = delete;

    // data member
private:
    movement_reference _movement;
};


// get the inline definitions
#define pyre_timers_Proxy_icc
#include "Proxy.icc"
#undef pyre_timers_Proxy_icc


#endif

// end of file

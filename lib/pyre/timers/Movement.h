// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_timers_Movement_h)
#define pyre_timers_Movement_h


// the state shared by all timers of a given type+name
template <class clockT>
class pyre::timers::Movement {
    // types
public:
    // me types
    using movement_type = Movement;
    using movement_reference = movement_type &;

    // my clock
    using clock_type = clockT;

    // my parts
    using active_type = bool;
    using duration_type = typename clock_type::duration_type;
    using time_point_type = typename clock_type::time_point_type;

    // convenience
    using seconds_type = seconds_t;
    using milliseconds_type = milliseconds_t;
    using microseconds_type = microseconds_t;

    // metamethods
public:
    inline explicit Movement();

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
    inline auto reset() -> movement_reference;

    // readouts
    // get the accumulated time; make sure to stop the timer first, otherwise the behavior is
    // undefined
    inline auto read() const ;
    // compute the accumulated time without disturbing the timer;
    inline auto lap() const;

    // display convenience
    // read the accumulated time and render it as a string in seconds
    inline auto sec() const;
    // read the accumulated time and render it as a string in milliseconds
    inline auto ms() const;
    // read the accumulated time and render it as a string in microseconds
    inline auto us() const;

    // syntactic sugar
public:
    inline operator active_type() const;

    // other meta-methods: let the compiler write these
public:
    // constructors and assignments
    Movement(const Movement &) = default;
    Movement(Movement &&) = default;
    Movement & operator=(const Movement &) = default;
    Movement & operator=(Movement &&) = default;
    // destructor
    ~Movement() = default;

    // data members
private:
    active_type _active;         // active timers accumulate time
    time_point_type _mark;       // timestamp from when the timer was last activated
    duration_type _elapsed;      // the total time this timer has been active
};


// get the inline definitions
#define pyre_timers_Movement_icc
#include "Movement.icc"
#undef pyre_timers_Movement_icc


#endif

// end of file

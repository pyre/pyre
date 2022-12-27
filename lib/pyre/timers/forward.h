// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_timers_forward_h)
#define pyre_timers_forward_h


// forward declarations of all user facing entities
namespace pyre::timers {
    // clocks
    class WallClock;
    class ProcessClock;

    // timer movements
    template <class timerT> class Movement;
    // and their proxies
    template <class timerT, class clockT> class Proxy;

    // the timer registry
    template <class movementT> class Registrar;

    // the timer
    template <class clockT, template <class, class> class proxyT> class Timer;
}


// when testing
#if defined(PYRE_CORE)
// type aliases of internal parts
namespace pyre::timers {
    // clocks
    using wall_clock_t = WallClock;
    using process_clock_t = ProcessClock;

    // timer parts
    template <class timerT>
    using movement_t = Movement<timerT>;

    // movement proxy; controls access to the shared timer state
    // for single threaded code, it is essentially a {movement_t &} that forwards its interface
    // for multi-threaded code, it's the place to park the access wrappers
    template <class timerT, class clockT>
    using proxy_t = Proxy<timerT, clockT>;

    // timer registry: a map from names to timer movements
    template <class movementT>
    using registrar_t = Registrar<movementT>;
}
# endif


# endif

// end of file

// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_timers_Timer_h)
#define pyre_timers_Timer_h


// user facing encapsulation of a timer
template <class clockT, template <class, class> class proxyT>
class pyre::timers::Timer : public proxyT<Timer<clockT, proxyT>, clockT> {
    // types
public:
    // my clock type
    using clock_type = clockT;
    // access to my shared state
    using proxy_type = proxyT<Timer<clockT, proxyT>, clockT>;
    // and its parts
    using movement_type = typename proxy_type::movement_type;
    // my registry
    using registry_type = Registrar<movement_type>;
    using registry_reference = registry_type &;
    // my name
    using name_type = typename registry_type::name_type;

    // metamethods
public:
    // constructor
    inline explicit Timer(const name_type &);
    // let the compiler write the destructor
    ~Timer() = default;

    // accessors
public:
    inline auto name() const;

    // static interface
public:
    inline static auto registry() -> registry_reference;

    // implementation details: data members
private:
    name_type _name;

    // implementation details: static data
private:
    // the timer registry
    inline static registry_type _registry;

    // disable constructors and assignments
private:
    Timer(const Timer &) = delete;
    Timer(Timer &&) = delete;
    Timer & operator=(const Timer &) = delete;
    Timer & operator=(Timer &&) = delete;
};


// get the inline definitions
#define pyre_timers_Timer_icc
#include "Timer.icc"
#undef pyre_timers_Timer_icc


#endif

// end of file

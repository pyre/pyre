// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_timers_Registrar_h)
#define pyre_timers_Registrar_h


// owner of the map (timer name -> shared movement)
template <class movementT>
class pyre::timers::Registrar
{
    // types
public:
    // timer names
    using name_type = name_t;
    // shared movement
    using movement_type = movementT;

    // the map from channel names to movement instances
    using registry_type = std::map<name_type, movement_type>;

    // metamethods
public:
    inline Registrar();
    // let the compiler write the rest
    Registrar(const Registrar &) = default;
    Registrar(Registrar &&) = default;
    Registrar & operator= (const Registrar &) = default;
    Registrar & operator= (Registrar &&) = default;

    // interface
public:
    // simple access to the underlying index
    inline auto size() const;
    inline auto empty() const;
    inline auto contains(const name_type &) const;

    // explicit movement insertion
    inline auto emplace(const name_type &);

    // iteration
    inline auto begin() const;
    inline auto end() const;

    // look up the movement of the named timer
    inline auto lookup(const name_type &) -> movement_type &;

    // data members
private:
    registry_type _registry;
};


// get the inline definitions
#define pyre_timers_Registrar_icc
#include "Registrar.icc"
#undef pyre_timers_Registrar_icc


#endif

// end of file

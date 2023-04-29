// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_journal_Null_h)
#define pyre_journal_Null_h


// the null channel conforms to the API but has no effect
class pyre::journal::Null
{
    // types
public:
    // channel names
    using name_type = name_t;
    using nameset_type = nameset_t;
    // parts
    using active_type = bool;
    using fatal_type = bool;
    using device_type = void *;

    // metamethods
public:
    // constructor
    inline explicit Null(const name_type &);

    // accessors
public:
    inline constexpr auto active() const;
    inline constexpr auto fatal() const;
    inline constexpr auto device() const -> device_type;

    // mutators
public:
    inline constexpr auto active(active_type) -> Null &;
    inline constexpr auto fatal(fatal_type) -> Null &;
    inline constexpr auto device(device_type) -> Null &;

    // syntactic sugar
public:
    inline constexpr operator active_type() const;

    // interface
public:
    // state management
    inline constexpr void activate() const;
    inline constexpr void deactivate() const;

    // bulk activation
    static constexpr inline void activateChannels(const nameset_type &);

    // disallow
private:
    Null(const Null &) = delete;
    Null(const Null &&) = delete;
    const Null & operator= (const Null &) = delete;
    const Null & operator= (const Null &&) = delete;
};


// get the inline definitions
#define pyre_journal_Null_icc
#include "Null.icc"
#undef pyre_journal_Null_icc


#endif

// end of file

// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_viz_filters_LogSaw_h)
#define pyre_viz_filters_LogSaw_h


// a filter computes the fractional part of the logarithm of its source
template <class sourceT>
class pyre::viz::filters::LogSaw {
    // types
public:
    // my template parameter
    using source_type = sourceT;
    // and its reference type
    using source_const_reference = const source_type &;
    // my value type
    using value_type = double;

    // metamethods
public:
    // constructor
    inline LogSaw(source_const_reference source);

    // interface
public:
    inline auto operator*() const -> value_type;
    inline auto operator++() -> void;

    // implementation details: data
private:
    source_type _source;

    // default metamethods
public:
    // destructor
    ~LogSaw() = default;

    // constructors
    LogSaw(const LogSaw &) = default;
    LogSaw & operator=(const LogSaw &) = default;
    LogSaw(LogSaw &&) = default;
    LogSaw & operator=(LogSaw &&) = default;
};


// get the inline definitions
#define pyre_viz_filters_LogSaw_icc
#include "LogSaw.icc"
#undef pyre_viz_filters_LogSaw_icc


#endif

// end of file

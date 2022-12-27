// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2023 all rights reserved

// code guard
#if !defined(pyre_viz_filters_Imaginary_h)
#define pyre_viz_filters_Imaginary_h


// a filter that extracts the amplitude of its complex data source
template <class sourceT>
class pyre::viz::filters::Imaginary {
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
    inline Imaginary(source_const_reference source);

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
    ~Imaginary() = default;

    // constructors
    Imaginary(const Imaginary &) = default;
    Imaginary & operator=(const Imaginary &) = default;
    Imaginary(Imaginary &&) = default;
    Imaginary & operator=(Imaginary &&) = default;
};


// get the inline definitions
#define pyre_viz_filters_Imaginary_icc
#include "Imaginary.icc"
#undef pyre_viz_filters_Imaginary_icc


#endif

// end of file

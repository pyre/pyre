// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "forward.h"


// a space with a chart and the code an authority assigns to the pair, such as 4326 from the
// EPSG for longitude and latitude on the WGS84 ellipsoid; the code is what PostGIS calls the
// SRID; the datum is carried by the parameters of the space
template <class chartT>
class pyre::geometry::ReferenceSystem {
    // type aliases
public:
    // me
    using self_type = ReferenceSystem<chartT>;
    // my chart
    using chart_type = chartT;
    // my space
    using space_type = typename chart_type::space_type;
    // my parts
    using string_type = string_t;
    using code_type = int;

    // metamethods
public:
    // a reference system with the given parts
    ReferenceSystem(
        const space_type & space, const chart_type & chart, const string_type & authority,
        code_type code);

    // the rest
    ReferenceSystem(const ReferenceSystem &) = default;
    ReferenceSystem(ReferenceSystem &&) = default;
    ReferenceSystem & operator=(const ReferenceSystem &) = default;
    ReferenceSystem & operator=(ReferenceSystem &&) = default;
    ~ReferenceSystem() = default;

    // equality
    auto operator==(const ReferenceSystem &) const -> bool = default;

    // interface
public:
    // my space
    auto space() const -> const space_type &;
    // my chart
    auto chart() const -> const chart_type &;
    // the authority that assigned my code
    auto authority() const -> const string_type &;
    // my code
    auto code() const -> code_type;

    // implementation details - data
private:
    space_type _space;
    chart_type _chart;
    string_type _authority;
    code_type _code;
};


// get the inline definitions
#include "ReferenceSystem.icc"


// end of file

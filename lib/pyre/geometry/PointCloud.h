// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "forward.h"


// a collection of points
template <typename pointT>
class pyre::geometry::PointCloud {
    // type aliases
public:
    // me
    using self_type = PointCloud<pointT>;
    // my points
    using point_type = pointT;
    // indices
    using size_type = size_t;
    // my storage
    using rep_type = std::vector<point_type>;

    // metamethods
public:
    // a cloud of {count} points, each one built by the default constructor of its type
    inline explicit PointCloud(size_type count);

    // the rest
    PointCloud(const PointCloud &) = default;
    PointCloud(PointCloud &&) = default;
    PointCloud & operator=(const PointCloud &) = default;
    PointCloud & operator=(PointCloud &&) = default;
    ~PointCloud() = default;

    // interface
public:
    // iteration
    inline auto begin() const;
    inline auto end() const;

    // indexed access
    inline auto & operator[](size_type pos);
    inline const auto & operator[](size_type pos) const;

    // implementation details
private:
    rep_type _points;
};


// get the inline definitions
#include "PointCloud.icc"


// end of file

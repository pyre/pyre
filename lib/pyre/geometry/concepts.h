// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// my dependencies
#include "forward.h"


// set up the namespace
namespace pyre::geometry {

    // a space knows its dimension and how its points are stored
    template <class S>
    concept space_c = requires(std::ostream & stream, const typename S::rep_type & rep) {
        // the dimension is known at compile time
        { S::dimension() } -> std::convertible_to<size_t>;
        // and the space knows how to write its points
        S::inject(stream, rep);
    };

    // a metric space measures the distance between two of its points
    template <class S>
    concept metric_space_c = space_c<S> and requires(const S & space, const Point<S> & point) {
        // the distance between two points
        { space.distance(point, point) } -> std::convertible_to<double>;
    };

    // an affine space subtracts points to get vectors, and translates points by vectors
    template <class S>
    concept affine_space_c =
        space_c<S>
        and requires(const typename S::rep_type & rep, const typename S::vector_type & vector) {
                // the vector from one point to another
                { S::difference(rep, rep) } -> std::same_as<typename S::vector_type>;
                // a point translated by a vector
                { S::translate(rep, vector) } -> std::same_as<typename S::rep_type>;
            };

    // a line is a space of one dimension whose points are ordered by a coordinate, which extends
    // to the infinities so that the line has ends
    template <class S>
    concept line_c =
        space_c<S> and (S::dimension() == 1)
        and requires(const typename S::rep_type & rep, const typename S::coordinate_type & x) {
                // the coordinate of a point
                { S::coordinate(rep) } -> std::same_as<typename S::coordinate_type>;
                // the point at a coordinate
                { S::fromCoordinate(x) } -> std::same_as<typename S::rep_type>;
            };

    // a chart maps the points of its space to coordinates and back
    template <class C>
    concept chart_c = space_c<typename C::space_type>
                  and requires(
                          const C & chart, const typename C::coordinates_type & coordinates,
                          const Point<typename C::space_type> & point) {
                          // the point with the given coordinates
                          {
                              chart.point(coordinates)
                          } -> std::same_as<Point<typename C::space_type>>;
                          // the coordinates of a point
                          {
                              chart.coordinates(point)
                          } -> std::same_as<typename C::coordinates_type>;
                      };

} // namespace pyre::geometry


// end of file

// -*- C++ -*-
//
// michael a.g. aïvázis
// orthologue
// (c) 1998-2016 all rights reserved
//

// Representation of a logical d-dimensional parallelopiped
//
// A brick is a container of 2^d nodes whose actual type is a template parameter

// declaration of bricks
template <std::size_t dim, typename nodeT>
class pyre::geometry::Brick {
    // types
public:
    typedef nodeT node_type;
    typedef std::size_t size_type;
    typedef std::array<node_type, 1<<dim> rep_type; // 2^d nodes of a type of your choice

    // meta-methods
public:
    template <typename... cornerT> inline Brick(cornerT... corner);

    // interface
public:
    // the dimension of the underlying space
    inline constexpr static auto dimension();
    // the intrinsic dimension of the brick
    inline constexpr static auto intrinsicDimension();
    // the number of points in the brick
    inline constexpr static auto points();

    // indexed access
    inline auto operator[](size_type item) const;

    // support for ranged for loops
    inline auto begin() const;
    inline auto end() const;

    // implementation details
private:
    rep_type _corners;
};


// end of file

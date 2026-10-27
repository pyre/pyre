// -*- c++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// externals
#include "external.h"
// namespace setup
#include "forward.h"


// helpers
namespace pyre::py::flow {
    // bind the variables that hold a value of type {cellT}, and register them with the catalog
    template <typename cellT>
    inline void bindVariable(py::module & m)
    {
        // the variable
        using variable_type = var_t<cellT>;
        // register it with the catalog
        registry().registerProduct<variable_type>();
        // its readable name, which must outlive the binding of the class
        auto name = variable_type::className();
        // bind it, under its readable name
        auto cls = py::classh<variable_type, product_t>(
            // the scope
            m,
            // the name of the class
            name.c_str(),
            // the docstring
            "a scalar");
        // the spelling of its type, which is its key in the catalog
        cls.def_property_readonly_static(
            // the name
            "decl",
            // the implementation
            [](const py::object &) -> string_t { return variable_type::declSelf(); },
            // the docstring
            "the declaration of my type, which is my key in the catalog");
        // its value
        cls.def_property(
            // the name
            "value",
            // the getter refreshes the value if it is stale
            [](variable_type & self) -> cellT { return self.value(); },
            // the setter marks whatever is computed from the value as stale
            [](variable_type & self, cellT value) -> void { self.value(value); },
            // the docstring
            "my value, refreshed if it is stale; setting it marks whatever is computed from it as "
            "stale");
        // all done
        return;
    }
} // namespace pyre::py::flow


// the variables
void
pyre::py::flow::variables(py::module & m)
{
    // the scalars the factories in the catalog take
    bindVariable<pyre::memory::float64_t>(m);
    // all done
    return;
}


// end of file

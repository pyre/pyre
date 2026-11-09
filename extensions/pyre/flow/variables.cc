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
    // apply {step} to each type of value there are variables of
    template <class stepT>
    inline void variableCells(stepT step)
    {
        // the scalars the factories in the catalog take
        step.template operator()<pyre::memory::float64_t>();
        // all done
        return;
    }

    // register the class of the variables that hold a value of type {cellT}, so that every
    // signature can name it
    template <typename cellT>
    inline void variableClass(py::module & m)
    {
        // the variable
        using variable_type = var_t<cellT>;
        // its readable name, which must outlive the registration of the class
        auto name = variable_type::className();
        // register it, under its readable name
        py::classh<variable_type, product_t>(
            // the scope
            m,
            // the name of the class
            name.c_str(),
            // the docstring
            "a scalar");
        // all done
        return;
    }

    // bind the variables that hold a value of type {cellT}, and register them with the catalog
    template <typename cellT>
    inline void bindVariable()
    {
        // the variable
        using variable_type = var_t<cellT>;
        // register it with the catalog
        registry().registerProduct<variable_type>();
        // its class, registered by {variableClass}
        auto cls = py::classh<variable_type, product_t>(py::type::of<variable_type>());
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


// register the classes of the variables, so that every signature can name them
void
pyre::py::flow::variableClasses(py::module & m)
{
    // one type of value at a time
    variableCells([&m]<typename cellT>() {
        // register the class of its variables
        variableClass<cellT>(m);
        // all done
        return;
    });
    // all done
    return;
}


// the variables
void
pyre::py::flow::variables()
{
    // one type of value at a time
    variableCells([]<typename cellT>() {
        // bind its variables
        bindVariable<cellT>();
        // all done
        return;
    });
    // all done
    return;
}


// end of file

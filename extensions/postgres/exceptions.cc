// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// external dependencies
#include "external.h"
// namespace setup
#include "forward.h"


// the machinery this file needs, and nobody else does
namespace pyre::postgres::py {
    // the module that holds the python side of the hierarchy
    //
    // it is imported the first time an exception has to cross the boundary, and never again. it
    // may not be imported as this module is initialized: {pyre.db} imports the component that
    // imports us, so reaching back for it then would close the cycle
    //
    // the reference is deliberately leaked. a {py::object} with static storage would be
    // destroyed after the interpreter has finalized, and dropping a reference at that point is
    // undefined behavior
    static auto errors() -> const py::object &
    {
        // import it, once
        static const py::object * module =
            new py::object(py::module_::import("pyre.db.exceptions"));
        // and hand it back
        return *module;
    }

    // spread the server's report across the keyword arguments its python counterpart expects
    static auto payload(const Diagnostic & diagnostic) -> py::dict
    {
        // the explanation, which is what the python classes render
        py::dict kwds;
        kwds["diagnostic"] = diagnostic.message();
        // the only part of a complaint that is portable, and hence the only part worth branching
        // on; this is what the bindings this package replaces threw away
        kwds["sqlstate"] = diagnostic.sqlstate();
        // the statement that provoked it
        kwds["command"] = diagnostic.command();
        // how bad the server thinks it is
        kwds["severity"] = diagnostic.severity();
        // and the elaborations, each of which is empty when the server did not supply it
        kwds["detail"] = diagnostic.detail();
        kwds["hint"] = diagnostic.hint();
        kwds["position"] = diagnostic.position();
        // together with the object it is about, which is how a caller with two unique indices
        // tells them apart without reading english
        kwds["schema"] = diagnostic.schema();
        kwds["table"] = diagnostic.table();
        kwds["column"] = diagnostic.column();
        kwds["datatype"] = diagnostic.datatype();
        kwds["constraint"] = diagnostic.constraint();

        // hand it off
        return kwds;
    }

    // raise the python exception named {name}, built out of {error}
    static auto raise(classname_t name, const Exception & error) -> void
    {
        // find the class; it is the very one {pyre.db} publishes, so that the {except} clauses
        // client code has always written keep working, and keep catching what they always did
        const py::object cls = errors().attr(name);
        // build an instance out of the server's report
        const py::object instance = cls(**payload(error.diagnostic()));
        // and arm it
        PyErr_SetObject(cls.ptr(), instance.ptr());

        // all done
        return;
    }
} // namespace pyre::postgres::py


// teach pybind11 how to carry what {pyre::postgres} throws across into python
//
// note that this is a translator, and not a set of {py::register_exception} calls. those would
// mint new python classes, which must not happen: {pyre.db.exceptions} already publishes this
// hierarchy, client code already catches it, and the classes there derive from {FrameworkError},
// which a freshly minted class would not
void
pyre::postgres::py::exceptions(py::module &)
{
    // one translator does the lot
    py::register_exception_translator([](std::exception_ptr raised) {
        // rethrow whatever we were handed, so that the clauses below may sort it
        try {
            // there is always something
            if (raised) {
                std::rethrow_exception(raised);
            }
        }
        // the order below matters: each leaf must be caught before the base it derives from, or
        // a {DataError} would arrive in python under its parent's name
        catch (const DataError & error) {
            raise("DataError", error);
        }
        catch (const IntegrityError & error) {
            raise("IntegrityError", error);
        }
        catch (const InternalError & error) {
            raise("InternalError", error);
        }
        catch (const OperationalError & error) {
            raise("OperationalError", error);
        }
        catch (const ProgrammingError & error) {
            raise("ProgrammingError", error);
        }
        catch (const NotSupportedError & error) {
            raise("NotSupportedError", error);
        }
        // the two interior nodes
        catch (const DatabaseError & error) {
            raise("DatabaseError", error);
        }
        catch (const InterfaceError & error) {
            raise("InterfaceError", error);
        }
        // and the two roots; a warning is not an error, and does not derive from one
        catch (const Warning & error) {
            raise("Warning", error);
        }
        catch (const Error & error) {
            raise("Error", error);
        }
        // anything else the package throws is, by construction, one of the above; this clause is
        // here so that a leaf added to the hierarchy and forgotten here still arrives in python
        // as something a client can catch, rather than as a call to {std::terminate}
        catch (const Exception & error) {
            raise("Error", error);
        }
    });

    // all done
    return;
}


// end of file

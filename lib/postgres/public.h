// -*- C++ -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// code guard
#pragma once


// external packages
#include "external.h"
// set up the namespace
#include "forward.h"

// published type aliases and declarations that constitute the public API of this package
// this is the file you are looking for
#include "api.h"

// what the server says when a statement does not work out, and the exceptions that carry it
#include "Diagnostic.h"
#include "Error.h"
// the shared ownership of a libpq object
#include "traits.h"
#include "Handle.h"
// the names for the states libpq reports
#include "status.h"
// the translation between the values of a c++ program and the text postgres exchanges
#include "codecs.h"
// what the server sends back when a statement does work out
#include "Field.h"
#include "Row.h"
#include "Result.h"
// what other sessions have to say
#include "Notification.h"
// the session, and the scope of the work done over it
#include "Connection.h"
#include "Transaction.h"


// end of file

// -*- c++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

#pragma once


// establish the namespace, the fundamental color types, and the external dependencies
#include "forward.h"

// the published api: the color converter declarations; this is the file you are looking for
#include "api.h"

// the {rgb} converters
#include "rgb/hl.h"
#include "rgb/hsb.h"
#include "rgb/hsl.h"
#include "rgb/oklch.h"

// the {ansi} serializers
#include "ansi/gray.h"
#include "ansi/reset.h"
#include "ansi/rgb.h"
#include "ansi/rgb256.h"


// end of file

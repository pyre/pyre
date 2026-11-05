// -*- web -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved


// the plugins of the eslint toolchain, for the configurations of projects: a configuration is an
// es module, and it can't reach the modules of the toolchain by name, since the imports of es
// modules don't consult {NODE_PATH}; this module lives next to them, so its imports find them, and
// a configuration imports it by the path in {MM_ESLINT_PLUGINS}

// the rules that lay out the code
export { default as stylistic } from "@stylistic/eslint-plugin"
// and the ones that reflow its comments
export { default as commentLength } from "eslint-plugin-comment-length"


// end of file

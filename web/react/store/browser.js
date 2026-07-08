// -*- web -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// externals
import { createResponsiveStateReducer } from 'redux-responsive'

// create a reducer that is aware of the height and width of the browser
const reducer = createResponsiveStateReducer(null, {
    extraFields: () => ({
        width: window.innerWidth,
        height: window.innerHeight,
    })
})

// publish
export default reducer

// end of file

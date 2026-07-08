// -*- web -*-
// -*- coding: utf-8 -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 1998-2026 all rights reserved

// externals
import React from 'react'
// locals
import document from './styles'

// render
const Narrative = ({children, style}) => (
    <div style={{...document.narrative, ...style}}>
        {children}
    </div>
)

// defaults
Narrative.defaultProps = {
    style: {},
}

// publish
export default Narrative

// end of file
